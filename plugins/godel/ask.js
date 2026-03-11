/**
 * ask.js — Helper to query the Godel bridge
 *
 * CLI:   node ask.js "your tension here"
 * Module: const ask = require('./ask'); const r = await ask('tension');
 */

const http = require('http');

const PORT = parseInt(process.env.GODEL_PORT || '3004', 10);

function ask(question, context = null, mode = null) {
    return new Promise((resolve, reject) => {
        const body = { question, context };
        if (mode) body.mode = mode;
        const payload = JSON.stringify(body);

        const req = http.request({
            hostname: '127.0.0.1',
            port: PORT,
            path: '/ask',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload),
            },
            timeout: 5 * 60 * 1000,
        }, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    if (res.statusCode === 200) {
                        resolve({
                            answer: parsed.answer || '',
                            meta: parsed.meta || null,
                            elapsed: parsed.elapsed,
                        });
                    } else {
                        reject(new Error(parsed.error || 'Bridge error'));
                    }
                } catch (e) {
                    reject(new Error('Unparseable response'));
                }
            });
        });

        req.on('error', reject);
        req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
        req.write(payload);
        req.end();
    });
}

if (require.main === module) {
    const question = process.argv.slice(2).join(' ');
    if (!question) {
        console.error('Usage: node ask.js "your question"');
        process.exit(1);
    }
    ask(question).then(r => {
        console.log(r.answer);
        if (r.meta) console.log('\n[Meta]', JSON.stringify(r.meta));
    }).catch(e => {
        console.error('Error:', e.message);
        process.exit(1);
    });
}

module.exports = ask;
