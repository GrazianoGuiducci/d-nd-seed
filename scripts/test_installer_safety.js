#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const nodeBin = process.execPath;
const tests = [];

function test(name, fn) {
  tests.push({ name, fn });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function runNode(args, opts = {}) {
  const result = spawnSync(nodeBin, args, {
    cwd: root,
    encoding: 'utf8',
    ...opts
  });
  return {
    status: result.status,
    stdout: result.stdout || '',
    stderr: result.stderr || '',
    error: result.error
  };
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function listTree(dir) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  const walk = current => {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const full = path.join(current, entry.name);
      const rel = path.relative(dir, full).replace(/\\/g, '/');
      out.push(rel + (entry.isDirectory() ? '/' : ''));
      if (entry.isDirectory()) walk(full);
    }
  };
  walk(dir);
  return out.sort();
}

function baseProfile(projectDir) {
  return {
    node_id: 'TEST_NODE',
    description: 'Temporary installer safety fixture',
    project_dir: projectDir,
    agent_runtime: 'codex',
    install_mode: 'recommended',
    risk_tolerance: 'writes_files',
    intent: ['coding'],
    repos: [
      { name: 'fixture', path: '.', branch: 'main' }
    ]
  };
}

test('registry strict coverage validates', () => {
  const result = runNode(['scripts/validate_capability_registry.js', '--strict-coverage']);
  assert(result.status === 0, result.stdout + result.stderr);
  assert(result.stdout.includes('OK:'), 'registry validator did not report OK');
});

test('seed_plan emits clean JSON', () => {
  const result = runNode(['scripts/seed_plan.js', 'profiles/example-codex.json', '--json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const data = JSON.parse(result.stdout);
  assert(Array.isArray(data.included), 'plan JSON missing included array');
  assert(data.context.agent === 'codex', 'plan JSON did not preserve codex runtime');
});

test('seed_plan emits included paths only', () => {
  const result = runNode(['scripts/seed_plan.js', 'profiles/example-claude-code.json', '--paths']);
  assert(result.status === 0, result.stdout + result.stderr);
  const lines = result.stdout.trim().split(/\r?\n/).filter(Boolean);
  assert(lines.length > 0, 'paths output is empty');
  assert(lines.every(line => !line.includes('D-ND Seed')), 'paths output contains prose');
});

test('seed_plan is read-only against fixture target', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-plan-'));
  const target = path.join(tempRoot, 'target');
  fs.mkdirSync(target, { recursive: true });
  fs.writeFileSync(path.join(target, 'marker.txt'), 'marker\n');
  const profilePath = path.join(tempRoot, 'profile.json');
  writeJson(profilePath, baseProfile(target));

  const before = JSON.stringify(listTree(target));
  const result = runNode(['scripts/seed_plan.js', profilePath, '--target-policy=dry-run']);
  const after = JSON.stringify(listTree(target));

  assert(result.status === 0, result.stdout + result.stderr);
  assert(before === after, 'seed_plan changed the fixture target tree');
});

test('validate_profile rejects placeholder path in write mode', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'placeholder.json');
  writeJson(profilePath, baseProfile('/path/to/your/project'));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'placeholder path was accepted in write mode');
  assert((result.stderr + result.stdout).includes('placeholder'), 'missing placeholder rejection message');
});

test('validate_profile rejects shell-control characters', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'shell-control.json');
  const profile = baseProfile(path.join(tempRoot, 'target'));
  profile.node_id = 'BAD;NODE';
  writeJson(profilePath, profile);

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=read-only']);
  assert(result.status !== 0, 'shell-control profile was accepted');
  assert((result.stderr + result.stdout).includes('shell-control'), 'missing shell-control rejection message');
});

test('validate_profile rejects parent traversal', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'traversal.json');
  writeJson(profilePath, baseProfile('../outside'));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'parent traversal was accepted');
  assert((result.stderr + result.stdout).includes('escapes upward'), 'missing traversal rejection message');
});

test('validate_profile rejects seed repo target in write mode', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'seed-target.json');
  writeJson(profilePath, baseProfile(root));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'seed repository target was accepted');
  assert((result.stderr + result.stdout).includes('seed repository'), 'missing seed target rejection message');
});

test('install/update/high-risk hooks contain no shell eval statements', () => {
  const files = [
    'install.sh',
    'update.sh',
    ...fs.readdirSync(path.join(root, 'templates', 'hooks'))
      .filter(name => name.endsWith('.tmpl'))
      .map(name => path.join('templates', 'hooks', name))
  ];
  const offenders = [];
  for (const rel of files) {
    const content = fs.readFileSync(path.join(root, rel), 'utf8');
    if (/^\s*eval\b/m.test(content)) offenders.push(rel);
  }
  assert(offenders.length === 0, `eval statements found in: ${offenders.join(', ')}`);
});

test('dry-run messaging cannot claim completed install', () => {
  const install = fs.readFileSync(path.join(root, 'install.sh'), 'utf8');
  assert(install.includes('=== Seed dry-run complete'), 'install dry-run completion message missing');
  assert(install.includes('No target files were written.'), 'install dry-run non-write message missing');
  assert(install.includes('Would save neutral Seed manifest'), 'install dry-run neutral manifest message missing');
});

test('update dry-run does not write update plan', () => {
  const update = fs.readFileSync(path.join(root, 'update.sh'), 'utf8');
  assert(update.includes('[DRY-RUN] Would save update plan'), 'update dry-run plan message missing');
  assert(update.includes('[DRY-RUN] Would save neutral update plan'), 'update dry-run neutral plan message missing');
  assert(/else\s*\n\s*mkdir -p "\$CLAUDE_TARGET" "\$NEUTRAL_TARGET"\s*\n\s*node "\$SEED_DIR\/scripts\/installer_option_router\.js" "\$PROFILE" --json > "\$CLAUDE_TARGET\/seed_update_plan\.json"\s*\n\s*cp "\$CLAUDE_TARGET\/seed_update_plan\.json" "\$NEUTRAL_TARGET\/seed_update_plan\.json"/.test(update), 'update plan writes are not confined to non-dry-run branch');
  assert(update.includes('NEUTRAL_PROFILE="$NEUTRAL_TARGET/seed_profile.json"'), 'update is missing neutral profile path');
  assert(update.includes('if [ -f "$NEUTRAL_PROFILE" ]; then'), 'update does not prefer neutral profile when available');
});

let failed = 0;
for (const { name, fn } of tests) {
  try {
    fn();
    console.log(`ok - ${name}`);
  } catch (err) {
    failed += 1;
    console.error(`not ok - ${name}`);
    console.error(`  ${err.message}`);
  }
}

console.log('');
console.log(`${tests.length - failed}/${tests.length} installer safety tests passed`);
if (failed) process.exit(1);
