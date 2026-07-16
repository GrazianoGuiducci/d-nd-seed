#!/usr/bin/env node
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const registryPath = path.join(root, 'capabilities', 'registry.json');
const contractPath = path.join(root, 'capabilities', 'mmk-compatibility.json');
const openCodeProfilePath = path.join(root, 'profiles', 'example-opencode.json');
const legacyCatalogPath = path.join(root, 'skills', 'catalog.json');

const classifications = new Set(['keep', 'adapt', 'supersede', 'retire_candidate', 'unknown']);
const levels = new Set(['system', 'default', 'environment-selected']);

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function sha256File(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function sameIds(a, b) {
  return a.length === b.length && a.every((value, index) => value === b[index]);
}

function main() {
  const errors = [];
  const registry = readJson(registryPath);
  const contract = readJson(contractPath);
  const profile = readJson(openCodeProfilePath);
  const legacyCatalog = readJson(legacyCatalogPath);
  const caps = registry.capabilities || [];
  const rows = contract.classifications || [];
  const capById = new Map(caps.map(cap => [cap.id, cap]));
  const rowIds = rows.map(row => row.id);
  const registryIds = caps.map(cap => cap.id);

  if (contract.schema !== 'dnd.seed.mmk_compatibility.v1') errors.push('invalid contract schema');
  if (new Set(rowIds).size !== rowIds.length) errors.push('duplicate classification id');
  const missing = registryIds.filter(id => !rowIds.includes(id));
  const extra = rowIds.filter(id => !capById.has(id));
  if (missing.length) errors.push(`missing classifications: ${missing.join(', ')}`);
  if (extra.length) errors.push(`unknown classifications: ${extra.join(', ')}`);

  for (const row of rows) {
    if (!classifications.has(row.classification)) errors.push(`${row.id}: invalid classification`);
    if (!levels.has(row.selection_level)) errors.push(`${row.id}: invalid selection_level`);
    if (!row.rationale) errors.push(`${row.id}: rationale is required`);
    const cap = capById.get(row.id);
    if (cap && ['uses_network', 'publishes'].includes(cap.risk) && row.classification !== 'unknown') {
      errors.push(`${row.id}: network/publish capability must remain unknown`);
    }
  }

  const inventory = contract.inventory || {};
  if (inventory.path !== 'capabilities/registry.json') errors.push('inventory.path mismatch');
  if (inventory.schema !== registry.schema) errors.push('inventory.schema mismatch');
  if (inventory.version !== registry.version) errors.push('inventory.version mismatch');
  if (inventory.sha256 !== sha256File(registryPath)) errors.push('inventory.sha256 drift');
  if (legacyCatalog.catalog_role !== 'legacy_coder_thinker_skill_taxonomy') errors.push('legacy catalog role is not explicit');
  if (legacyCatalog.selection_authority !== false) errors.push('legacy catalog must not own selection');
  if (legacyCatalog.capability_registry !== 'capabilities/registry.json') errors.push('legacy catalog registry pointer mismatch');
  if (legacyCatalog.mmk_compatibility !== 'capabilities/mmk-compatibility.json') errors.push('legacy catalog MMK pointer mismatch');

  const policy = contract.selection_policy || {};
  const system = policy.system_bundle || [];
  const defaults = policy.default_bundle_additions || [];
  if (system.length === 0 || system.length > 2) errors.push('system bundle must contain one or two capabilities');
  if (defaults.length > 1) errors.push('default additions must remain at most one capability');
  if (new Set(system).size !== system.length) errors.push('system bundle contains duplicate ids');
  if (new Set(defaults).size !== defaults.length) errors.push('default additions contain duplicate ids');
  const overlap = defaults.filter(id => system.includes(id));
  if (overlap.length) errors.push(`system/default bundles overlap: ${overlap.join(', ')}`);
  for (const id of [...system, ...defaults]) {
    const cap = capById.get(id);
    const row = rows.find(item => item.id === id);
    if (!cap || !row) errors.push(`bundle references unknown capability: ${id}`);
    else {
      if (cap.risk !== 'safe') errors.push(`${id}: default bundle risk is not safe`);
      if (['hook', 'plugin'].includes(cap.type)) errors.push(`${id}: hook/plugin cannot enter default bundle`);
      if (!['keep', 'adapt'].includes(row.classification)) errors.push(`${id}: invalid default classification`);
    }
  }
  for (const row of rows) {
    const expectedLevel = system.includes(row.id) ? 'system' : defaults.includes(row.id) ? 'default' : 'environment-selected';
    if (row.selection_level !== expectedLevel) {
      errors.push(`${row.id}: selection_level ${row.selection_level} does not match bundle role ${expectedLevel}`);
    }
  }
  const systemSet = new Set(system);
  const defaultSet = new Set([...system, ...defaults]);
  for (const id of system) {
    const missingDeps = (capById.get(id)?.requires || []).filter(dep => !systemSet.has(dep));
    if (missingDeps.length) errors.push(`${id}: system bundle is missing dependencies ${missingDeps.join(', ')}`);
  }
  for (const id of defaults) {
    const missingDeps = (capById.get(id)?.requires || []).filter(dep => !defaultSet.has(dep));
    if (missingDeps.length) errors.push(`${id}: default bundle is missing dependencies ${missingDeps.join(', ')}`);
  }
  if (policy.levels_are_cumulative !== true) errors.push('selection levels must be cumulative');
  if (!policy.environment_selected_requires_allowlist) errors.push('environment selection must require allowlist');
  if (!policy.environment_selected_requires_ephemeral_host_evidence) errors.push('environment selection must require ephemeral host evidence');
  if (!policy.mmk_current_session_validation_external) errors.push('MMK current-session validation must remain external');
  if (policy.capability_effect_review_required !== true) errors.push('capability effect review must remain required');
  if (policy.registry_risk_is_effect_proof !== false) errors.push('registry risk must not be treated as effect proof');
  if (policy.automatic_activation !== false) errors.push('automatic_activation must be false');
  if (policy.authority_ceiling !== 'inventory_only_no_activation') errors.push('invalid authority ceiling');

  const license = contract.license_boundary || {};
  if (license.repo_license !== 'AGPL-3.0') errors.push('repo_license must preserve the existing declaration');
  if (license.capability_license_default !== 'unknown') errors.push('capability license default must be unknown');
  if (license.capability_license_status_default !== 'not_declared_per_capability') errors.push('invalid capability license status');
  if (license.compatibility_gate_default !== 'review_required_before_copy_or_embedding') errors.push('invalid license compatibility gate');
  if (license.legal_strategy_resolved !== false) errors.push('legal strategy must remain unresolved');
  for (const [id, override] of Object.entries(contract.capability_license_overrides || {})) {
    if (!capById.has(id)) errors.push(`license override references unknown capability: ${id}`);
    if (!override || typeof override !== 'object' || Array.isArray(override)) {
      errors.push(`${id}: license override must be an object`);
      continue;
    }
    if (override.capability_license && typeof override.capability_license !== 'string') errors.push(`${id}: invalid capability license override`);
    if (override.status && typeof override.status !== 'string') errors.push(`${id}: invalid capability license status override`);
    if (override.compatibility_gate && typeof override.compatibility_gate !== 'string') errors.push(`${id}: invalid compatibility gate override`);
  }

  if (profile.agent_runtime !== 'opencode') errors.push('OpenCode profile runtime mismatch');
  if (profile.install_mode !== 'minimal') errors.push('OpenCode profile must be minimal');
  if (profile.mmk_selection_level !== 'system') errors.push('OpenCode profile must start at system level');
  if (profile.risk_tolerance !== 'safe') errors.push('OpenCode profile risk must be safe');
  if (profile.write_policy !== 'plan_only') errors.push('OpenCode profile must be plan_only');
  if (!sameIds([...profile.capability_allowlist].sort(), [...system].sort())) errors.push('OpenCode allowlist must equal system bundle');
  if (Object.values(profile.implicit_capabilities || {}).some(Boolean)) errors.push('OpenCode profile has implicit capabilities');
  if (profile.host_capability_policy?.on_missing !== 'plan_only') errors.push('missing attestation must remain plan_only');
  if (profile.host_capability_policy?.grants_authority !== false) errors.push('attestation cannot grant authority');
  if (profile.host_capability_policy?.persists_attestation !== false) errors.push('attestation cannot persist as session truth');
  if (profile.host_capability_policy?.session_attestation !== 'required_for_environment-selected') errors.push('invalid OpenCode attestation policy');
  if (profile.host_capability_policy?.validation_owner !== 'mmk_external') errors.push('OpenCode session validation owner must remain external MMK');
  if (!Number.isInteger(profile.host_capability_policy?.max_age_seconds) || profile.host_capability_policy.max_age_seconds <= 0) {
    errors.push('OpenCode evidence age window must be a positive integer');
  }
  if (profile.host_capability_policy?.max_age_seconds > 3600) errors.push('OpenCode evidence age window must not exceed 3600 seconds');
  if ('model' in profile || 'model_id' in profile || 'provider' in profile) errors.push('OpenCode profile must be model-agnostic');

  if (errors.length) {
    console.error('ERRORS');
    for (const error of errors) console.error(`- ${error}`);
    process.exit(1);
  }

  const counts = {};
  for (const row of rows) counts[row.classification] = (counts[row.classification] || 0) + 1;
  console.log(`OK: MMK/Seed contract validates (${rows.length}/${caps.length} classified)`);
  console.log(`Classification counts: ${Object.entries(counts).map(([key, value]) => `${key}=${value}`).join(', ')}`);
  console.log(`System/default bundle: ${system.length}+${defaults.length}`);
}

main();
