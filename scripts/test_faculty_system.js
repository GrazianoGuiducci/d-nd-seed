#!/usr/bin/env node
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { defaultRegistryPath, readJson, validateRegistry } = require('./validate_faculty_registry');

const root = path.resolve(__dirname, '..');
let passed = 0;

function test(name, fn) {
  try {
    fn();
    passed += 1;
    console.log(`PASS: ${name}`);
  } catch (error) {
    console.error(`FAIL: ${name}`);
    throw error;
  }
}

function run(args) {
  return spawnSync(process.execPath, args, { cwd: root, encoding: 'utf8' });
}

const registry = readJson(defaultRegistryPath);

test('registry validates and covers the declared inventory', () => {
  const result = validateRegistry(registry);
  assert.deepStrictEqual(result.errors, []);
  assert.strictEqual(result.count, 43);
  assert.strictEqual(result.resultContractCount, 43);
});

test('all public ids are unique and every bundle is populated', () => {
  const ids = registry.faculties.map(faculty => faculty.id);
  assert.strictEqual(new Set(ids).size, ids.length);
  Object.keys(registry.bundle_definitions).forEach(bundle => {
    assert(registry.faculties.some(faculty => faculty.bundles.includes(bundle)), bundle);
  });
});

test('catalog excludes private identity maps and absolute workspace paths', () => {
  const text = fs.readFileSync(defaultRegistryPath, 'utf8');
  assert(!/[A-Za-z]:\\/.test(text));
  assert(!text.includes('/opt/'));
  assert.strictEqual(registry.source_inventory.internal_identity_map_included, false);
  assert.strictEqual(registry.source_inventory.evidence_status, 'maintainer_attested');
  assert.strictEqual(registry.source_inventory.publicly_reproducible, false);
});

test('privacy validation rejects cross-platform private path forms', () => {
  for (const privatePath of [
    'C:\\PVSC\\ANTI_G\\private',
    'C:/PVSC/ANTI_G/private',
    '\\\\server\\share\\private',
    '/home/operator/private',
    '/Users/operator/private'
  ]) {
    const candidate = JSON.parse(JSON.stringify(registry));
    candidate.scope = privatePath;
    const result = validateRegistry(candidate);
    assert(result.errors.some(error => error.includes('private residue matched')), privatePath);
  }
});

test('public-neutral policy invariants are enforced', () => {
  const mutations = [
    ['private_adapter_code_included', true],
    ['source_runtime_state_included', true],
    ['effect_review_required', false],
    ['contract_license', 'AGPL-3.0']
  ];
  for (const [key, value] of mutations) {
    const candidate = JSON.parse(JSON.stringify(registry));
    candidate.policy[key] = value;
    assert(validateRegistry(candidate).errors.length > 0, key);
  }
});

test('malformed faculty data returns errors instead of crashing', () => {
  const candidate = JSON.parse(JSON.stringify(registry));
  delete candidate.faculties[0].bundles;
  const result = validateRegistry(candidate);
  assert(result.errors.some(error => error.includes('bundles are required')));
});

test('bundle planning is read-only and machine-readable', () => {
  const result = run(['scripts/faculty_plan.js', '--bundle=software', '--json']);
  assert.strictEqual(result.status, 0, result.stderr);
  const plan = JSON.parse(result.stdout);
  assert(plan.selection_count > 0);
  assert(plan.selected.every(faculty => typeof faculty.result_contract === 'string'));
  assert.strictEqual(plan.activates_faculties, false);
  assert.strictEqual(plan.writes_files, false);
});

test('list output exposes public functions and result contracts', () => {
  const result = run(['scripts/faculty_plan.js', '--list', '--json']);
  assert.strictEqual(result.status, 0, result.stderr);
  const list = JSON.parse(result.stdout);
  assert(list.faculties.every(faculty => faculty.public_function && faculty.result_contract));
});

test('candidate router is opt-in and has no false runtime dependencies', () => {
  const capabilityRegistry = JSON.parse(fs.readFileSync(path.join(root, 'capabilities', 'registry.json'), 'utf8'));
  const router = capabilityRegistry.capabilities.find(capability => capability.id === 'faculty-router');
  assert(router);
  assert.strictEqual(router.stratum, 'recent_candidate');
  assert.strictEqual(router.visibility, 'optional');
  assert.deepStrictEqual(router.requires, []);
  const result = run(['scripts/installer_option_router.js', 'profiles/example.json', '--json']);
  assert.strictEqual(result.status, 0, result.stderr);
  const plan = JSON.parse(result.stdout);
  assert(!plan.included.some(capability => capability.id === 'faculty-router'));
  assert(plan.available.some(capability => capability.id === 'faculty-router'));
});

test('explicit faculty planning rejects unknown ids', () => {
  const result = run(['scripts/faculty_plan.js', '--faculty=not-a-faculty', '--json']);
  assert.notStrictEqual(result.status, 0);
  assert(result.stderr.includes('Unknown faculty'));
});

test('installed router points to the bundled registry', () => {
  const skillPath = path.join(root, 'plugins', 'd-nd-core', 'skills', 'faculty-router', 'SKILL.md');
  const skill = fs.readFileSync(skillPath, 'utf8');
  assert(skill.includes('name: faculty-router'));
  assert(skill.includes('references/faculty-registry.json'));
});

console.log(`OK: ${passed} faculty system tests passed`);
