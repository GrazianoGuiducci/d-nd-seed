#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const registryPath = path.join(root, 'capabilities', 'registry.json');

const allowed = {
  targetPolicy: new Set(['read-only', 'dry-run', 'write']),
  installMode: new Set(['minimal', 'recommended', 'contextual', 'recent', 'expert', 'migration']),
  risk: new Set(['safe', 'writes_files', 'uses_network', 'uses_secrets', 'publishes', 'runtime', 'destructive']),
  agentRuntime: new Set(['claude-code', 'codex', 'cursor', 'generic', 'opencode', 'copilot', 'gemini', 'other']),
  mmkSelectionLevel: new Set(['system', 'default', 'environment-selected']),
  missingAttestation: new Set(['plan_only', 'block']),
  writePolicy: new Set(['plan_only', 'target_write'])
};

const shellControl = /[\r\n`$;&|<>]/;

function parseArgs(argv) {
  const args = { profile: null, targetPolicy: 'read-only', json: false, effectiveProjectDir: null, targetOnly: null };
  for (const arg of argv) {
    if (arg === '--json') args.json = true;
    else if (arg.startsWith('--target-policy=')) args.targetPolicy = arg.slice('--target-policy='.length);
    else if (arg.startsWith('--effective-project-dir=')) args.effectiveProjectDir = arg.slice('--effective-project-dir='.length);
    else if (arg.startsWith('--target-only=')) args.targetOnly = arg.slice('--target-only='.length);
    else if (!arg.startsWith('--') && !args.profile) args.profile = arg;
    else throw new Error(`Unknown or duplicate argument: ${arg}`);
  }
  if (args.targetOnly != null && args.profile) throw new Error('--target-only cannot be combined with a profile');
  return args;
}

function resolveProfile(profileArg) {
  if (!profileArg) throw new Error('Missing profile path');
  const candidates = [
    path.resolve(process.cwd(), profileArg),
    path.join(root, 'profiles', profileArg),
    path.join(root, 'profiles', `${profileArg}.json`)
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) return candidate;
  }
  throw new Error(`Profile not found: ${profileArg}`);
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function values(input) {
  if (!input) return [];
  return Array.isArray(input) ? input.map(String) : String(input).split(',').map(s => s.trim()).filter(Boolean);
}

function hasShellControl(value) {
  return shellControl.test(String(value || ''));
}

function isPlaceholderProjectDir(value) {
  const normalized = String(value || '').replace(/\\/g, '/').toLowerCase();
  return normalized === '/path/to/your/project' || normalized.includes('your/project') || normalized.includes('my-project');
}

function pathLooksUnsafe(value) {
  const raw = String(value || '').trim();
  const normalized = raw.replace(/\\/g, '/');
  if (!raw) return 'project_dir is empty';
  if (raw === '/' || raw === '\\') return 'project_dir points to filesystem root';
  if (/^[a-zA-Z]:[\\/]?$/.test(raw)) return 'project_dir points to drive root';
  if (normalized.split('/').includes('..')) return 'project_dir contains parent traversal';
  return null;
}

function canonicalTarget(value) {
  const absolute = path.resolve(process.cwd(), value || '.');
  let existing = absolute;
  const suffix = [];
  while (!fs.existsSync(existing)) {
    const parent = path.dirname(existing);
    if (parent === existing) break;
    suffix.unshift(path.basename(existing));
    existing = parent;
  }
  const realBase = fs.existsSync(existing) ? fs.realpathSync(existing) : existing;
  return path.resolve(realBase, ...suffix);
}

function isInside(parent, candidate) {
  const rel = path.relative(parent, candidate);
  return rel === '' || (!rel.startsWith('..') && !path.isAbsolute(rel));
}

function sameTarget(a, b) {
  const normalize = value => process.platform === 'win32' ? path.normalize(value).toLowerCase() : path.normalize(value);
  return normalize(a) === normalize(b);
}

function validateString(errors, label, value, opts = {}) {
  if (value == null) {
    if (opts.required) errors.push(`${label} is required`);
    return;
  }
  if (typeof value !== 'string' && typeof value !== 'number' && typeof value !== 'boolean') {
    errors.push(`${label} must be scalar`);
    return;
  }
  if (hasShellControl(value)) errors.push(`${label} contains shell-control characters`);
}

function validateProjectTarget(value, targetPolicy, label = 'project_dir') {
  const errors = [];
  const warnings = [];
  validateString(errors, label, value, { required: true });
  const issue = pathLooksUnsafe(value);
  if (issue) errors.push(issue.replace(/^project_dir/, label));

  if (targetPolicy === 'write' && isPlaceholderProjectDir(value)) {
    errors.push(`${label} is a placeholder/example path: ${value}`);
  } else if (isPlaceholderProjectDir(value)) {
    warnings.push(`${label} appears to be an example path: ${value}`);
  }

  let resolved = null;
  try {
    resolved = canonicalTarget(value || '.');
    if (targetPolicy === 'write' && isInside(fs.realpathSync(root), resolved)) {
      errors.push(`${label} resolves to the seed repository or one of its descendants`);
    }
  } catch (error) {
    errors.push(`${label} cannot be resolved safely: ${error.message}`);
  }
  return { errors, warnings, resolved };
}

function validateTargetOnly(value, targetPolicy) {
  const errors = [];
  if (!allowed.targetPolicy.has(targetPolicy)) errors.push(`invalid target policy: ${targetPolicy}`);
  const target = validateProjectTarget(value, targetPolicy, 'effective_project_dir');
  errors.push(...target.errors);
  return {
    targetPolicy,
    effective_project_dir: value,
    resolved_project_dir: target.resolved,
    errors,
    warnings: target.warnings
  };
}

function validateProfile(profile, profilePath, targetPolicy, effectiveProjectDir = null) {
  const errors = [];
  const warnings = [];
  const registry = readJson(registryPath);
  const registryIds = new Set((registry.capabilities || []).map(cap => cap.id));

  if (!allowed.targetPolicy.has(targetPolicy)) {
    errors.push(`invalid target policy: ${targetPolicy}`);
  }

  validateString(errors, 'node_id', profile.node_id, { required: true });

  const installMode = profile.install_mode || 'recommended';
  if (!allowed.installMode.has(installMode)) errors.push(`invalid install_mode: ${installMode}`);

  const risk = profile.risk_tolerance || 'writes_files';
  if (!allowed.risk.has(risk)) errors.push(`invalid risk_tolerance: ${risk}`);

  const agentRuntime = profile.agent_runtime || 'claude-code';
  if (!allowed.agentRuntime.has(agentRuntime)) {
    errors.push(`invalid agent_runtime: ${agentRuntime}`);
  }

  for (const [label, value] of [
    ['description', profile.description || ''],
    ['system_path', profile.system_path || ''],
    ['memory_path', profile.memory_path || ''],
    ['vps_url', profile.vps_url || ''],
    ['sinapsi_for', profile.sinapsi_for || profile.sync_for || '']
  ]) {
    validateString(errors, label, value);
  }

  const profileTarget = validateProjectTarget(profile.project_dir, targetPolicy);
  errors.push(...profileTarget.errors);
  warnings.push(...profileTarget.warnings);
  const projectAbs = profileTarget.resolved;
  let effectiveProjectAbs = null;
  if (effectiveProjectDir != null) {
    const effectiveTarget = validateProjectTarget(effectiveProjectDir, targetPolicy, 'effective_project_dir');
    errors.push(...effectiveTarget.errors);
    warnings.push(...effectiveTarget.warnings);
    effectiveProjectAbs = effectiveTarget.resolved;
    if (projectAbs && effectiveProjectAbs && !sameTarget(projectAbs, effectiveProjectAbs)) {
      errors.push('effective_project_dir does not match profile project_dir');
    }
  }

  if ('repos' in profile && !Array.isArray(profile.repos)) {
    errors.push('repos must be an array');
  }

  for (const [index, repo] of (profile.repos || []).entries()) {
    if (!repo || typeof repo !== 'object' || Array.isArray(repo)) {
      errors.push(`repos[${index}] must be an object`);
      continue;
    }
    validateString(errors, `repos[${index}].name`, repo.name, { required: true });
    validateString(errors, `repos[${index}].path`, repo.path, { required: true });
    validateString(errors, `repos[${index}].branch`, repo.branch || '');
    const repoPathIssue = pathLooksUnsafe(repo.path || '');
    if (repoPathIssue) errors.push(`repos[${index}].path ${repoPathIssue.replace('project_dir ', '')}`);
  }

  for (const key of ['profile', 'profiles', 'intent', 'intents', 'plugins']) {
    for (const [index, value] of values(profile[key]).entries()) {
      validateString(errors, `${key}[${index}]`, value);
    }
  }

  if ('capability_allowlist' in profile) {
    if (!Array.isArray(profile.capability_allowlist)) {
      errors.push('capability_allowlist must be an array');
    } else {
      const seen = new Set();
      for (const [index, value] of profile.capability_allowlist.entries()) {
        validateString(errors, `capability_allowlist[${index}]`, value, { required: true });
        if (seen.has(value)) errors.push(`capability_allowlist contains duplicate id: ${value}`);
        if (!registryIds.has(value)) errors.push(`capability_allowlist contains unknown id: ${value}`);
        seen.add(value);
      }
    }
  }

  const mmkProfile = Object.prototype.hasOwnProperty.call(profile, 'mmk_selection_level');
  if (mmkProfile && (typeof profile.mmk_selection_level !== 'string' || !profile.mmk_selection_level.trim() || !allowed.mmkSelectionLevel.has(profile.mmk_selection_level))) {
    errors.push(`invalid mmk_selection_level: ${profile.mmk_selection_level}`);
  }
  const writePolicy = profile.write_policy || 'target_write';
  if (!allowed.writePolicy.has(writePolicy)) errors.push(`invalid write_policy: ${writePolicy}`);
  if (mmkProfile && writePolicy !== 'plan_only') {
    errors.push('MMK selection profiles must use write_policy plan_only; activation requires a separate owner-gated adapter');
  }
  if (targetPolicy === 'write' && writePolicy === 'plan_only') {
    errors.push('write_policy plan_only forbids write target policy');
  }

  if (mmkProfile && profile.host_capability_policy == null) {
    errors.push('MMK selection profiles require host_capability_policy');
  }
  if (profile.host_capability_policy != null) {
    const policy = profile.host_capability_policy;
    if (typeof policy !== 'object' || Array.isArray(policy)) {
      errors.push('host_capability_policy must be an object');
    } else {
      validateString(errors, 'host_capability_policy.session_attestation', policy.session_attestation, { required: true });
      validateString(errors, 'host_capability_policy.validation_owner', policy.validation_owner, { required: true });
      if (!allowed.missingAttestation.has(policy.on_missing)) {
        errors.push(`invalid host_capability_policy.on_missing: ${policy.on_missing}`);
      }
      for (const key of ['grants_authority', 'persists_attestation']) {
        if (typeof policy[key] !== 'boolean') errors.push(`host_capability_policy.${key} must be boolean`);
      }
      if (!Number.isInteger(policy.max_age_seconds) || policy.max_age_seconds <= 0) {
        errors.push('host_capability_policy.max_age_seconds must be a positive integer');
      }
      if (mmkProfile) {
        if (Number.isInteger(policy.max_age_seconds) && policy.max_age_seconds > 3600) {
          errors.push('MMK host_capability_policy.max_age_seconds must not exceed 3600');
        }
        if (policy.session_attestation !== 'required_for_environment-selected') {
          errors.push('MMK host_capability_policy.session_attestation must be required_for_environment-selected');
        }
        if (policy.validation_owner !== 'mmk_external') {
          errors.push('MMK host_capability_policy.validation_owner must be mmk_external');
        }
        if (policy.on_missing !== 'plan_only') errors.push('MMK host_capability_policy.on_missing must be plan_only');
        if (policy.grants_authority !== false) errors.push('MMK host_capability_policy.grants_authority must be false');
        if (policy.persists_attestation !== false) errors.push('MMK host_capability_policy.persists_attestation must be false');
      }
    }
  }

  const mmkImplicitKeys = ['claude_writer', 'hooks', 'cron', 'polling', 'network', 'global_skills', 'target_writes'];
  if (mmkProfile && profile.implicit_capabilities == null) {
    errors.push('MMK selection profiles require explicit implicit_capabilities=false declarations');
  }
  if (profile.implicit_capabilities != null) {
    if (typeof profile.implicit_capabilities !== 'object' || Array.isArray(profile.implicit_capabilities)) {
      errors.push('implicit_capabilities must be an object');
    } else {
      for (const [key, value] of Object.entries(profile.implicit_capabilities)) {
        if (typeof value !== 'boolean') errors.push(`implicit_capabilities.${key} must be boolean`);
        if (mmkProfile && !mmkImplicitKeys.includes(key)) errors.push(`unknown MMK implicit_capabilities key: ${key}`);
        if (mmkProfile && value !== false) errors.push(`MMK implicit_capabilities.${key} must be false`);
      }
      if (mmkProfile) {
        for (const key of mmkImplicitKeys) {
          if (profile.implicit_capabilities[key] !== false) {
            errors.push(`MMK implicit_capabilities.${key} must be explicitly false`);
          }
        }
      }
    }
  }

  if (profile.godel != null) {
    if (typeof profile.godel !== 'object' || Array.isArray(profile.godel)) {
      errors.push('godel must be an object');
    } else {
      for (const [key, value] of Object.entries(profile.godel)) {
        if (key === 'enabled') continue;
        validateString(errors, `godel.${key}`, value);
      }
    }
  }

  if (profile.researcher != null && (typeof profile.researcher !== 'object' || Array.isArray(profile.researcher))) {
    errors.push('researcher must be an object when present');
  }

  return {
    profilePath,
    targetPolicy,
    node_id: profile.node_id || 'UNKNOWN',
    project_dir: profile.project_dir || '.',
    resolved_project_dir: projectAbs,
    resolved_effective_project_dir: effectiveProjectAbs,
    install_mode: installMode,
    risk_tolerance: risk,
    agent_runtime: agentRuntime,
    mmk_selection_level: profile.mmk_selection_level || null,
    write_policy: writePolicy,
    capability_allowlist: profile.capability_allowlist || null,
    errors,
    warnings
  };
}

function printText(result) {
  if (result.warnings.length) {
    console.log('WARNINGS');
    for (const warning of result.warnings) console.log(`- ${warning}`);
    console.log('');
  }
  if (result.errors.length) {
    console.error('ERRORS');
    for (const error of result.errors) console.error(`- ${error}`);
    process.exit(1);
  }
  console.log(`OK: profile validated (${result.targetPolicy})`);
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.targetOnly != null) {
      const result = validateTargetOnly(args.targetOnly, args.targetPolicy);
      if (args.json) {
        console.log(JSON.stringify(result, null, 2));
        if (result.errors.length) process.exit(1);
      } else {
        printText(result);
      }
      return;
    }
    const profilePath = resolveProfile(args.profile);
    const profile = readJson(profilePath);
    const result = validateProfile(profile, profilePath, args.targetPolicy, args.effectiveProjectDir);
    if (args.json) {
      console.log(JSON.stringify(result, null, 2));
      if (result.errors.length) process.exit(1);
    } else {
      printText(result);
    }
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) main();
