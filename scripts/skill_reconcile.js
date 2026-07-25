#!/usr/bin/env node
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const repoRoot = path.resolve(__dirname, '..');
const stateSchema = 'dnd.seed.skill_state.v1';

function sha256(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function pathWithin(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}

function realExisting(filePath, label) {
  if (!fs.existsSync(filePath)) throw new Error(`${label} does not exist: ${filePath}`);
  return fs.realpathSync(filePath);
}

function nearestExistingParent(filePath) {
  let current = path.resolve(filePath);
  while (!fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) throw new Error(`no existing parent for ${filePath}`);
    current = parent;
  }
  return fs.realpathSync(current);
}

function assertDestination(projectRoot, destination, label) {
  const projectReal = realExisting(projectRoot, 'project root');
  const absolute = path.resolve(destination);
  if (!pathWithin(path.resolve(projectRoot), absolute)) {
    throw new Error(`${label} escapes project root: ${destination}`);
  }
  const existingParent = nearestExistingParent(absolute);
  if (!pathWithin(projectReal, existingParent)) {
    throw new Error(`${label} resolves outside project root: ${destination}`);
  }
  if (fs.existsSync(absolute)) {
    const stat = fs.lstatSync(absolute);
    if (stat.isSymbolicLink()) throw new Error(`${label} cannot be a symlink: ${destination}`);
    if (!pathWithin(projectReal, fs.realpathSync(absolute))) {
      throw new Error(`${label} resolves outside project root: ${destination}`);
    }
  }
  return { projectReal, absolute };
}

function listFiles(root) {
  const files = [];
  function walk(current, relativeBase) {
    for (const entry of fs.readdirSync(current, { withFileTypes: true }).sort((a, b) => {
      if (a.name < b.name) return -1;
      if (a.name > b.name) return 1;
      return 0;
    })) {
      const absolute = path.join(current, entry.name);
      const relative = relativeBase ? `${relativeBase}/${entry.name}` : entry.name;
      const stat = fs.lstatSync(absolute);
      if (stat.isSymbolicLink()) throw new Error(`symlinks are not supported in skill trees: ${relative}`);
      if (stat.isDirectory()) walk(absolute, relative);
      else if (stat.isFile()) files.push({ absolute, relative });
      else throw new Error(`unsupported skill tree entry: ${relative}`);
    }
  }
  walk(root, '');
  return files;
}

function hashTree(root) {
  const realRoot = realExisting(root, 'skill tree');
  if (!fs.statSync(realRoot).isDirectory()) throw new Error(`skill tree is not a directory: ${root}`);
  const material = listFiles(realRoot)
    .map(file => `${file.relative}\0${sha256(fs.readFileSync(file.absolute))}\n`)
    .join('');
  return sha256(Buffer.from(material, 'utf8'));
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function loadState(statePath) {
  if (!fs.existsSync(statePath)) {
    return { schema: stateSchema, capabilities: {}, pending: {} };
  }
  const state = readJson(statePath);
  if (state.schema !== stateSchema) throw new Error(`unsupported skill state schema: ${state.schema || 'missing'}`);
  if (!state.capabilities || typeof state.capabilities !== 'object' || Array.isArray(state.capabilities)) {
    throw new Error('skill state capabilities must be an object');
  }
  if (!state.pending || typeof state.pending !== 'object' || Array.isArray(state.pending)) state.pending = {};
  return state;
}

function writeJsonAtomic(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const temp = path.join(path.dirname(filePath), `.${path.basename(filePath)}.${process.pid}.tmp`);
  const backup = path.join(path.dirname(filePath), `.${path.basename(filePath)}.${process.pid}.backup`);
  fs.writeFileSync(temp, `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
  let previousMoved = false;
  try {
    if (fs.existsSync(filePath)) {
      fs.renameSync(filePath, backup);
      previousMoved = true;
    }
    fs.renameSync(temp, filePath);
    if (previousMoved) fs.rmSync(backup, { force: true });
  } catch (error) {
    if (fs.existsSync(temp)) fs.rmSync(temp, { force: true });
    if (previousMoved && fs.existsSync(backup) && !fs.existsSync(filePath)) fs.renameSync(backup, filePath);
    throw error;
  }
}

function safeCapabilityId(value) {
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value || '')) {
    throw new Error(`invalid capability id: ${value || 'missing'}`);
  }
  return value;
}

function sourceContract(seedRoot, source, capabilityId) {
  const seedReal = realExisting(seedRoot, 'Seed root');
  const sourceReal = realExisting(source, 'skill source');
  const expectedParent = path.join(seedReal, 'plugins', 'd-nd-core', 'skills');
  if (!pathWithin(expectedParent, sourceReal) || path.basename(sourceReal) !== capabilityId) {
    throw new Error(`skill source is not the selected Seed capability: ${source}`);
  }
  return { seedReal, sourceReal, sourceRelative: path.relative(seedReal, sourceReal).split(path.sep).join('/') };
}

function planSkill(options) {
  const capabilityId = safeCapabilityId(options.capabilityId);
  const { projectReal, absolute: target } = assertDestination(options.projectRoot, options.target, 'skill target');
  if (path.basename(target) !== capabilityId) throw new Error('skill target basename must match capability id');
  const { seedReal, sourceReal, sourceRelative } = sourceContract(options.seedRoot || repoRoot, options.source, capabilityId);
  const stateLocation = options.statePath || path.join(projectReal, '.seed', 'seed_skill_state.json');
  const { absolute: statePath } = assertDestination(projectReal, stateLocation, 'skill state');
  const state = loadState(statePath);
  const sourceHash = hashTree(sourceReal);
  const entry = state.capabilities[capabilityId] || null;
  let targetHash = null;
  let classification;
  let action;

  if (!fs.existsSync(target)) {
    classification = 'new';
    action = 'install';
  } else {
    targetHash = hashTree(target);
    if (!entry) {
      classification = 'baseline_unknown';
      action = 'stage_review';
    } else if (targetHash !== entry.installed_tree_sha256) {
      classification = 'locally_modified';
      action = 'stage_review';
    } else if (sourceHash === entry.source_tree_sha256) {
      classification = 'unchanged';
      action = 'none';
    } else {
      classification = 'upstream_changed';
      action = 'replace_atomically';
    }
  }

  const registry = readJson(path.join(seedReal, 'capabilities', 'registry.json'));
  const planSha256 = options.planPath && fs.existsSync(options.planPath)
    ? sha256(fs.readFileSync(options.planPath))
    : null;
  return {
    schema: 'dnd.seed.skill_reconcile_plan.v1',
    capability_id: capabilityId,
    classification,
    action,
    source_tree_sha256: sourceHash,
    target_tree_sha256: targetHash,
    recorded_baseline_sha256: entry?.installed_tree_sha256 || null,
    registry_version: registry.version,
    plan_sha256: planSha256,
    source_path: sourceRelative,
    target_path: path.relative(projectReal, target).split(path.sep).join('/'),
    state_path: path.relative(projectReal, statePath).split(path.sep).join('/'),
    _paths: { projectReal, sourceReal, target, statePath },
    _state: state
  };
}

function copyTreeAtomic(source, destination) {
  const parent = path.dirname(destination);
  fs.mkdirSync(parent, { recursive: true });
  const stage = path.join(parent, `.${path.basename(destination)}.dnd-seed-stage-${process.pid}-${crypto.randomBytes(5).toString('hex')}`);
  fs.cpSync(source, stage, { recursive: true, errorOnExist: true, force: false });
  return stage;
}

function stateEntry(plan) {
  return {
    source_path: plan.source_path,
    target_path: plan.target_path,
    source_tree_sha256: plan.source_tree_sha256,
    installed_tree_sha256: plan.source_tree_sha256,
    registry_version: plan.registry_version,
    plan_sha256: plan.plan_sha256
  };
}

function persistInstalledState(plan) {
  plan._state.schema = stateSchema;
  plan._state.registry_version = plan.registry_version;
  plan._state.plan_sha256 = plan.plan_sha256;
  plan._state.capabilities[plan.capability_id] = stateEntry(plan);
  delete plan._state.pending[plan.capability_id];
  writeJsonAtomic(plan._paths.statePath, plan._state);
}

function installNew(plan) {
  const stage = copyTreeAtomic(plan._paths.sourceReal, plan._paths.target);
  try {
    fs.renameSync(stage, plan._paths.target);
    try {
      persistInstalledState(plan);
    } catch (error) {
      fs.rmSync(plan._paths.target, { recursive: true, force: true });
      throw error;
    }
  } finally {
    if (fs.existsSync(stage)) fs.rmSync(stage, { recursive: true, force: true });
  }
}

function replaceAtomically(plan) {
  const stage = copyTreeAtomic(plan._paths.sourceReal, plan._paths.target);
  const backup = path.join(
    path.dirname(plan._paths.target),
    `.${path.basename(plan._paths.target)}.dnd-seed-backup-${process.pid}-${crypto.randomBytes(5).toString('hex')}`
  );
  let targetMoved = false;
  try {
    fs.renameSync(plan._paths.target, backup);
    targetMoved = true;
    fs.renameSync(stage, plan._paths.target);
    try {
      persistInstalledState(plan);
    } catch (error) {
      fs.rmSync(plan._paths.target, { recursive: true, force: true });
      fs.renameSync(backup, plan._paths.target);
      targetMoved = false;
      throw error;
    }
    fs.rmSync(backup, { recursive: true, force: true });
    targetMoved = false;
  } catch (error) {
    if (fs.existsSync(stage)) fs.rmSync(stage, { recursive: true, force: true });
    if (targetMoved && fs.existsSync(backup) && !fs.existsSync(plan._paths.target)) {
      fs.renameSync(backup, plan._paths.target);
    }
    throw error;
  }
}

function stageForReview(plan) {
  const incoming = path.join(
    plan._paths.projectReal,
    '.seed',
    'incoming',
    'skills',
    plan.capability_id,
    plan.source_tree_sha256
  );
  assertDestination(plan._paths.projectReal, incoming, 'incoming skill review path');
  let staged = false;
  if (fs.existsSync(incoming)) {
    if (hashTree(incoming) !== plan.source_tree_sha256) {
      throw new Error(`incoming review path exists with unexpected content: ${incoming}`);
    }
  } else {
    const stage = copyTreeAtomic(plan._paths.sourceReal, incoming);
    try {
      fs.renameSync(stage, incoming);
      staged = true;
    } finally {
      if (fs.existsSync(stage)) fs.rmSync(stage, { recursive: true, force: true });
    }
  }
  plan._state.pending[plan.capability_id] = {
    classification: plan.classification,
    source_tree_sha256: plan.source_tree_sha256,
    staged_path: path.relative(plan._paths.projectReal, incoming).split(path.sep).join('/'),
    registry_version: plan.registry_version,
    plan_sha256: plan.plan_sha256
  };
  writeJsonAtomic(plan._paths.statePath, plan._state);
  return { incoming, staged };
}

function publicPlan(plan) {
  const { _paths, _state, ...result } = plan;
  return result;
}

function reconcileSkill(options) {
  const plan = planSkill(options);
  const mode = options.mode || 'plan';
  const result = publicPlan(plan);
  result.writes_files = false;

  if (mode === 'plan' || mode === 'dry-run') {
    result.action = mode === 'dry-run' && plan.action !== 'none' ? `would_${plan.action}` : plan.action;
    return result;
  }
  if (mode !== 'apply') throw new Error(`unsupported mode: ${mode}`);

  if (plan.classification === 'new') {
    installNew(plan);
    result.writes_files = true;
  } else if (plan.classification === 'upstream_changed') {
    replaceAtomically(plan);
    result.writes_files = true;
  } else if (plan.classification === 'baseline_unknown' || plan.classification === 'locally_modified') {
    const staged = stageForReview(plan);
    result.action = staged.staged ? 'staged_for_review' : 'review_stage_already_current';
    result.review_path = path.relative(plan._paths.projectReal, staged.incoming).split(path.sep).join('/');
    result.writes_files = true;
  }
  return result;
}

function auditRemoved(statePath, selectedPathsFile) {
  const state = loadState(statePath);
  const selected = new Set();
  if (selectedPathsFile && fs.existsSync(selectedPathsFile)) {
    for (const line of fs.readFileSync(selectedPathsFile, 'utf8').split(/\r?\n/)) {
      const match = line.trim().match(/^plugins\/d-nd-core\/skills\/([a-z0-9-]+)$/);
      if (match) selected.add(match[1]);
    }
  }
  return {
    schema: 'dnd.seed.skill_selection_audit.v1',
    selection_removed: Object.keys(state.capabilities).filter(id => !selected.has(id)).sort(),
    deletes_files: false
  };
}

function parseArgs(argv) {
  const options = { mode: 'plan' };
  for (const arg of argv) {
    if (arg === '--apply') options.mode = 'apply';
    else if (arg === '--dry-run') options.mode = 'dry-run';
    else if (arg === '--audit-selection') options.auditSelection = true;
    else if (arg.startsWith('--seed-root=')) options.seedRoot = arg.slice(12);
    else if (arg.startsWith('--project=')) options.projectRoot = arg.slice(10);
    else if (arg.startsWith('--source=')) options.source = arg.slice(9);
    else if (arg.startsWith('--target=')) options.target = arg.slice(9);
    else if (arg.startsWith('--state=')) options.statePath = arg.slice(8);
    else if (arg.startsWith('--capability=')) options.capabilityId = arg.slice(13);
    else if (arg.startsWith('--plan=')) options.planPath = arg.slice(7);
    else if (arg.startsWith('--selected-paths=')) options.selectedPathsFile = arg.slice(17);
    else throw new Error(`unknown option: ${arg}`);
  }
  return options;
}

function main() {
  try {
    const options = parseArgs(process.argv.slice(2));
    if (options.auditSelection) {
      if (!options.statePath) throw new Error('--state is required for selection audit');
      console.log(JSON.stringify(auditRemoved(options.statePath, options.selectedPathsFile), null, 2));
      return;
    }
    for (const key of ['projectRoot', 'source', 'target', 'capabilityId']) {
      if (!options[key]) throw new Error(`--${key} is required`);
    }
    console.log(JSON.stringify(reconcileSkill(options), null, 2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) main();

module.exports = {
  auditRemoved,
  hashTree,
  loadState,
  planSkill,
  reconcileSkill,
  stateSchema
};
