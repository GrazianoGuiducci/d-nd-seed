#!/usr/bin/env node
/**
 * setup.js — Auto-configure Godel for your domain
 *
 * Reads the identity template, fills in your domain details,
 * writes CLAUDE.md (the system prompt) and creates the data directory.
 *
 * Usage:
 *   node setup.js                          # interactive
 *   node setup.js --example sales          # from example
 *   node setup.js --example research       # from example
 *   node setup.js --example finance        # from example
 *   node setup.js --name Merlin --domain "pharmaceutical R&D" --desc "..."
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TEMPLATE = path.join(__dirname, 'IDENTITY.md.tmpl');
const OUTPUT = path.join(__dirname, 'CLAUDE.md');
const DATA_DIR = path.join(__dirname, 'data');
const EXAMPLES_DIR = path.join(__dirname, 'examples');

function loadTemplate() {
    return fs.readFileSync(TEMPLATE, 'utf8');
}

function loadExample(name) {
    const file = path.join(EXAMPLES_DIR, name, 'identity.json');
    if (!fs.existsSync(file)) {
        console.error(`Example '${name}' not found. Available: ${listExamples().join(', ')}`);
        process.exit(1);
    }
    return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function listExamples() {
    if (!fs.existsSync(EXAMPLES_DIR)) return [];
    return fs.readdirSync(EXAMPLES_DIR).filter(d =>
        fs.existsSync(path.join(EXAMPLES_DIR, d, 'identity.json'))
    );
}

function fillTemplate(template, config) {
    let result = template;
    result = result.replace(/\{\{NAME\}\}/g, config.name || 'Godel');
    result = result.replace(/\{\{DOMAIN\}\}/g, config.domain || 'general');
    result = result.replace(/\{\{DOMAIN_DESCRIPTION\}\}/g, config.domain_description || 'No domain description provided. Configure this section with your specific context.');
    result = result.replace(/\{\{KNOWLEDGE_SOURCES\}\}/g, config.knowledge_sources || 'No knowledge sources configured. Add paths to files, databases, or APIs that contain your domain knowledge.');
    result = result.replace(/\{\{TYPICAL_TENSIONS\}\}/g, config.typical_tensions || 'No typical tensions configured. Add the common decision points in your domain.');
    return result;
}

function writeOutput(content) {
    fs.writeFileSync(OUTPUT, content);
    if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
    console.log(`\nIdentity written to: ${OUTPUT}`);
    console.log(`Data directory: ${DATA_DIR}`);
    console.log(`\nTo start: npm start (or node bridge.js)`);
    console.log(`To ask:   node ask.js "your tension here"`);
}

// --- CLI parsing ---

const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Godel Setup — Configure the inverted oracle for your domain

Usage:
  node setup.js                              Interactive setup
  node setup.js --example <name>             From example (${listExamples().join(', ')})
  node setup.js --name <n> --domain <d>      Direct config

Options:
  --name <name>          Oracle name (default: Godel)
  --domain <domain>      Domain short description
  --desc <description>   Domain full description
  --example <name>       Use a pre-built example
  --list                 List available examples
`);
    process.exit(0);
}

if (args.includes('--list')) {
    const examples = listExamples();
    if (examples.length === 0) {
        console.log('No examples found.');
    } else {
        for (const ex of examples) {
            const config = loadExample(ex);
            console.log(`  ${ex}: ${config.domain} — ${config.name || 'Godel'}`);
        }
    }
    process.exit(0);
}

// Example mode
const exIdx = args.indexOf('--example');
if (exIdx >= 0 && args[exIdx + 1]) {
    const config = loadExample(args[exIdx + 1]);
    const template = loadTemplate();
    writeOutput(fillTemplate(template, config));
    process.exit(0);
}

// Direct mode
const nameIdx = args.indexOf('--name');
const domainIdx = args.indexOf('--domain');
const descIdx = args.indexOf('--desc');

if (nameIdx >= 0 || domainIdx >= 0) {
    const config = {
        name: nameIdx >= 0 ? args[nameIdx + 1] : 'Godel',
        domain: domainIdx >= 0 ? args[domainIdx + 1] : 'general',
        domain_description: descIdx >= 0 ? args[descIdx + 1] : '',
    };
    const template = loadTemplate();
    writeOutput(fillTemplate(template, config));
    process.exit(0);
}

// Interactive mode
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const q = (prompt) => new Promise(resolve => rl.question(prompt, resolve));

(async () => {
    console.log('\n=== Godel Setup — Configure the inverted oracle ===\n');

    const examples = listExamples();
    if (examples.length > 0) {
        console.log(`Pre-built examples available: ${examples.join(', ')}`);
        const useExample = await q('Use an example? (name or Enter to skip): ');
        if (useExample && examples.includes(useExample)) {
            const config = loadExample(useExample);
            const template = loadTemplate();
            writeOutput(fillTemplate(template, config));
            rl.close();
            return;
        }
    }

    const name = (await q('Oracle name (default: Godel): ')).trim() || 'Godel';
    const domain = (await q('Domain (e.g., "sales strategy", "pharmaceutical R&D"): ')).trim() || 'general';
    const desc = (await q('Domain description (2-3 sentences about what you do): ')).trim();

    const tensions = [];
    console.log('\nEnter typical tensions in your domain (empty line to finish):');
    console.log('  Example: "We have two pricing strategies. Data says A, gut says B."');
    while (true) {
        const t = (await q('  > ')).trim();
        if (!t) break;
        tensions.push(`- ${t}`);
    }

    const sources = [];
    console.log('\nKnowledge sources — paths to files your oracle should read (empty to skip):');
    while (true) {
        const s = (await q('  path> ')).trim();
        if (!s) break;
        sources.push(`- \`${s}\``);
    }

    const config = {
        name,
        domain,
        domain_description: desc || `Configured for ${domain}. Add details about your specific context, constraints, and goals here.`,
        typical_tensions: tensions.length ? tensions.join('\n') : `- (Add your domain-specific tensions here)`,
        knowledge_sources: sources.length ? sources.join('\n') : `- (Add paths to your domain knowledge files here)`,
    };

    const template = loadTemplate();
    writeOutput(fillTemplate(template, config));

    // Save config for reference
    const configFile = path.join(DATA_DIR, 'setup_config.json');
    fs.writeFileSync(configFile, JSON.stringify(config, null, 2));
    console.log(`Config saved to: ${configFile}`);

    rl.close();
})();
