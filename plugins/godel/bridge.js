/**
 * bridge.js — Godel Bridge (domain-agnostic)
 *
 * HTTP server that receives questions, injects memory+field context,
 * calls an LLM via Claude Code CLI, parses structured meta from output,
 * and maintains dual-layer memory (tape + field).
 *
 * Port: configurable via GODEL_PORT env (default 3004)
 * Identity: reads IDENTITY.md from same directory as system prompt
 *
 * Endpoints:
 *   POST /ask     — send a question, get an inverted answer
 *   GET  /status  — service health + field summary
 *   GET  /field   — current field state (vector, tensions, saturation)
 *   GET  /memory  — tape stats + recent entries
 *   GET  /history — last 10 tasks
 */

const http = require('http');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// --- Config ---

const PORT = parseInt(process.env.GODEL_PORT || '3004', 10);
const PROJECT_DIR = process.env.GODEL_DIR || __dirname;
const DATA_DIR = path.join(PROJECT_DIR, 'data');
const MEMORY_FILE = path.join(DATA_DIR, 'godel_memory.jsonl');
const FIELD_FILE = path.join(DATA_DIR, 'godel_field.json');
const MEMORY_CONTEXT_SIZE = parseInt(process.env.GODEL_MEMORY_SIZE || '10', 10);
const MAX_TIMEOUT = parseInt(process.env.GODEL_TIMEOUT || String(5 * 60 * 1000), 10);
const MAX_CONCURRENT = parseInt(process.env.GODEL_CONCURRENCY || '1', 10);

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

let activeTasks = 0;
let taskHistory = [];

// --- Parsing GODEL_META from output ---

function parseGodelMeta(output) {
    const metaRegex = /<!-- GODEL_META\s*\n([\s\S]*?)-->/;
    const match = output.match(metaRegex);
    if (!match) return null;

    const block = match[1];
    const meta = {};

    const residuoMatch = block.match(/residuo:\s*(.+)/);
    if (residuoMatch) meta.residuo = residuoMatch[1].trim();

    const vettoreMatch = block.match(/vettore:\s*\[([^\]]+)\]/);
    if (vettoreMatch) {
        meta.vettore = {};
        const pairs = vettoreMatch[1].split(',');
        for (const p of pairs) {
            const [key, val] = p.split(':').map(s => s.trim());
            if (key && val) meta.vettore[key] = parseFloat(val) || 0;
        }
    }

    const satMatch = block.match(/saturazione:\s*(true|false)/i);
    if (satMatch) meta.saturazione = satMatch[1].toLowerCase() === 'true';

    return meta;
}

function stripGodelMeta(output) {
    return output.replace(/<!-- GODEL_META\s*\n[\s\S]*?-->\s*/, '').trim();
}

// --- Field (aggregated state vector) ---

const DEFAULT_FIELD = {
    vettore: { DUALE: 0, CONFINE: 0, DOMINIO: 0, ROTTURA: 0, SCALA: 0 },
    ultimo_residuo: null,
    tensioni_aperte: [],
    saturazioni: 0,
    interazioni: 0,
    ultimo_aggiornamento: null,
};

function loadField() {
    try {
        if (!fs.existsSync(FIELD_FILE)) return { ...DEFAULT_FIELD };
        return JSON.parse(fs.readFileSync(FIELD_FILE, 'utf8'));
    } catch { return { ...DEFAULT_FIELD }; }
}

function updateField(meta) {
    const field = loadField();
    field.interazioni++;
    field.ultimo_aggiornamento = new Date().toISOString();

    if (meta.residuo) {
        field.ultimo_residuo = meta.residuo;
        field.tensioni_aperte.push(meta.residuo);
        if (field.tensioni_aperte.length > 5) field.tensioni_aperte.shift();
    }

    if (meta.vettore) {
        const alpha = 0.3;
        for (const axis of Object.keys(field.vettore)) {
            if (meta.vettore[axis] !== undefined) {
                field.vettore[axis] = field.vettore[axis] * (1 - alpha) + meta.vettore[axis] * alpha;
                field.vettore[axis] = Math.round(field.vettore[axis] * 1000) / 1000;
            }
        }
    }

    if (meta.saturazione) field.saturazioni++;

    try {
        fs.writeFileSync(FIELD_FILE, JSON.stringify(field, null, 2));
    } catch (e) {
        console.error('[GODEL] Field write failed:', e.message);
    }

    return field;
}

// --- Memory (tape + injection) ---

function loadAllMemory() {
    try {
        if (!fs.existsSync(MEMORY_FILE)) return [];
        const lines = fs.readFileSync(MEMORY_FILE, 'utf8').trim().split('\n').filter(Boolean);
        return lines.map(line => {
            try { return JSON.parse(line); } catch { return null; }
        }).filter(Boolean);
    } catch { return []; }
}

function selectByResonance(memories, question, limit) {
    if (memories.length <= limit) return memories;

    const qLower = question.toLowerCase();
    const qVector = {
        DUALE: /scegli|decid|dilemma|oppure|bivio|dualit|choose|decision/i.test(qLower) ? 1 : 0,
        CONFINE: /confin|limit|soglia|spazi|terzo|inclus|boundary|threshold/i.test(qLower) ? 1 : 0,
        DOMINIO: /trasfer|applic|domini|contesto|campo|port|domain|context|transfer/i.test(qLower) ? 1 : 0,
        ROTTURA: /rottur|cambi|rompere|crisi|frattur|discontinu|break|crisis|disrupt/i.test(qLower) ? 1 : 0,
        SCALA: /tempo|scala|cresci|evol|cicl|fase|time|scale|growth|phase/i.test(qLower) ? 1 : 0,
    };

    const scored = memories.map(m => {
        if (!m.vettore) return { m, score: 0 };
        let dot = 0, normQ = 0, normM = 0;
        for (const axis of Object.keys(qVector)) {
            const qv = qVector[axis];
            const mv = m.vettore[axis] || 0;
            dot += qv * mv;
            normQ += qv * qv;
            normM += mv * mv;
        }
        const denom = Math.sqrt(normQ) * Math.sqrt(normM);
        const score = denom > 0 ? dot / denom : 0;
        return { m, score };
    });

    scored.sort((a, b) => b.score - a.score);
    const byResonance = scored.filter(s => s.score > 0.1).slice(0, limit).map(s => s.m);

    if (byResonance.length >= limit) return byResonance;

    const ids = new Set(byResonance.map(m => m.ts));
    const recent = memories.slice(-limit).reverse().filter(m => !ids.has(m.ts));
    return [...byResonance, ...recent].slice(0, limit);
}

function buildMemoryContext(memories, field) {
    let ctx = '';

    if (field && field.interazioni > 0) {
        ctx += '[FIELD STATE]\n';
        ctx += `Vector: ${JSON.stringify(field.vettore)}\n`;
        if (field.ultimo_residuo) ctx += `Last residue: ${field.ultimo_residuo}\n`;
        if (field.tensioni_aperte.length) ctx += `Open tensions: ${field.tensioni_aperte.join(' | ')}\n`;
        ctx += `Interactions: ${field.interazioni}, Saturations: ${field.saturazioni}\n`;
        ctx += '[/FIELD]\n\n';
    }

    if (memories.length) {
        ctx += '[RECENT MEMORY]\n';
        for (const m of memories) {
            ctx += `[${m.ts}] Q: ${m.q}\n`;
            if (m.residuo) {
                ctx += `Residue: ${m.residuo}\n`;
            } else {
                ctx += `A: ${m.a}\n`;
            }
            ctx += '\n';
        }
        ctx += '[/MEMORY]\n\n';
    }

    return ctx;
}

function saveToMemory(question, answer, meta, mode) {
    try {
        const entry = {
            ts: new Date().toISOString(),
            mode: mode || 'manual',
            q: question,
            a: answer.slice(0, 2000),
        };
        if (meta) {
            if (meta.residuo) entry.residuo = meta.residuo;
            if (meta.vettore) entry.vettore = meta.vettore;
            if (meta.saturazione !== undefined) entry.saturazione = meta.saturazione;
        }
        fs.appendFileSync(MEMORY_FILE, JSON.stringify(entry) + '\n');
    } catch (e) {
        console.error('[GODEL] Memory write failed:', e.message);
    }
}

// --- LLM runner (Claude Code CLI) ---

function runClaudeCode(prompt) {
    return new Promise((resolve, reject) => {
        const args = [
            '--output-format', 'text',
            '--max-turns', '15',
            '--permission-mode', 'acceptEdits',
            '-p', prompt,
        ];

        const env = { ...process.env, HOME: process.env.HOME || '/root' };
        // Remove env vars that trigger "nested session" check
        for (const key of Object.keys(env)) {
            if (key.startsWith('CLAUDE')) delete env[key];
        }

        const proc = spawn('claude', args, {
            cwd: PROJECT_DIR,
            env,
            stdio: ['ignore', 'pipe', 'pipe'],
            timeout: MAX_TIMEOUT,
        });

        let stdout = '';
        let stderr = '';

        proc.stdout.on('data', (d) => { stdout += d.toString(); });
        proc.stderr.on('data', (d) => { stderr += d.toString(); });

        proc.on('close', (code) => {
            resolve({
                exit_code: code,
                output: stdout.trim(),
                error: stderr.trim(),
            });
        });

        proc.on('error', (err) => {
            reject(err);
        });

        setTimeout(() => {
            try { proc.kill('SIGTERM'); } catch (e) {}
            reject(new Error('Timeout'));
        }, MAX_TIMEOUT);
    });
}

// --- HTTP Server ---

const server = http.createServer(async (req, res) => {
    res.setHeader('Content-Type', 'application/json');

    // Health
    if (req.method === 'GET' && req.url === '/status') {
        const field = loadField();
        res.end(JSON.stringify({
            service: 'godel-bridge',
            active: activeTasks,
            history: taskHistory.length,
            uptime: process.uptime(),
            field: field.vettore,
            interactions: field.interazioni,
        }));
        return;
    }

    // Ask
    if (req.method === 'POST' && req.url === '/ask') {
        if (activeTasks >= MAX_CONCURRENT) {
            res.writeHead(429);
            res.end(JSON.stringify({ error: 'The oracle is already thinking. Try again.' }));
            return;
        }

        let body = '';
        req.on('data', (chunk) => { body += chunk; });
        req.on('end', async () => {
            try {
                const { question, context, mode } = JSON.parse(body);
                if (!question) {
                    res.writeHead(400);
                    res.end(JSON.stringify({ error: 'A question is required.' }));
                    return;
                }

                activeTasks++;
                const taskId = `godel_${Date.now()}`;
                const start = Date.now();

                console.log(`[GODEL] Task ${taskId}: ${question.slice(0, 80)}...`);

                const field = loadField();
                const allMemory = loadAllMemory();
                const selected = selectByResonance(allMemory, question, MEMORY_CONTEXT_SIZE);
                const memoryCtx = buildMemoryContext(selected, field);

                let prompt = '';
                if (memoryCtx) prompt += memoryCtx;
                if (context) prompt += `Context: ${context}\n\n`;
                prompt += question;

                try {
                    let result = await runClaudeCode(prompt);
                    let elapsed = ((Date.now() - start) / 1000).toFixed(1);

                    if (result.error) console.log(`[GODEL] stderr: ${result.error.slice(0, 200)}`);
                    if (result.exit_code !== 0) console.log(`[GODEL] exit_code: ${result.exit_code}`);

                    // Escalation: if max-turns or empty output, force collapse
                    const isLoop = result.output.includes('Reached max turns')
                        || result.output.includes('max_turns')
                        || (!result.output.trim() && result.exit_code !== 0);

                    if (isLoop) {
                        console.log(`[GODEL] Loop detected — escalation: forcing collapse`);
                        const collapsePrompt = `Do NOT explore files. Do NOT use tools. Respond ONLY with text. The question was: "${question.slice(0, 500)}". You went into a loop. Apply det(M)=-1: invert the viewpoint. Produce ONLY the resultant in max 3 sentences and the GODEL_META block. No analysis, no preambles.`;
                        result = await runClaudeCode(collapsePrompt);
                        elapsed = ((Date.now() - start) / 1000).toFixed(1);
                        console.log(`[GODEL] Collapse in ${elapsed}s`);
                    }

                    // Parse structured meta and update field
                    const meta = parseGodelMeta(result.output);
                    const cleanOutput = stripGodelMeta(result.output);

                    if (meta) {
                        updateField(meta);
                        console.log(`[GODEL] Meta: residue="${(meta.residuo || '').slice(0, 60)}" sat=${meta.saturazione}`);
                    }

                    if (cleanOutput) {
                        saveToMemory(question, cleanOutput, meta, mode);
                    }

                    taskHistory.push({
                        id: taskId,
                        mode: mode || 'manual',
                        question: question.slice(0, 100),
                        elapsed: `${elapsed}s`,
                        exit_code: result.exit_code,
                        timestamp: new Date().toISOString(),
                        has_meta: !!meta,
                        escalated: isLoop,
                    });

                    if (taskHistory.length > 50) taskHistory = taskHistory.slice(-50);

                    console.log(`[GODEL] Task ${taskId} done in ${elapsed}s${isLoop ? ' (escalated)' : ''}`);

                    res.end(JSON.stringify({
                        id: taskId,
                        answer: cleanOutput,
                        elapsed: `${elapsed}s`,
                        meta: meta || null,
                        escalated: isLoop,
                    }));
                } catch (err) {
                    console.error(`[GODEL] Task ${taskId} failed: ${err.message}`);
                    res.writeHead(500);
                    res.end(JSON.stringify({ error: err.message }));
                } finally {
                    activeTasks--;
                }

            } catch (e) {
                res.writeHead(400);
                res.end(JSON.stringify({ error: 'Invalid JSON.' }));
            }
        });
        return;
    }

    // History
    if (req.method === 'GET' && req.url === '/history') {
        res.end(JSON.stringify(taskHistory.slice(-10)));
        return;
    }

    // Memory
    if (req.method === 'GET' && req.url === '/memory') {
        const allMemory = loadAllMemory();
        const field = loadField();
        res.end(JSON.stringify({
            field,
            tape: { count: allMemory.length, recent: allMemory.slice(-5) },
        }));
        return;
    }

    // Field only
    if (req.method === 'GET' && req.url === '/field') {
        res.end(JSON.stringify(loadField()));
        return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
});

server.listen(PORT, '127.0.0.1', () => {
    console.log(`[GODEL] Bridge online on :${PORT}. Dual-layer memory active.`);
});
