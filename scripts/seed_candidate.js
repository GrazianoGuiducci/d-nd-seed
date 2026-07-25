#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const schemaId = 'dnd.seed.update_candidate.v1';
const classifications = new Set([
  'trigger_template',
  'subskill',
  'standalone_skill',
  'metaskill',
  'repokernel_rule',
  'seed_public_candidate',
  'product_capability'
]);
const effectClasses = new Set([
  'reasoning_only',
  'local_write_gated',
  'external_action_gated',
  'sensitive_data_gated'
]);
const promotionTargets = new Set(['capability_registry', 'faculty_registry', 'documentation', 'none']);
const forbiddenResidue = [
  /(^|[\s"'(])[A-Za-z]:[\\/]/,
  /\\\\[^\\/]+[\\/][^\\/]+/,
  /\/home\//,
  /\/Users\//,
  /\/opt\//,
  /GRAZIANO_GITHUB_TOKEN/i,
  /github_pat_/i,
  /active_surface\.json/i
];

function stringsIn(value, output = []) {
  if (typeof value === 'string') output.push(value);
  else if (Array.isArray(value)) value.forEach(item => stringsIn(item, output));
  else if (value && typeof value === 'object') Object.values(value).forEach(item => stringsIn(item, output));
  return output;
}

function validateCandidate(candidate) {
  const errors = [];
  const blockers = [];
  if (!candidate || typeof candidate !== 'object' || Array.isArray(candidate)) {
    return { errors: ['candidate must be an object'], blockers: [], decision: 'invalid' };
  }
  if (candidate.schema !== schemaId) errors.push('invalid candidate schema');
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(candidate.candidate_id || '')) errors.push('invalid candidate_id');
  if (typeof candidate.title !== 'string' || !candidate.title.trim()) errors.push('title is required');
  if (!/^\d{4}-\d{2}-\d{2}$/.test(candidate.observed_date || '')) errors.push('observed_date must be YYYY-MM-DD');

  const origin = candidate.origin || {};
  if (!['withheld_private_source', 'public_source'].includes(origin.disclosure)) errors.push('invalid origin disclosure');
  if (!['maintainer_attested', 'publicly_reproducible'].includes(origin.evidence_status)) errors.push('invalid origin evidence_status');
  if (origin.disclosure === 'public_source') {
    if (typeof origin.public_url !== 'string' || !/^https:\/\//.test(origin.public_url)) errors.push('public_source requires an HTTPS public_url');
    if (typeof origin.revision !== 'string' || !origin.revision.trim()) errors.push('public_source requires a revision');
  } else if (origin.public_url !== null || origin.revision !== null) {
    errors.push('withheld_private_source must not expose public_url or revision placeholders');
  }

  const proposal = candidate.proposal || {};
  if (!classifications.has(proposal.classification)) errors.push('invalid proposal classification');
  if (typeof proposal.public_function !== 'string' || !proposal.public_function.trim()) errors.push('public_function is required');
  if (typeof proposal.expected_result !== 'string' || !proposal.expected_result.trim()) errors.push('expected_result is required');
  if (!['neutral_method_only', 'source_copy_review'].includes(proposal.transfer_mode)) errors.push('invalid transfer_mode');

  const safety = candidate.safety || {};
  if (safety.private_residue_removed !== true) blockers.push('private_residue_review_required');
  if (safety.authority_transfer !== false) errors.push('authority_transfer must be false');
  if (safety.automatic_publication !== false) errors.push('automatic_publication must be false');
  if (!effectClasses.has(safety.effect_class)) errors.push('invalid effect_class');
  if (safety.effect_review !== 'complete') blockers.push('effect_review_required');
  if (!['not_applicable_method_only', 'compatible_evidence_attached', 'separate_review_required', 'unknown'].includes(safety.license_status)) {
    errors.push('invalid license_status');
  }
  if (proposal.transfer_mode === 'neutral_method_only' && safety.source_code_included !== false) {
    errors.push('neutral_method_only cannot include source code');
  }
  if (proposal.transfer_mode === 'source_copy_review') {
    if (safety.source_code_included !== true) errors.push('source_copy_review must declare source_code_included=true');
    if (safety.license_status !== 'compatible_evidence_attached') blockers.push('capability_license_evidence_required');
  }
  if (['unknown', 'separate_review_required'].includes(safety.license_status)) blockers.push('license_review_required');

  const promotion = candidate.promotion || {};
  if (promotion.status !== 'queued') errors.push('promotion status must be queued');
  if (!promotionTargets.has(promotion.target)) errors.push('invalid promotion target');

  stringsIn(candidate).forEach(value => {
    for (const pattern of forbiddenResidue) {
      if (pattern.test(value)) errors.push(`private residue matched ${pattern}`);
    }
  });

  return {
    schema: 'dnd.seed.update_candidate_reduction.v1',
    candidate_id: candidate.candidate_id || null,
    errors: [...new Set(errors)],
    blockers: [...new Set(blockers)],
    decision: errors.length ? 'invalid' : blockers.length ? 'blocked' : 'ready_for_registry_review',
    automatic_registry_update: false,
    automatic_publication: false,
    required_human_gates: ['source_owner_review', 'public_neutral_diff_review', 'validation', 'commit_and_push']
  };
}

function validateFile(filePath) {
  const candidate = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  return { file: filePath, ...validateCandidate(candidate) };
}

function checkDirectory(directory) {
  if (!fs.existsSync(directory)) return [];
  return fs.readdirSync(directory)
    .filter(name => name.endsWith('.json'))
    .sort()
    .map(name => validateFile(path.join(directory, name)));
}

function parseArgs(argv) {
  const args = {};
  for (const arg of argv) {
    if (arg.startsWith('--file=')) args.file = arg.slice(7);
    else if (arg.startsWith('--check-dir=')) args.directory = arg.slice(12);
    else throw new Error(`unknown option: ${arg}`);
  }
  return args;
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    if (!args.file && !args.directory) throw new Error('use --file=<candidate.json> or --check-dir=<directory>');
    const results = args.file ? [validateFile(path.resolve(args.file))] : checkDirectory(path.resolve(args.directory));
    console.log(JSON.stringify({ schema: 'dnd.seed.update_candidate_check.v1', count: results.length, results }, null, 2));
    if (results.some(result => result.decision !== 'ready_for_registry_review')) process.exit(1);
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) main();

module.exports = { checkDirectory, forbiddenResidue, schemaId, validateCandidate, validateFile };
