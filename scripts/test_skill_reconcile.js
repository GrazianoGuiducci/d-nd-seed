#!/usr/bin/env node
'use strict';

const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const {
  auditRemoved,
  hashTree,
  loadState,
  reconcileSkill,
  stateSchema
} = require('./skill_reconcile');

let passed = 0;

function test(name, fn) {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'dnd-seed-skill-reconcile-'));
  try {
    fn(makeFixture(tempRoot));
    passed += 1;
    console.log(`PASS: ${name}`);
  } catch (error) {
    console.error(`FAIL: ${name}`);
    throw error;
  } finally {
    fs.rmSync(tempRoot, { recursive: true, force: true });
  }
}

function write(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, value);
}

function makeFixture(tempRoot) {
  const seedRoot = path.join(tempRoot, 'seed');
  const projectRoot = path.join(tempRoot, 'project');
  const capabilityId = 'demo-skill';
  const source = path.join(seedRoot, 'plugins', 'd-nd-core', 'skills', capabilityId);
  const target = path.join(projectRoot, '.claude', 'skills', capabilityId);
  const statePath = path.join(projectRoot, '.seed', 'seed_skill_state.json');
  const planPath = path.join(tempRoot, 'plan.json');
  fs.mkdirSync(projectRoot, { recursive: true });
  write(path.join(seedRoot, 'capabilities', 'registry.json'), JSON.stringify({ version: 'test-v1' }));
  write(path.join(source, 'SKILL.md'), 'version one\n');
  write(path.join(source, 'references', 'obsolete.txt'), 'remove later\n');
  write(planPath, '{"selected":["demo-skill"]}\n');
  return {
    tempRoot,
    seedRoot,
    projectRoot,
    capabilityId,
    source,
    target,
    statePath,
    planPath,
    options(mode = 'plan') {
      return { seedRoot, projectRoot, capabilityId, source, target, statePath, planPath, mode };
    }
  };
}

test('dry-run classifies a new skill without writes', fixture => {
  const result = reconcileSkill(fixture.options('dry-run'));
  assert.strictEqual(result.classification, 'new');
  assert.strictEqual(result.action, 'would_install');
  assert.strictEqual(result.writes_files, false);
  assert(!fs.existsSync(fixture.target));
  assert(!fs.existsSync(fixture.statePath));
});

test('new install copies the full tree and records provenance', fixture => {
  const result = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(result.classification, 'new');
  assert.strictEqual(hashTree(fixture.source), hashTree(fixture.target));
  const state = loadState(fixture.statePath);
  assert.strictEqual(state.schema, stateSchema);
  const entry = state.capabilities[fixture.capabilityId];
  assert(entry);
  assert.strictEqual(entry.source_tree_sha256, hashTree(fixture.source));
  assert.strictEqual(entry.installed_tree_sha256, hashTree(fixture.target));
  assert.strictEqual(entry.registry_version, 'test-v1');
  assert(entry.plan_sha256);
  assert(!path.isAbsolute(entry.source_path));
  assert(!path.isAbsolute(entry.target_path));
});

test('unchanged baseline performs no write', fixture => {
  reconcileSkill(fixture.options('apply'));
  const before = fs.readFileSync(fixture.statePath, 'utf8');
  const result = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(result.classification, 'unchanged');
  assert.strictEqual(result.action, 'none');
  assert.strictEqual(result.writes_files, false);
  assert.strictEqual(fs.readFileSync(fixture.statePath, 'utf8'), before);
});

test('upstream change atomically replaces the whole unmodified tree', fixture => {
  reconcileSkill(fixture.options('apply'));
  fs.rmSync(path.join(fixture.source, 'references', 'obsolete.txt'));
  write(path.join(fixture.source, 'SKILL.md'), 'version two\n');
  write(path.join(fixture.source, 'references', 'new.txt'), 'new upstream file\n');
  const result = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(result.classification, 'upstream_changed');
  assert.strictEqual(result.action, 'replace_atomically');
  assert.strictEqual(hashTree(fixture.source), hashTree(fixture.target));
  assert(!fs.existsSync(path.join(fixture.target, 'references', 'obsolete.txt')));
  assert(fs.existsSync(path.join(fixture.target, 'references', 'new.txt')));
});

test('failed state commit rolls an upstream replacement back', fixture => {
  reconcileSkill(fixture.options('apply'));
  const targetBefore = hashTree(fixture.target);
  const stateBefore = fs.readFileSync(fixture.statePath, 'utf8');
  write(path.join(fixture.source, 'SKILL.md'), 'version two\n');

  const originalRename = fs.renameSync;
  fs.renameSync = (source, destination) => {
    if (destination === fixture.statePath && source.endsWith('.tmp')) {
      throw new Error('injected state commit failure');
    }
    return originalRename(source, destination);
  };
  try {
    assert.throws(() => reconcileSkill(fixture.options('apply')), /injected state commit failure/);
  } finally {
    fs.renameSync = originalRename;
  }

  assert.strictEqual(hashTree(fixture.target), targetBefore);
  assert.strictEqual(fs.readFileSync(fixture.statePath, 'utf8'), stateBefore);
});

test('locally modified target is preserved and upstream is staged', fixture => {
  reconcileSkill(fixture.options('apply'));
  write(path.join(fixture.target, 'SKILL.md'), 'local customization\n');
  write(path.join(fixture.source, 'SKILL.md'), 'version two\n');
  const targetBefore = fs.readFileSync(path.join(fixture.target, 'SKILL.md'), 'utf8');
  const result = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(result.classification, 'locally_modified');
  assert.strictEqual(result.action, 'staged_for_review');
  assert.strictEqual(fs.readFileSync(path.join(fixture.target, 'SKILL.md'), 'utf8'), targetBefore);
  const incoming = path.join(fixture.projectRoot, result.review_path);
  assert.strictEqual(hashTree(incoming), hashTree(fixture.source));
  assert(loadState(fixture.statePath).pending[fixture.capabilityId]);
});

test('existing target without baseline is never overwritten', fixture => {
  write(path.join(fixture.target, 'SKILL.md'), 'unknown owner content\n');
  const result = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(result.classification, 'baseline_unknown');
  assert.strictEqual(result.action, 'staged_for_review');
  assert.strictEqual(fs.readFileSync(path.join(fixture.target, 'SKILL.md'), 'utf8'), 'unknown owner content\n');
  assert(!loadState(fixture.statePath).capabilities[fixture.capabilityId]);
});

test('dry-run and apply agree without mutating the target during dry-run', fixture => {
  reconcileSkill(fixture.options('apply'));
  write(path.join(fixture.source, 'SKILL.md'), 'version two\n');
  const targetBefore = hashTree(fixture.target);
  const dry = reconcileSkill(fixture.options('dry-run'));
  assert.strictEqual(dry.classification, 'upstream_changed');
  assert.strictEqual(dry.action, 'would_replace_atomically');
  assert.strictEqual(hashTree(fixture.target), targetBefore);
  const applied = reconcileSkill(fixture.options('apply'));
  assert.strictEqual(applied.classification, dry.classification);
});

test('removed selection is reported without deletion', fixture => {
  reconcileSkill(fixture.options('apply'));
  const selectedPath = path.join(fixture.tempRoot, 'selected.txt');
  write(selectedPath, 'plugins/d-nd-core/skills/another-skill\n');
  const audit = auditRemoved(fixture.statePath, selectedPath);
  assert.deepStrictEqual(audit.selection_removed, [fixture.capabilityId]);
  assert.strictEqual(audit.deletes_files, false);
  assert(fs.existsSync(fixture.target));
});

test('source and target containment are enforced', fixture => {
  const externalSource = path.join(fixture.tempRoot, 'external', fixture.capabilityId);
  write(path.join(externalSource, 'SKILL.md'), 'external\n');
  assert.throws(
    () => reconcileSkill({ ...fixture.options(), source: externalSource }),
    /not the selected Seed capability/
  );
  const externalTarget = path.join(fixture.tempRoot, 'outside', fixture.capabilityId);
  assert.throws(
    () => reconcileSkill({ ...fixture.options(), target: externalTarget }),
    /escapes project root/
  );
});

test('corrupt installed state fails closed', fixture => {
  write(fixture.statePath, '{"schema":"wrong","capabilities":{}}\n');
  assert.throws(() => reconcileSkill(fixture.options()), /unsupported skill state schema/);
});

console.log(`OK: ${passed} skill reconciliation tests passed`);
