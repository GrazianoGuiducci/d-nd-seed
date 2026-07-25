#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const defaultRegistryPath = path.join(
  root,
  'plugins',
  'd-nd-core',
  'skills',
  'faculty-router',
  'references',
  'faculty-registry.json'
);

const allowedPortability = new Set([
  'portable_method',
  'adapted_contract',
  'related_resource',
  'gated_contract'
]);
const allowedEffects = new Set([
  'reasoning_only',
  'local_write_gated',
  'external_action_gated',
  'sensitive_data_gated'
]);
const allowedRoles = new Set([
  'binder',
  'primary',
  'support',
  'surface_adapter',
  'learning'
]);
const forbiddenPublicResidue = [
  /(^|[\s"'(])[A-Za-z]:[\\/]/,
  /\\\\[^\\/]+[\\/][^\\/]+/,
  /\/home\//,
  /\/Users\//,
  /\/opt\//,
  /GRAZIANO_GITHUB_TOKEN/i,
  /github_pat_/i,
  /active_surface\.json/i
];

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function stringsIn(value, out = []) {
  if (typeof value === 'string') out.push(value);
  else if (Array.isArray(value)) value.forEach(item => stringsIn(item, out));
  else if (value && typeof value === 'object') {
    Object.values(value).forEach(item => stringsIn(item, out));
  }
  return out;
}

function validateRegistry(registry) {
  const errors = [];
  const warnings = [];
  const faculties = Array.isArray(registry.faculties) ? registry.faculties : [];
  const bundles = new Set(Object.keys(registry.bundle_definitions || {}));
  const resultContracts = registry.result_contracts || {};
  const relatedResources = registry.related_resources || {};
  const ids = new Set();

  if (registry.schema !== 'dnd.seed.faculty_registry.v1') errors.push('invalid registry schema');
  if (!registry.version) errors.push('registry version is required');
  if (!registry.source_inventory || registry.source_inventory.total !== faculties.length) {
    errors.push('source_inventory.total must equal faculties.length');
  }
  if (registry.source_inventory?.internal_identity_map_included !== false) {
    errors.push('internal identity map must remain excluded');
  }
  if (registry.source_inventory?.evidence_status !== 'maintainer_attested') {
    errors.push('source inventory evidence must remain maintainer_attested');
  }
  if (registry.source_inventory?.publicly_reproducible !== false) {
    errors.push('source inventory must not claim publicly reproducible private-source coverage');
  }
  if (registry.policy?.automatic_activation !== false) errors.push('automatic activation must be false');
  if (registry.policy?.authority_ceiling !== 'method_and_plan_only') {
    errors.push('authority ceiling must remain method_and_plan_only');
  }
  if (registry.policy?.private_adapter_code_included !== false) {
    errors.push('private adapter code must remain excluded');
  }
  if (registry.policy?.source_runtime_state_included !== false) {
    errors.push('source runtime state must remain excluded');
  }
  if (registry.policy?.effect_review_required !== true) {
    errors.push('effect review must remain required');
  }
  if (registry.policy?.contract_license !== 'unknown') {
    errors.push('capability contract license must remain unknown without capability-level evidence');
  }
  if (registry.policy?.contract_license_status !== 'not_declared_per_capability') {
    errors.push('invalid capability contract license status');
  }
  if (bundles.size === 0) errors.push('at least one bundle definition is required');

  faculties.forEach((faculty, index) => {
    const label = faculty.id || `faculties[${index}]`;
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(faculty.id || '')) errors.push(`${label}: invalid id`);
    if (ids.has(faculty.id)) errors.push(`${label}: duplicate id`);
    ids.add(faculty.id);
    if (!faculty.title || !faculty.public_function) errors.push(`${label}: title and public_function are required`);
    if (typeof resultContracts[faculty.id] !== 'string' || !resultContracts[faculty.id].trim()) {
      errors.push(`${label}: result contract is required`);
    }
    if (!Array.isArray(faculty.bundles) || faculty.bundles.length === 0) errors.push(`${label}: bundles are required`);
    for (const bundle of faculty.bundles || []) {
      if (!bundles.has(bundle)) errors.push(`${label}: unknown bundle ${bundle}`);
    }
    if (!Array.isArray(faculty.roles) || faculty.roles.length === 0) errors.push(`${label}: roles are required`);
    for (const role of faculty.roles || []) {
      if (!allowedRoles.has(role)) errors.push(`${label}: unknown role ${role}`);
    }
    if (!allowedPortability.has(faculty.portability)) errors.push(`${label}: invalid portability`);
    if (!allowedEffects.has(faculty.effect_class)) errors.push(`${label}: invalid effect_class`);
    if (faculty.portability === 'related_resource') {
      if (!Array.isArray(faculty.resource_ids) || faculty.resource_ids.length === 0) {
        errors.push(`${label}: related_resource requires resource_ids`);
      }
      for (const resourceId of faculty.resource_ids || []) {
        if (!relatedResources[resourceId]) errors.push(`${label}: unknown related resource ${resourceId}`);
      }
    }
    if (faculty.effect_class === 'reasoning_only' && faculty.portability === 'gated_contract') {
      warnings.push(`${label}: gated contract has reasoning-only effect`);
    }
  });

  for (const bundle of bundles) {
    if (!faculties.some(faculty => Array.isArray(faculty.bundles) && faculty.bundles.includes(bundle))) {
      errors.push(`bundle has no faculties: ${bundle}`);
    }
  }
  for (const [id, resource] of Object.entries(relatedResources)) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id)) errors.push(`invalid related resource id: ${id}`);
    if (!resource || typeof resource !== 'object' || Array.isArray(resource)) {
      errors.push(`${id}: related resource must be an object`);
      continue;
    }
    if (typeof resource.url !== 'string' || !/^https:\/\//.test(resource.url)) {
      errors.push(`${id}: related resource requires an https URL`);
    }
    if (!resource.revision_status) errors.push(`${id}: related resource revision_status is required`);
    if (resource.license_status !== 'separate_review_required') {
      errors.push(`${id}: related resource license must require separate review`);
    }
  }
  for (const id of Object.keys(resultContracts)) {
    if (!ids.has(id)) errors.push(`orphan result contract: ${id}`);
  }

  stringsIn(registry).forEach(value => {
    for (const pattern of forbiddenPublicResidue) {
      if (pattern.test(value)) errors.push(`private residue matched ${pattern}: ${value}`);
    }
  });

  return {
    errors,
    warnings,
    count: faculties.length,
    bundleCount: bundles.size,
    resultContractCount: Object.keys(resultContracts).length
  };
}

function main() {
  const registryArg = process.argv.find(arg => arg.startsWith('--registry='));
  const registryPath = registryArg
    ? path.resolve(process.cwd(), registryArg.slice('--registry='.length))
    : defaultRegistryPath;
  const registry = readJson(registryPath);
  const result = validateRegistry(registry);
  result.warnings.forEach(warning => console.warn(`WARN: ${warning}`));
  if (result.errors.length) {
    result.errors.forEach(error => console.error(`ERROR: ${error}`));
    process.exit(1);
  }
  console.log(`OK: ${result.count} public-neutral faculties and ${result.resultContractCount} result contracts across ${result.bundleCount} bundles`);
}

if (require.main === module) main();

module.exports = { defaultRegistryPath, readJson, validateRegistry };
