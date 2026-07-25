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

function findBash() {
  const candidates = process.platform === 'win32'
    ? ['C:\\Program Files\\Git\\bin\\bash.exe', 'bash.exe']
    : ['bash'];
  for (const candidate of candidates) {
    const probe = spawnSync(candidate, ['--version'], { encoding: 'utf8' });
    if (!probe.error && probe.status === 0) return candidate;
  }
  return null;
}

function bashPath(value) {
  return process.platform === 'win32' ? value.replace(/\\/g, '/') : value;
}

function runBash(script, args = []) {
  const bash = findBash();
  if (!bash) return null;
  const result = spawnSync(bash, [bashPath(path.join(root, script)), ...args.map(bashPath)], {
    cwd: root,
    encoding: 'utf8',
    env: { ...process.env, DND_SEED_ALLOW_WINDOWS_BASH: '1' }
  });
  return { status: result.status, stdout: result.stdout || '', stderr: result.stderr || '', error: result.error };
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
  assert((result.stderr + result.stdout).includes('parent traversal'), 'missing traversal rejection message');
});

test('validate_profile rejects seed repo target in write mode', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'seed-target.json');
  writeJson(profilePath, baseProfile(root));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'seed repository target was accepted');
  assert((result.stderr + result.stdout).includes('seed repository'), 'missing seed target rejection message');
});

test('validate_profile resolves relative targets exactly like installer cwd', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-'));
  const profilePath = path.join(tempRoot, 'cwd-target.json');
  writeJson(profilePath, baseProfile('profiles'));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'relative target inside Seed was accepted');
  assert((result.stderr + result.stdout).includes('descendants'), 'cwd-resolved containment error missing');
});

test('validate_profile binds the effective updater target to profile project_dir', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-bind-'));
  const profileTarget = path.join(tempRoot, 'declared');
  const effectiveTarget = path.join(tempRoot, 'effective');
  const profilePath = path.join(tempRoot, 'profile.json');
  writeJson(profilePath, baseProfile(profileTarget));

  const result = runNode([
    'scripts/validate_profile.js',
    profilePath,
    '--target-policy=write',
    `--effective-project-dir=${effectiveTarget}`
  ]);
  assert(result.status !== 0, 'mismatched effective updater target was accepted');
  assert((result.stderr + result.stdout).includes('does not match profile project_dir'), 'target-binding error missing');
});

test('validate_profile rejects a symlink or junction resolving into Seed', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-link-'));
  const link = path.join(tempRoot, 'seed-link');
  fs.symlinkSync(root, link, process.platform === 'win32' ? 'junction' : 'dir');
  const profilePath = path.join(tempRoot, 'linked-target.json');
  writeJson(profilePath, baseProfile(link));

  const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=write']);
  assert(result.status !== 0, 'linked target inside Seed was accepted');
  assert((result.stderr + result.stdout).includes('descendants'), 'canonical containment error missing');
});

test('target-only validation rejects a symlink or junction resolving into Seed', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-target-link-'));
  const link = path.join(tempRoot, 'seed-link');
  fs.symlinkSync(root, link, process.platform === 'win32' ? 'junction' : 'dir');
  const result = runNode(['scripts/validate_profile.js', `--target-only=${link}`, '--target-policy=write']);
  assert(result.status !== 0, 'target-only validator accepted a linked Seed target');
  assert((result.stderr + result.stdout).includes('descendants'), 'target-only containment error missing');
});

test('registry validation rejects source paths outside Seed', () => {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-registry-'));
  const registry = JSON.parse(fs.readFileSync(path.join(root, 'capabilities', 'registry.json'), 'utf8'));
  registry.capabilities[0].path = '../outside-seed';
  const registryPath = path.join(tempRoot, 'registry.json');
  writeJson(registryPath, registry);

  const result = runNode(['scripts/validate_capability_registry.js', `--registry=${registryPath}`]);
  assert(result.status !== 0, 'escaping registry source path was accepted');
  assert((result.stderr + result.stdout).includes('escapes the seed repository'), 'source containment error missing');
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

test('plan-only profiles cannot invoke installer or updater writers', () => {
  const install = fs.readFileSync(path.join(root, 'install.sh'), 'utf8');
  const update = fs.readFileSync(path.join(root, 'update.sh'), 'utf8');
  assert(install.includes('Profile write_policy is plan_only.'), 'installer plan-only guard missing');
  assert(install.includes('this profile cannot invoke installer writers'), 'installer guard message missing');
  assert(update.includes('Saved profile write_policy is plan_only.'), 'updater plan-only guard missing');
  assert(update.includes('this profile cannot invoke updater writers'), 'updater guard message missing');
  const policyGuard = update.indexOf('WRITE_POLICY=$(node -e');
  const legacyBranch = update.indexOf('INCLUDED_PATHS_FILE=""');
  assert(policyGuard >= 0 && policyGuard < legacyBranch, 'updater policy guard can be bypassed by --legacy-all');
  const writeValidation = runNode(['scripts/validate_profile.js', 'profiles/example-opencode.json', '--target-policy=write']);
  assert(writeValidation.status !== 0, 'plan-only OpenCode profile validated for writing');
});

test('updater preserves untracked and provenance-unknown existing files', () => {
  const update = fs.readFileSync(path.join(root, 'update.sh'), 'utf8');
  assert(update.includes('ls-files --error-unmatch'), 'untracked hook protection missing');
  assert(update.includes('diff --cached --quiet'), 'staged hook protection missing');
  assert(update.includes('scenario_projector.py.new'), 'projector review copy missing');
  assert(update.includes('examples/$fname.new'), 'example review copy missing');
});

test('installer permission pass tolerates an empty hook selection', () => {
  const install = fs.readFileSync(path.join(root, 'install.sh'), 'utf8');
  assert(install.includes('for hook in "$TARGET/hooks/"*.sh; do'), 'safe hook permission loop missing');
  assert(install.includes('[ -f "$hook" ] || continue'), 'empty hook glob is not guarded');
});

test('Bash installer completes when the selected plan contains no hooks', () => {
  if (!findBash()) return;
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-no-hooks-'));
  const target = path.join(tempRoot, 'target');
  const profilePath = path.join(tempRoot, 'profile.json');
  const profile = baseProfile(bashPath(target));
  profile.agent_runtime = 'generic';
  profile.install_mode = 'minimal';
  profile.risk_tolerance = 'safe';
  profile.capability_allowlist = ['assertion-verifier'];
  profile.write_policy = 'target_write';
  writeJson(profilePath, profile);

  const result = runBash('install.sh', [profilePath]);
  assert(result && result.status === 0, (result?.stdout || '') + (result?.stderr || ''));
  assert(fs.existsSync(path.join(target, '.seed', 'seed_profile.json')), 'neutral profile was not installed');
});

test('Bash install and update use provenance-aware skill reconciliation', () => {
  if (!findBash()) return;
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-skill-integration-'));
  const target = path.join(tempRoot, 'target');
  const profilePath = path.join(tempRoot, 'profile.json');
  const profile = baseProfile(bashPath(target));
  profile.agent_runtime = 'generic';
  profile.risk_tolerance = 'safe';
  profile.capability_allowlist = ['faculty-router'];
  profile.write_policy = 'target_write';
  writeJson(profilePath, profile);

  const installResult = runBash('install.sh', [profilePath]);
  assert(installResult && installResult.status === 0, (installResult?.stdout || '') + (installResult?.stderr || ''));
  const skill = path.join(target, '.claude', 'skills', 'faculty-router');
  const statePath = path.join(target, '.seed', 'seed_skill_state.json');
  assert(fs.existsSync(path.join(skill, 'SKILL.md')), 'selected skill was not installed');
  assert(fs.existsSync(statePath), 'skill provenance state was not installed');
  const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  assert(state.capabilities['faculty-router'], 'faculty-router provenance is missing');

  fs.appendFileSync(path.join(skill, 'SKILL.md'), '\nlocal fixture customization\n');
  const customized = fs.readFileSync(path.join(skill, 'SKILL.md'), 'utf8');
  const updateResult = runBash('update.sh', [target]);
  assert(updateResult && updateResult.status === 0, (updateResult?.stdout || '') + (updateResult?.stderr || ''));
  assert((updateResult.stdout + updateResult.stderr).includes('locally_modified -> staged_for_review'), 'local modification was not classified for review');
  assert(fs.readFileSync(path.join(skill, 'SKILL.md'), 'utf8') === customized, 'updater overwrote a locally modified skill');
  const updatedState = JSON.parse(fs.readFileSync(statePath, 'utf8'));
  const pending = updatedState.pending['faculty-router'];
  assert(pending && fs.existsSync(path.join(target, pending.staged_path)), 'review tree was not staged');
});

test('Bash updater cannot bypass a saved plan-only profile with legacy-all', () => {
  if (!findBash()) return;
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-update-policy-'));
  const target = path.join(tempRoot, 'target');
  fs.mkdirSync(path.join(target, '.seed'), { recursive: true });
  fs.writeFileSync(path.join(target, 'marker.txt'), 'preserve\n');
  const profile = JSON.parse(fs.readFileSync(path.join(root, 'profiles', 'example-opencode.json'), 'utf8'));
  profile.project_dir = bashPath(target);
  writeJson(path.join(target, '.seed', 'seed_profile.json'), profile);
  const before = JSON.stringify(listTree(target));

  const result = runBash('update.sh', [target, '--legacy-all']);
  const after = JSON.stringify(listTree(target));
  assert(result && result.status !== 0, 'legacy-all bypassed plan-only policy');
  assert((result.stdout + result.stderr).includes('write_policy is plan_only'), 'plan-only rejection was not explicit');
  assert(before === after, 'updater changed the target before rejecting plan-only policy');
});

test('Bash updater rejects a CLI target that differs from the saved profile target', () => {
  if (!findBash()) return;
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-update-bind-'));
  const declared = path.join(tempRoot, 'declared');
  const effective = path.join(tempRoot, 'effective');
  fs.mkdirSync(path.join(effective, '.seed'), { recursive: true });
  fs.writeFileSync(path.join(effective, 'marker.txt'), 'preserve\n');
  const profile = baseProfile(bashPath(declared));
  profile.capability_allowlist = ['assertion-verifier'];
  profile.write_policy = 'target_write';
  writeJson(path.join(effective, '.seed', 'seed_profile.json'), profile);
  const before = JSON.stringify(listTree(effective));

  const result = runBash('update.sh', [effective, '--legacy-all']);
  const after = JSON.stringify(listTree(effective));
  assert(result && result.status !== 0, 'updater accepted a CLI/profile target mismatch');
  assert((result.stdout + result.stderr).includes('does not match profile project_dir'), 'updater target-binding error missing');
  assert(before === after, 'updater changed the mismatched target before rejection');
});

test('Bash updater rejects a legacy-all target resolving into Seed before profile lookup', () => {
  if (!findBash()) return;
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-update-link-'));
  const link = path.join(tempRoot, 'seed-link');
  fs.symlinkSync(root, link, process.platform === 'win32' ? 'junction' : 'dir');
  const result = runBash('update.sh', [link, '--legacy-all']);
  assert(result && result.status !== 0, 'legacy-all accepted a target resolving into Seed');
  assert((result.stdout + result.stderr).includes('descendants'), 'legacy target containment error missing');
});

test('update dry-run does not write update plan', () => {
  const update = fs.readFileSync(path.join(root, 'update.sh'), 'utf8');
  assert(update.includes('[DRY-RUN] Would save update plan'), 'update dry-run plan message missing');
  assert(update.includes('[DRY-RUN] Would save neutral update plan'), 'update dry-run neutral plan message missing');
  assert(update.includes('node "$SEED_DIR/scripts/installer_option_router.js" "$PROFILE" --json > "$PLAN_FILE"'), 'temporary update plan generation missing');
  assert(/else\s*\n\s*mkdir -p "\$CLAUDE_TARGET" "\$NEUTRAL_TARGET"\s*\n\s*cp "\$PLAN_FILE" "\$CLAUDE_TARGET\/seed_update_plan\.json"\s*\n\s*cp "\$CLAUDE_TARGET\/seed_update_plan\.json" "\$NEUTRAL_TARGET\/seed_update_plan\.json"/.test(update), 'update plan writes are not confined to non-dry-run branch');
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
