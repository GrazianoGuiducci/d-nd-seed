#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const realRoot = fs.realpathSync(root);
const defaultRegistryPath = path.join(root, 'capabilities', 'registry.json');

const allowed = {
  type: new Set(['hook', 'skill', 'plugin', 'template', 'doc', 'lab_pattern', 'kernel']),
  stratum: new Set(['core_invariant', 'stable_default', 'contextual', 'recent_candidate', 'experimental', 'legacy_or_superseded']),
  maturity: new Set(['established', 'stable', 'emerging', 'candidate', 'experimental', 'deprecated']),
  risk: new Set(['safe', 'writes_files', 'uses_network', 'uses_secrets', 'publishes', 'runtime', 'destructive']),
  visibility: new Set(['default', 'recommended', 'optional', 'advanced', 'hidden']),
  agentStatus: new Set(['native', 'adapter', 'documented', 'unsupported'])
};

const required = [
  'id',
  'type',
  'path',
  'stratum',
  'maturity',
  'profiles',
  'intents',
  'risk',
  'visibility',
  'introduced',
  'reviewed',
  'supersedes',
  'superseded_by',
  'requires',
  'conflicts_with',
  'why'
];

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function listDirs(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(entry => entry.isDirectory())
    .map(entry => entry.name)
    .sort();
}

function listFiles(dir, suffix) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true })
    .filter(entry => entry.isFile() && entry.name.endsWith(suffix))
    .map(entry => entry.name)
    .sort();
}

function pathCoveredByRegistry(registryPaths, relPath) {
  if (registryPaths.has(relPath)) return true;
  const prefix = `${relPath}/`;
  return [...registryPaths].some(p => p.startsWith(prefix));
}

function isInside(parent, candidate) {
  const rel = path.relative(parent, candidate);
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

function main() {
  const strictCoverage = process.argv.includes('--strict-coverage');
  const registryArg = process.argv.find(arg => arg.startsWith('--registry='));
  const registryPath = registryArg
    ? path.resolve(process.cwd(), registryArg.slice('--registry='.length))
    : defaultRegistryPath;
  const registry = readJson(registryPath);
  const caps = registry.capabilities || [];
  const ids = new Set();
  const errors = [];
  const warnings = [];

  if (!registry.schema) errors.push('registry.schema is required');
  if (!registry.version) errors.push('registry.version is required');
  if (!Array.isArray(caps)) errors.push('registry.capabilities must be an array');

  for (const [index, cap] of caps.entries()) {
    const label = cap.id || `capability[${index}]`;
    for (const key of required) {
      if (!(key in cap)) errors.push(`${label}: missing required field ${key}`);
    }
    if (cap.id && ids.has(cap.id)) errors.push(`${label}: duplicate id`);
    if (cap.id) ids.add(cap.id);

    for (const key of ['type', 'stratum', 'maturity', 'risk', 'visibility']) {
      if (cap[key] && !allowed[key].has(cap[key])) errors.push(`${label}: invalid ${key}: ${cap[key]}`);
    }

    for (const key of ['profiles', 'intents', 'supersedes', 'requires', 'conflicts_with']) {
      if (key in cap && !Array.isArray(cap[key])) errors.push(`${label}: ${key} must be an array`);
    }

    if (cap.path) {
      if (path.isAbsolute(cap.path)) {
        errors.push(`${label}: path must be repository-relative: ${cap.path}`);
      } else {
        const source = path.resolve(root, cap.path);
        if (!isInside(root, source)) {
          errors.push(`${label}: path escapes the seed repository: ${cap.path}`);
        } else if (!fs.existsSync(source)) {
          errors.push(`${label}: path does not exist: ${cap.path}`);
        } else if (!isInside(realRoot, fs.realpathSync(source))) {
          errors.push(`${label}: path resolves outside the seed repository: ${cap.path}`);
        }
      }
    }

    if (!cap.agent_support || typeof cap.agent_support !== 'object' || Array.isArray(cap.agent_support)) {
      errors.push(`${label}: agent_support object is required`);
    } else {
      for (const [agent, support] of Object.entries(cap.agent_support)) {
        if (!support || typeof support !== 'object' || Array.isArray(support)) {
          errors.push(`${label}: agent_support.${agent} must be an object`);
          continue;
        }
        if (!allowed.agentStatus.has(support.status)) {
          errors.push(`${label}: invalid agent_support.${agent}.status: ${support.status}`);
        }
      }
    }

    for (const ref of cap.requires || []) {
      if (!ids.has(ref) && !caps.some(candidate => candidate.id === ref)) {
        errors.push(`${label}: requires unknown capability ${ref}`);
      }
    }
    for (const ref of cap.supersedes || []) {
      if (!ids.has(ref) && !caps.some(candidate => candidate.id === ref)) {
        warnings.push(`${label}: supersedes unknown capability ${ref}`);
      }
    }
    for (const ref of cap.conflicts_with || []) {
      if (!ids.has(ref) && !caps.some(candidate => candidate.id === ref)) {
        errors.push(`${label}: conflicts_with unknown capability ${ref}`);
      }
    }
    if (cap.superseded_by && !caps.some(candidate => candidate.id === cap.superseded_by)) {
      warnings.push(`${label}: superseded_by unknown capability ${cap.superseded_by}`);
    }
  }

  const registryPaths = new Set(caps.map(cap => cap.path));
  for (const hook of listFiles(path.join(root, 'templates', 'hooks'), '.tmpl')) {
    const p = `templates/hooks/${hook}`;
    if (!registryPaths.has(p)) warnings.push(`unregistered hook template: ${p}`);
  }
  for (const skill of listDirs(path.join(root, 'plugins', 'd-nd-core', 'skills'))) {
    const p = `plugins/d-nd-core/skills/${skill}`;
    if (!registryPaths.has(p)) warnings.push(`unregistered core skill: ${p}`);
  }
  for (const plugin of listDirs(path.join(root, 'plugins'))) {
    const p = `plugins/${plugin}`;
    if (plugin !== 'd-nd-core' && !registryPaths.has(p)) warnings.push(`unregistered plugin: ${p}`);
  }

  const referenceOnlyTemplateSkills = new Map();
  const referenceOnlyPath = path.join(root, 'templates', 'skills', 'reference-only.json');
  if (fs.existsSync(referenceOnlyPath)) {
    const manifest = readJson(referenceOnlyPath);
    if (manifest.schema !== 'dnd.seed.reference_only_template_skills.v1') {
      errors.push('templates/skills/reference-only.json: invalid or missing schema');
    }
    if (!Array.isArray(manifest.items)) {
      errors.push('templates/skills/reference-only.json: items must be an array');
    } else {
      for (const [index, item] of manifest.items.entries()) {
        const label = `templates/skills/reference-only.json items[${index}]`;
        if (!item || typeof item !== 'object' || Array.isArray(item)) {
          errors.push(`${label}: item must be an object`);
          continue;
        }
        if (!item.path) errors.push(`${label}: path is required`);
        if (!item.reason) errors.push(`${label}: reason is required`);
        if (!item.reviewed) errors.push(`${label}: reviewed is required`);
        if (item.path) {
          if (referenceOnlyTemplateSkills.has(item.path)) errors.push(`${label}: duplicate path ${item.path}`);
          referenceOnlyTemplateSkills.set(item.path, item);
          if (!fs.existsSync(path.join(root, item.path))) {
            errors.push(`${label}: path does not exist: ${item.path}`);
          }
        }
      }
    }
  }

  for (const skill of listDirs(path.join(root, 'templates', 'skills'))) {
    const p = `templates/skills/${skill}`;
    if (pathCoveredByRegistry(registryPaths, p)) continue;
    if (referenceOnlyTemplateSkills.has(p)) {
      warnings.push(`reference-only template skill: ${p}`);
    } else {
      warnings.push(`unregistered template skill: ${p}`);
    }
  }

  if (strictCoverage) {
    for (const warning of warnings) {
      if (warning.startsWith('unregistered ')) errors.push(warning);
    }
  }

  if (warnings.length) {
    console.log('WARNINGS');
    for (const warning of warnings) console.log(`- ${warning}`);
    console.log('');
  }

  if (errors.length) {
    console.error('ERRORS');
    for (const error of errors) console.error(`- ${error}`);
    process.exit(1);
  }

  console.log(`OK: ${caps.length} capabilities validated`);
  if (warnings.length) console.log(`Warnings: ${warnings.length}`);
}

main();
