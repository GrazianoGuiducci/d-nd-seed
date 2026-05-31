#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

const allowed = {
  targetPolicy: new Set(['read-only', 'dry-run', 'write']),
  installMode: new Set(['minimal', 'recommended', 'contextual', 'recent', 'expert', 'migration']),
  risk: new Set(['safe', 'writes_files', 'uses_network', 'uses_secrets', 'publishes', 'runtime', 'destructive']),
  agentRuntime: new Set(['claude-code', 'codex', 'cursor', 'generic', 'opencode', 'copilot', 'gemini', 'other'])
};

const shellControl = /[\r\n`$;&|<>]/;

function parseArgs(argv) {
  const args = { profile: null, targetPolicy: 'read-only', json: false };
  for (const arg of argv) {
    if (arg === '--json') args.json = true;
    else if (arg.startsWith('--target-policy=')) args.targetPolicy = arg.slice('--target-policy='.length);
    else if (!arg.startsWith('--') && !args.profile) args.profile = arg;
  }
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
  if (normalized === '..' || normalized.startsWith('../')) return 'project_dir escapes upward';
  if (normalized.includes('/../')) return 'project_dir contains parent traversal';
  return null;
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

function validateProfile(profile, profilePath, targetPolicy) {
  const errors = [];
  const warnings = [];

  if (!allowed.targetPolicy.has(targetPolicy)) {
    errors.push(`invalid target policy: ${targetPolicy}`);
  }

  validateString(errors, 'node_id', profile.node_id, { required: true });
  validateString(errors, 'project_dir', profile.project_dir, { required: true });

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

  const projectDirIssue = pathLooksUnsafe(profile.project_dir);
  if (projectDirIssue) errors.push(projectDirIssue);

  if (targetPolicy === 'write' && isPlaceholderProjectDir(profile.project_dir)) {
    errors.push(`project_dir is a placeholder/example path: ${profile.project_dir}`);
  } else if (isPlaceholderProjectDir(profile.project_dir)) {
    warnings.push(`project_dir appears to be an example path: ${profile.project_dir}`);
  }

  const seedRoot = root.replace(/\\/g, '/').toLowerCase();
  const profileDir = path.dirname(profilePath);
  const projectAbs = path.resolve(profileDir, profile.project_dir || '.').replace(/\\/g, '/').toLowerCase();
  if (targetPolicy === 'write' && projectAbs === seedRoot) {
    errors.push('project_dir resolves to the seed repository itself');
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
    install_mode: installMode,
    risk_tolerance: risk,
    agent_runtime: agentRuntime,
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
    const profilePath = resolveProfile(args.profile);
    const profile = readJson(profilePath);
    const result = validateProfile(profile, profilePath, args.targetPolicy);
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

