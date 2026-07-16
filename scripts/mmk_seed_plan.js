#!/usr/bin/env node
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const realRoot = fs.realpathSync(root);
const registryPath = path.join(root, 'capabilities', 'registry.json');
const contractPath = path.join(root, 'capabilities', 'mmk-compatibility.json');

const registryRiskHints = {
  safe: 'safe_label_only_not_effect_proof',
  writes_files: 'local_write_candidate',
  uses_network: 'network_candidate',
  uses_secrets: 'secret_adjacent_candidate',
  publishes: 'publication_candidate',
  runtime: 'runtime_candidate',
  destructive: 'destructive_candidate'
};

const forbiddenAttestationCapabilityFields = new Set([
  'authority_state',
  'effect_scope',
  'authorized_effects',
  'blocked_effects',
  'freshness_state',
  'availability_state'
]);

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function hashBuffer(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function isInside(parent, candidate) {
  const rel = path.relative(parent, candidate);
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

function sourceHash(sourcePath) {
  if (typeof sourcePath !== 'string' || !sourcePath || path.isAbsolute(sourcePath)) {
    throw new Error(`Capability source path must be repository-relative: ${sourcePath}`);
  }
  const absolute = path.resolve(root, sourcePath);
  if (!isInside(root, absolute) || !fs.existsSync(absolute)) {
    throw new Error(`Capability source escapes or is missing from Seed: ${sourcePath}`);
  }
  const realAbsolute = fs.realpathSync(absolute);
  if (!isInside(realRoot, realAbsolute)) {
    throw new Error(`Capability source resolves outside Seed: ${sourcePath}`);
  }

  const stat = fs.statSync(realAbsolute);
  if (stat.isFile()) return hashBuffer(fs.readFileSync(realAbsolute));
  const files = [];
  const walk = current => {
    for (const entry of fs.readdirSync(current, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const full = path.join(current, entry.name);
      if (entry.isSymbolicLink()) throw new Error(`Symbolic link is not allowed in capability source tree: ${sourcePath}`);
      if (entry.isDirectory()) walk(full);
      else if (entry.isFile()) files.push(full);
    }
  };
  walk(realAbsolute);
  const digestInput = files.map(file => {
    const rel = path.relative(realAbsolute, file).replace(/\\/g, '/');
    return `${rel}\0${hashBuffer(fs.readFileSync(file))}\n`;
  }).join('');
  return hashBuffer(Buffer.from(digestInput, 'utf8'));
}

function resolveInput(input) {
  const candidates = [
    path.resolve(process.cwd(), input),
    path.join(root, 'profiles', input),
    path.join(root, 'profiles', `${input}.json`)
  ];
  return candidates.find(fs.existsSync) || null;
}

function parseArgs(argv) {
  const args = { profile: null, level: null, attestation: null };
  for (const arg of argv) {
    if (arg.startsWith('--level=')) args.level = arg.slice('--level='.length);
    else if (arg.startsWith('--session-attestation=')) args.attestation = arg.slice('--session-attestation='.length);
    else if (!arg.startsWith('--') && !args.profile) args.profile = arg;
    else throw new Error(`Unknown or duplicate argument: ${arg}`);
  }
  if (!args.profile) throw new Error('Missing profile path');
  return args;
}

function validateAttestationEnvelope(value, profile, registryIds) {
  const errors = [];
  if (value.schema !== 'mmk.session-capability-attestation.v0.1') errors.push('invalid attestation schema');
  for (const key of ['attestation_id', 'session_id', 'host_id', 'owner_surface', 'observed_at', 'runtime']) {
    if (!value[key]) errors.push(`attestation.${key} is required`);
  }
  if (value.ephemeral !== true) errors.push('attestation.ephemeral must be true');
  if (value.grants_authority !== false) errors.push('attestation.grants_authority must be false');
  if (value.runtime !== profile.agent_runtime) errors.push('attestation runtime does not match profile');
  if (value.host_id !== profile.node_id) errors.push('attestation host_id does not match profile node_id');

  const observedAt = Date.parse(value.observed_at);
  const maxAgeSeconds = profile.host_capability_policy?.max_age_seconds;
  if (!Number.isInteger(maxAgeSeconds) || maxAgeSeconds <= 0) {
    errors.push('profile host evidence age window is missing or invalid');
  }
  if (Number.isInteger(maxAgeSeconds) && maxAgeSeconds > 3600) {
    errors.push('profile host evidence age window exceeds 3600 seconds');
  }
  if (!Number.isFinite(observedAt)) {
    errors.push('attestation.observed_at must be a valid ISO timestamp');
  } else if (Number.isInteger(maxAgeSeconds) && maxAgeSeconds > 0) {
    const ageMs = Date.now() - observedAt;
    if (ageMs < -60000) errors.push('attestation.observed_at is in the future');
    if (ageMs > maxAgeSeconds * 1000) errors.push('attestation exceeds the profile evidence age window');
  }

  if (!Array.isArray(value.capabilities)) errors.push('attestation.capabilities must be an array');
  const seen = new Set();
  for (const cap of value.capabilities || []) {
    if (!cap || typeof cap !== 'object' || Array.isArray(cap)) {
      errors.push('attested capability must be an object');
      continue;
    }
    if (!cap.capability_id) errors.push('attested capability_id is required');
    if (seen.has(cap.capability_id)) errors.push(`duplicate attested capability_id: ${cap.capability_id}`);
    seen.add(cap.capability_id);
    if (cap.capability_id && !registryIds.has(cap.capability_id)) {
      errors.push(`attestation contains unknown capability: ${cap.capability_id}`);
    }
    for (const field of forbiddenAttestationCapabilityFields) {
      if (field in cap) errors.push(`${cap.capability_id}: forbidden authority/effect field ${field}`);
    }
    if (typeof cap.exposed !== 'boolean') errors.push(`${cap.capability_id}: exposed must be boolean`);
    if (!['verified', 'unknown', 'unavailable'].includes(cap.access_state)) errors.push(`${cap.capability_id}: invalid access_state`);
    if (!['verified', 'unknown', 'missing'].includes(cap.operational_path_state)) errors.push(`${cap.capability_id}: invalid operational_path_state`);
    if (typeof cap.evidence !== 'string' || !cap.evidence.trim()) errors.push(`${cap.capability_id}: evidence is required`);
    if (cap.exposed === false && (cap.access_state !== 'unavailable' || cap.operational_path_state !== 'missing')) {
      errors.push(`${cap.capability_id}: exposed=false requires unavailable access and missing operational path`);
    }
  }
  if (errors.length) throw new Error(errors.join('; '));
}

function requiredGates(row, cap, missingDependencies, selectedConflicts, hasEvidence) {
  const gates = ['explicit_selection_required', 'capability_effect_review_required'];
  if (row.classification === 'unknown') gates.push('owner_and_runtime_verification_required');
  if (row.classification === 'retire_candidate') gates.push('deprecation_review_required');
  if (row.classification === 'supersede') gates.push('replacement_mapping_review_required');
  if (cap.risk !== 'safe') gates.push(`registry_risk_${registryRiskHints[cap.risk]}_gate`);
  if (missingDependencies.length) gates.push('explicit_dependency_selection_required');
  if (selectedConflicts.length) gates.push('capability_conflict_review_required');
  gates.push(hasEvidence ? 'mmk_session_validation_required' : 'current_host_session_evidence_required');
  gates.push('owner_effect_authority_gate_required');
  return [...new Set(gates)];
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const profilePath = resolveInput(args.profile);
    if (!profilePath) throw new Error(`Profile not found: ${args.profile}`);

    for (const [script, scriptArgs] of [
      ['scripts/validate_mmk_seed_contract.js', []],
      ['scripts/validate_profile.js', [profilePath, '--target-policy=read-only', '--json']]
    ]) {
      const result = spawnSync(process.execPath, [path.join(root, script), ...scriptArgs], { cwd: root, encoding: 'utf8' });
      if (result.status !== 0) throw new Error((result.stdout + result.stderr).trim() || `${script} failed`);
    }

    const profileBytes = fs.readFileSync(profilePath);
    const registryBytes = fs.readFileSync(registryPath);
    const contractBytes = fs.readFileSync(contractPath);
    const profile = JSON.parse(profileBytes.toString('utf8'));
    const registry = JSON.parse(registryBytes.toString('utf8'));
    const contract = JSON.parse(contractBytes.toString('utf8'));
    const profileSha256 = hashBuffer(profileBytes);
    const contractSha256 = hashBuffer(contractBytes);
    const level = args.level || profile.mmk_selection_level || 'system';
    if (!contract.selection_policy.levels.includes(level)) throw new Error(`Invalid selection level: ${level}`);
    const allowlist = Array.isArray(profile.capability_allowlist) ? profile.capability_allowlist : [];
    if (level === 'environment-selected' && !Array.isArray(profile.capability_allowlist)) {
      throw new Error('environment-selected requires an explicit capability allowlist');
    }

    const capById = new Map(registry.capabilities.map(cap => [cap.id, cap]));
    const registryIds = new Set(capById.keys());
    let attestation = null;
    let attestationSha256 = null;
    if (args.attestation) {
      const attestationPath = path.resolve(process.cwd(), args.attestation);
      const attestationBytes = fs.readFileSync(attestationPath);
      attestation = JSON.parse(attestationBytes.toString('utf8'));
      attestationSha256 = hashBuffer(attestationBytes);
      validateAttestationEnvelope(attestation, profile, registryIds);
    }
    if (level === 'environment-selected' && !attestation) {
      throw new Error('environment-selected requires profile-bound ephemeral host evidence; MMK session validation remains external');
    }

    const system = contract.selection_policy.system_bundle;
    const defaults = contract.selection_policy.default_bundle_additions;
    const candidates = [...new Set(
      level === 'system'
        ? system
        : level === 'default'
          ? [...system, ...defaults]
          : [...system, ...defaults, ...allowlist]
    )];
    const selectedIds = new Set(candidates);
    const rowById = new Map(contract.classifications.map(row => [row.id, row]));
    const attestedById = new Map((attestation?.capabilities || []).map(cap => [cap.capability_id, cap]));
    const licenseOverrides = contract.capability_license_overrides || {};

    const selected = candidates.map(id => {
      const cap = capById.get(id);
      const row = rowById.get(id);
      if (!cap || !row) throw new Error(`Unknown selected capability: ${id}`);
      const attested = attestedById.get(id) || null;
      const license = licenseOverrides[id] || {};
      const missingDependencies = (cap.requires || []).filter(dep => !selectedIds.has(dep));
      const selectedConflicts = (cap.conflicts_with || []).filter(conflict => selectedIds.has(conflict));
      return {
        id,
        type: cap.type,
        path: cap.path,
        source_sha256: sourceHash(cap.path),
        classification: row.classification,
        selection_level: row.selection_level,
        registry_risk: cap.risk,
        registry_risk_hint: registryRiskHints[cap.risk],
        side_effect_class: 'unknown_until_capability_effect_review',
        requires: cap.requires || [],
        missing_selected_dependencies: missingDependencies,
        conflicts_with_selected: selectedConflicts,
        authority_ceiling: contract.selection_policy.authority_ceiling,
        required_gates: requiredGates(row, cap, missingDependencies, selectedConflicts, Boolean(attested)),
        host_compatibility: attested ? {
          state: attested.exposed && attested.access_state === 'verified' && attested.operational_path_state === 'verified'
            ? 'profile_bound_evidence_for_planning'
            : 'unknown',
          verification_scope: 'seed_structural_checks_only_mmk_session_validation_external',
          exposed: attested.exposed,
          access_state: attested.access_state,
          operational_path_state: attested.operational_path_state,
          evidence: attested.evidence
        } : { state: 'session_attestation_required' },
        activation_allowed: false,
        repo_license: contract.license_boundary.repo_license,
        capability_license: license.capability_license || contract.license_boundary.capability_license_default,
        capability_license_status: license.status || contract.license_boundary.capability_license_status_default,
        compatibility_gate: license.compatibility_gate || contract.license_boundary.compatibility_gate_default
      };
    });

    const unresolvedDependencies = selected.flatMap(item =>
      item.missing_selected_dependencies.map(dependency => ({ capability_id: item.id, dependency }))
    );
    const selectedConflicts = selected.flatMap(item =>
      item.conflicts_with_selected.map(conflict => ({ capability_id: item.id, conflict }))
    );
    const selectionMaterial = JSON.stringify({
      registry_sha256: contract.inventory.sha256,
      compatibility_contract_sha256: contractSha256,
      profile_sha256: profileSha256,
      runtime: profile.agent_runtime,
      level,
      target_effect: 'inventory_mapping_only',
      session_attestation_sha256: attestationSha256,
      selected: selected.map(item => [item.id, item.source_sha256, item.required_gates])
    });

    const output = {
      schema: 'dnd.seed.mmk_plan.v1',
      boundary: 'plan_only_no_activation',
      profile: path.relative(root, profilePath).replace(/\\/g, '/'),
      profile_sha256: profileSha256,
      runtime: profile.agent_runtime,
      model_assumption: null,
      selection_level: level,
      selection_levels_are_cumulative: true,
      target_effect: 'inventory_mapping_only',
      registry: contract.inventory,
      compatibility_contract: {
        path: 'capabilities/mmk-compatibility.json',
        schema: contract.schema,
        sha256: contractSha256
      },
      session_attestation: attestation ? {
        attestation_id: attestation.attestation_id,
        session_id: attestation.session_id,
        host_id: attestation.host_id,
        owner_surface: attestation.owner_surface,
        runtime: attestation.runtime,
        observed_at: attestation.observed_at,
        sha256: attestationSha256,
        seed_check: 'profile_bound_and_within_declared_age_window',
        mmk_session_validation_required: true,
        ephemeral: true,
        grants_authority: false
      } : null,
      selected,
      unresolved_dependencies: unresolvedDependencies,
      selected_conflicts: selectedConflicts,
      not_selected_count: registry.capabilities.length - selected.length,
      selection_sha256: hashBuffer(Buffer.from(selectionMaterial, 'utf8')),
      writes_target: false,
      activates_capabilities: false
    };
    console.log(JSON.stringify(output, null, 2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

main();
