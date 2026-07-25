#!/usr/bin/env node
'use strict';

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { validateCandidate } = require('./seed_candidate');

const root = path.resolve(__dirname, '..');
const example = JSON.parse(fs.readFileSync(path.join(root, 'docs', 'examples', 'seed-update-candidate.example.json'), 'utf8'));
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

function clone() {
  return JSON.parse(JSON.stringify(example));
}

test('neutral example is ready only for registry review', () => {
  const result = validateCandidate(clone());
  assert.deepStrictEqual(result.errors, []);
  assert.deepStrictEqual(result.blockers, []);
  assert.strictEqual(result.decision, 'ready_for_registry_review');
  assert.strictEqual(result.automatic_registry_update, false);
  assert.strictEqual(result.automatic_publication, false);
});

test('private paths and credentials are rejected', () => {
  for (const residue of ['C:/private/source', 'C:\\private\\source', '/home/operator/source', '\\\\server\\share', 'github_pat_secret']) {
    const candidate = clone();
    candidate.proposal.public_function = residue;
    assert(validateCandidate(candidate).errors.some(error => error.includes('private residue')), residue);
  }
});

test('source-copy proposals require explicit license evidence', () => {
  const candidate = clone();
  candidate.proposal.transfer_mode = 'source_copy_review';
  candidate.safety.source_code_included = true;
  candidate.safety.license_status = 'unknown';
  const result = validateCandidate(candidate);
  assert(result.blockers.includes('capability_license_evidence_required'));
  assert.strictEqual(result.decision, 'blocked');
});

test('effect and privacy review block promotion without invalidating the shape', () => {
  const candidate = clone();
  candidate.safety.private_residue_removed = false;
  candidate.safety.effect_review = 'required';
  const result = validateCandidate(candidate);
  assert.deepStrictEqual(result.errors, []);
  assert(result.blockers.includes('private_residue_review_required'));
  assert(result.blockers.includes('effect_review_required'));
});

test('automatic publication and authority transfer fail closed', () => {
  const candidate = clone();
  candidate.safety.automatic_publication = true;
  candidate.safety.authority_transfer = true;
  const result = validateCandidate(candidate);
  assert(result.errors.includes('automatic_publication must be false'));
  assert(result.errors.includes('authority_transfer must be false'));
  assert.strictEqual(result.decision, 'invalid');
});

console.log(`OK: ${passed} Seed candidate tests passed`);
