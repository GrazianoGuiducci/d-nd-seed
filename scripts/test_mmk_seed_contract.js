#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const tests = [];

function test(name, fn) {
  tests.push({ name, fn });
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function runNode(args) {
  const result = spawnSync(process.execPath, args, { cwd: root, encoding: 'utf8' });
  return { status: result.status, stdout: result.stdout || '', stderr: result.stderr || '' };
}

function writeJson(file, value) {
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
}

function openCodeProfile() {
  return JSON.parse(fs.readFileSync(path.join(root, 'profiles', 'example-opencode.json'), 'utf8'));
}

function attestation(overrides = {}) {
  return {
    schema: 'mmk.session-capability-attestation.v0.1',
    attestation_id: 'TEST-OPEN-CODE-SESSION',
    session_id: 'TEST-SESSION',
    host_id: 'OPENCODE',
    owner_surface: 'temporary-test-fixture',
    observed_at: new Date().toISOString(),
    runtime: 'opencode',
    ephemeral: true,
    grants_authority: false,
    capabilities: [],
    ...overrides
  };
}

function runEnvironmentPlan(profile, evidence) {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-mmk-'));
  const profilePath = path.join(temp, 'profile.json');
  const attestationPath = path.join(temp, 'attestation.json');
  writeJson(profilePath, profile);
  writeJson(attestationPath, evidence);
  return runNode(['scripts/mmk_seed_plan.js', profilePath, '--level=environment-selected', `--session-attestation=${attestationPath}`]);
}

test('MMK Seed compatibility contract validates exact registry coverage', () => {
  const result = runNode(['scripts/validate_mmk_seed_contract.js']);
  assert(result.status === 0, result.stdout + result.stderr);
  assert(result.stdout.includes('65/65 classified'), 'validator did not prove 65/65 coverage');
});

test('dedicated OpenCode profile validates in read-only mode', () => {
  const result = runNode(['scripts/validate_profile.js', 'profiles/example-opencode.json', '--target-policy=read-only', '--json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const profile = JSON.parse(result.stdout);
  assert(profile.agent_runtime === 'opencode', 'profile runtime is not OpenCode');
  assert(profile.mmk_selection_level === 'system', 'profile is not system-minimal');
  assert(profile.write_policy === 'plan_only', 'profile is not plan-only');
});

test('legacy Seed planner honors the explicit OpenCode allowlist', () => {
  const result = runNode(['scripts/seed_plan.js', 'profiles/example-opencode.json', '--json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  const ids = plan.included.map(item => item.id).sort();
  assert(JSON.stringify(ids) === JSON.stringify(['assertion-verifier', 'evolution-transfer-protocol']), `unexpected allowlist plan: ${ids.join(', ')}`);
});

test('MMK system plan stays plan-only without session attestation', () => {
  const result = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  assert(plan.boundary === 'plan_only_no_activation', 'plan boundary widened');
  assert(plan.session_attestation === null, 'unexpected session attestation');
  assert(plan.selected.length === 2, 'system bundle is not minimal');
  assert(plan.selected.every(item => item.host_compatibility.state === 'session_attestation_required'), 'missing attestation was inferred');
  assert(plan.selected.every(item => item.activation_allowed === false), 'plan granted activation');
});

test('selection levels are cumulative and independent from legacy allowlist filtering', () => {
  const defaultResult = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json', '--level=default']);
  assert(defaultResult.status === 0, defaultResult.stdout + defaultResult.stderr);
  const defaultIds = JSON.parse(defaultResult.stdout).selected.map(item => item.id);
  assert(JSON.stringify(defaultIds) === JSON.stringify(['assertion-verifier', 'evolution-transfer-protocol', 'eval']), `default layer is not 2+1: ${defaultIds.join(', ')}`);

  const systemResult = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-codex.json', '--level=system']);
  assert(systemResult.status === 0, systemResult.stdout + systemResult.stderr);
  assert(JSON.parse(systemResult.stdout).selected.length === 2, 'system bundle was erased by a missing allowlist');
});

test('environment-selected level blocks without current evidence', () => {
  const result = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json', '--level=environment-selected']);
  assert(result.status !== 0, 'environment-selected plan succeeded without attestation');
  assert((result.stdout + result.stderr).includes('requires profile-bound ephemeral host evidence'), 'missing evidence error not reported');
});

test('profile-bound evidence refreshes planning only and levels remain cumulative', () => {
  const profile = openCodeProfile();
  profile.mmk_selection_level = 'environment-selected';
  profile.capability_allowlist = ['diagram-generator'];
  const evidence = attestation({
    capabilities: [{
      capability_id: 'diagram-generator',
      exposed: true,
      access_state: 'verified',
      operational_path_state: 'verified',
      evidence: 'temporary test fixture only'
    }]
  });
  const result = runEnvironmentPlan(profile, evidence);
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  const ids = plan.selected.map(item => item.id);
  assert(ids.includes('eval') && ids.includes('diagram-generator') && ids.length === 4, `environment layer is not cumulative: ${ids.join(', ')}`);
  const diagram = plan.selected.find(item => item.id === 'diagram-generator');
  assert(diagram.host_compatibility.state === 'profile_bound_evidence_for_planning', 'evidence was not mapped to planning');
  assert(diagram.host_compatibility.verification_scope.includes('mmk_session_validation_external'), 'Seed claimed MMK session validation');
  assert(plan.session_attestation.mmk_session_validation_required === true, 'external MMK validation gate missing');
  assert(diagram.activation_allowed === false, 'evidence granted activation');
});

test('invalid, stale, unbound or authority-bearing evidence is rejected', () => {
  const profile = openCodeProfile();
  profile.mmk_selection_level = 'environment-selected';
  profile.capability_allowlist = ['diagram-generator'];
  const capability = {
    capability_id: 'diagram-generator',
    exposed: true,
    access_state: 'verified',
    operational_path_state: 'verified',
    evidence: 'test'
  };
  const cases = [
    ['stale', attestation({ observed_at: new Date(Date.now() - 3600_000).toISOString() })],
    ['unparseable time', attestation({ observed_at: 'not-a-time' })],
    ['future time', attestation({ observed_at: new Date(Date.now() + 3600_000).toISOString() })],
    ['missing runtime', (() => { const value = attestation(); delete value.runtime; return value; })()],
    ['wrong host', attestation({ host_id: 'OTHER-HOST' })],
    ['duplicate capability', attestation({ capabilities: [capability, { ...capability }] })],
    ['authority field', attestation({ capabilities: [{ ...capability, authority_state: 'granted' }] })],
    ['inconsistent exposure', attestation({ capabilities: [{ ...capability, exposed: false }] })]
  ];
  for (const [name, evidence] of cases) {
    const result = runEnvironmentPlan(profile, evidence);
    assert(result.status !== 0, `${name} evidence was accepted`);
  }
});

test('selection hash binds profile and compatibility contract content, not profile path', () => {
  const originalResult = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json']);
  assert(originalResult.status === 0, originalResult.stdout + originalResult.stderr);
  const original = JSON.parse(originalResult.stdout);
  assert(original.profile_sha256, 'profile hash missing');
  assert(original.compatibility_contract?.sha256, 'compatibility contract hash missing');

  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-profile-hash-'));
  const copiedPath = path.join(temp, 'copied-profile.json');
  fs.copyFileSync(path.join(root, 'profiles', 'example-opencode.json'), copiedPath);
  const copiedResult = runNode(['scripts/mmk_seed_plan.js', copiedPath]);
  assert(copiedResult.status === 0, copiedResult.stdout + copiedResult.stderr);
  const copied = JSON.parse(copiedResult.stdout);
  assert(copied.selection_sha256 === original.selection_sha256, 'profile path changed the selection hash');

  const changedProfile = openCodeProfile();
  changedProfile.description += ' changed';
  writeJson(copiedPath, changedProfile);
  const changedResult = runNode(['scripts/mmk_seed_plan.js', copiedPath]);
  assert(changedResult.status === 0, changedResult.stdout + changedResult.stderr);
  assert(JSON.parse(changedResult.stdout).selection_sha256 !== original.selection_sha256, 'profile content did not change selection hash');
});

test('missing dependencies are reported and never added implicitly', () => {
  const profile = openCodeProfile();
  profile.mmk_selection_level = 'environment-selected';
  profile.capability_allowlist = ['continuity-boundary'];
  const result = runEnvironmentPlan(profile, attestation());
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  assert(!plan.selected.some(item => item.id === 'context-awareness'), 'dependency was added implicitly');
  assert(plan.unresolved_dependencies.some(item => item.capability_id === 'continuity-boundary' && item.dependency === 'context-awareness'), 'missing dependency was not reported');
  const item = plan.selected.find(entry => entry.id === 'continuity-boundary');
  assert(item.required_gates.includes('explicit_dependency_selection_required'), 'dependency gate missing');
});

test('registry risk remains a hint and every capability requires effect review', () => {
  const result = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  for (const item of plan.selected) {
    assert(item.side_effect_class === 'unknown_until_capability_effect_review', 'registry risk was promoted to effect proof');
    assert(item.required_gates.includes('capability_effect_review_required'), 'effect review gate missing');
    assert(Array.isArray(item.required_gates) && item.required_gates.length > 1, 'gates were not composed');
  }
});

test('license boundary remains explicit and unresolved per capability', () => {
  const result = runNode(['scripts/mmk_seed_plan.js', 'profiles/example-opencode.json']);
  assert(result.status === 0, result.stdout + result.stderr);
  const plan = JSON.parse(result.stdout);
  for (const item of plan.selected) {
    assert(item.repo_license === 'AGPL-3.0', 'repository license declaration missing');
    assert(item.capability_license === 'unknown', 'capability license was invented');
    assert(item.capability_license_status === 'not_declared_per_capability', 'capability license status missing');
    assert(item.compatibility_gate === 'review_required_before_copy_or_embedding', 'license gate missing');
  }
});

test('OpenCode profile is model-agnostic and has no implicit effects', () => {
  const profile = openCodeProfile();
  assert(!('model' in profile) && !('model_id' in profile) && !('provider' in profile), 'profile contains model/provider default');
  assert(Object.values(profile.implicit_capabilities).every(value => value === false), 'profile contains implicit capability');
  assert(profile.write_policy === 'plan_only', 'profile is not plan-only');
});

test('every MMK profile requires external evidence policy and explicit no-implicit-effects', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-mmk-policy-'));
  const cases = [
    ['missing host policy', profile => { delete profile.host_capability_policy; }],
    ['self validation', profile => { profile.host_capability_policy.validation_owner = 'profile_self'; }],
    ['authority grant', profile => { profile.host_capability_policy.grants_authority = true; }],
    ['persistent evidence', profile => { profile.host_capability_policy.persists_attestation = true; }],
    ['permissive missing evidence', profile => { profile.host_capability_policy.on_missing = 'block'; }],
    ['implicit hooks', profile => { profile.implicit_capabilities.hooks = true; }],
    ['missing implicit declarations', profile => { delete profile.implicit_capabilities; }],
    ['empty MMK level', profile => { profile.mmk_selection_level = ''; profile.write_policy = 'target_write'; }],
    ['null MMK level', profile => { profile.mmk_selection_level = null; profile.write_policy = 'target_write'; }],
    ['numeric MMK level', profile => { profile.mmk_selection_level = 0; profile.write_policy = 'target_write'; }],
    ['unknown implicit effect', profile => { profile.implicit_capabilities.external_publish = true; }],
    ['unknown implicit declaration', profile => { profile.implicit_capabilities.future_effect = false; }],
    ['excessive evidence window', profile => { profile.host_capability_policy.max_age_seconds = 86400; }]
  ];
  for (const [name, mutate] of cases) {
    const profile = openCodeProfile();
    profile.mmk_selection_level = 'environment-selected';
    profile.capability_allowlist = ['diagram-generator'];
    mutate(profile);
    const profilePath = path.join(temp, `${name.replace(/\s+/g, '-')}.json`);
    writeJson(profilePath, profile);
    const result = runNode(['scripts/validate_profile.js', profilePath, '--target-policy=read-only']);
    assert(result.status !== 0, `${name} MMK profile was accepted`);
  }

  const noPolicy = openCodeProfile();
  noPolicy.mmk_selection_level = 'environment-selected';
  noPolicy.capability_allowlist = ['diagram-generator'];
  delete noPolicy.host_capability_policy;
  const stale = attestation({ observed_at: '2020-01-01T00:00:00Z' });
  const plannerResult = runEnvironmentPlan(noPolicy, stale);
  assert(plannerResult.status !== 0, 'planner bypassed the mandatory MMK policy with stale evidence');
});

test('unknown capability ids and MMK writer profiles are rejected', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-invalid-profile-'));
  const profile = openCodeProfile();
  profile.capability_allowlist.push('not-a-real-capability');
  const unknownPath = path.join(temp, 'unknown.json');
  writeJson(unknownPath, profile);
  const unknown = runNode(['scripts/validate_profile.js', unknownPath, '--target-policy=read-only']);
  assert(unknown.status !== 0 && (unknown.stdout + unknown.stderr).includes('unknown id'), 'unknown allowlist id was accepted');

  profile.capability_allowlist = ['assertion-verifier', 'evolution-transfer-protocol'];
  profile.write_policy = 'target_write';
  const writerPath = path.join(temp, 'writer.json');
  writeJson(writerPath, profile);
  const writer = runNode(['scripts/validate_profile.js', writerPath, '--target-policy=read-only']);
  assert(writer.status !== 0 && (writer.stdout + writer.stderr).includes('MMK selection profiles'), 'MMK writer profile was accepted');
});

let failed = 0;
for (const { name, fn } of tests) {
  try {
    fn();
    console.log(`ok - ${name}`);
  } catch (error) {
    failed += 1;
    console.error(`not ok - ${name}`);
    console.error(`  ${error.message}`);
  }
}

console.log('');
console.log(`${tests.length - failed}/${tests.length} MMK Seed contract tests passed`);
if (failed) process.exit(1);
