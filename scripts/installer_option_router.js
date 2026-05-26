#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const riskRank = {
  safe: 0,
  writes_files: 1,
  uses_network: 2,
  uses_secrets: 3,
  publishes: 4,
  runtime: 5,
  destructive: 6
};

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function parseArgs(argv) {
  const args = { profile: null, json: false, paths: false, mode: null, intents: [], risk: null };
  for (const arg of argv) {
    if (arg === '--json') args.json = true;
    else if (arg === '--paths') args.paths = true;
    else if (arg.startsWith('--mode=')) args.mode = arg.slice('--mode='.length);
    else if (arg.startsWith('--intent=')) args.intents.push(...arg.slice('--intent='.length).split(',').filter(Boolean));
    else if (arg.startsWith('--risk=')) args.risk = arg.slice('--risk='.length);
    else if (!arg.startsWith('--') && !args.profile) args.profile = arg;
  }
  return args;
}

function resolveProfile(profileArg) {
  if (!profileArg) throw new Error('Missing profile path');
  const direct = path.resolve(process.cwd(), profileArg);
  const inProfiles = path.join(root, 'profiles', profileArg);
  const inProfilesJson = path.join(root, 'profiles', `${profileArg}.json`);
  for (const p of [direct, inProfiles, inProfilesJson]) {
    if (fs.existsSync(p)) return p;
  }
  throw new Error(`Profile not found: ${profileArg}`);
}

function values(input) {
  if (!input) return [];
  return Array.isArray(input) ? input.map(String) : String(input).split(',').map(s => s.trim()).filter(Boolean);
}

function inferProfiles(profile) {
  const inferred = new Set(values(profile.profile || profile.profiles));
  const id = String(profile.node_id || '').toLowerCase();
  const desc = String(profile.description || '').toLowerCase();
  const plugins = values(profile.plugins);

  if (inferred.size === 0) inferred.add('coder');
  if (id.includes('research') || desc.includes('research') || plugins.includes('researcher') || profile.researcher) inferred.add('researcher');
  if (id.includes('dev') || String(profile.vps_url || '').includes('localhost')) inferred.add('dev-node');
  if (id.includes('lab') || desc.includes('lab') || profile.researcher) inferred.add('lab');
  if (id.includes('publish') || desc.includes('site') || desc.includes('copy')) inferred.add('publisher');
  if (id.includes('operator') || desc.includes('operator')) inferred.add('operator');
  if (String(profile.sinapsi_for || '').trim()) inferred.add('team');
  return [...inferred];
}

function inferIntents(profile, cliIntents) {
  const inferred = new Set([...values(profile.intent), ...values(profile.intents), ...cliIntents]);
  const desc = String(profile.description || '').toLowerCase();
  const plugins = values(profile.plugins);

  if (inferred.size === 0) inferred.add('coding');
  if (profile.researcher || plugins.includes('researcher') || desc.includes('research')) inferred.add('research');
  if (profile.researcher || desc.includes('lab')) inferred.add('lab');
  if (String(profile.sinapsi_for || '').trim()) inferred.add('inter-node');
  if (desc.includes('site') || desc.includes('copy')) inferred.add('site');
  if (profile.godel?.enabled || plugins.includes('godel')) inferred.add('inversion');
  return [...inferred];
}

function allowedRisk(risk) {
  return riskRank[risk] ?? riskRank.writes_files;
}

function matchAny(needles, haystack) {
  return needles.some(v => haystack.includes(v));
}

function classify(cap, ctx) {
  const riskOk = allowedRisk(cap.risk) <= ctx.riskLimit;
  const profileMatch = matchAny(ctx.profiles, cap.profiles || []);
  const intentMatch = matchAny(ctx.intents, cap.intents || []);
  const requestedPlugins = values(ctx.profile.plugins);
  const hasSuperseder = Boolean(cap.superseded_by);
  const hidden = cap.visibility === 'hidden' || cap.maturity === 'deprecated' || cap.stratum === 'legacy_or_superseded' || hasSuperseder;

  if (cap.id === 'godel' && !ctx.profile.godel?.enabled && !requestedPlugins.includes('godel')) {
    return ['available', 'Godel is not enabled in this profile'];
  }
  if (cap.id === 'researcher-plugin' && !ctx.profile.researcher && !requestedPlugins.includes('researcher')) {
    return ['available', 'researcher plugin is not enabled in this profile'];
  }

  if (hidden && ctx.mode !== 'migration') {
    return ['hidden', 'legacy, deprecated, or superseded; use migration mode to inspect'];
  }
  if (!riskOk) {
    return ['withheld', `risk ${cap.risk} exceeds tolerance ${ctx.risk}`];
  }

  if (ctx.mode === 'minimal') {
    return cap.stratum === 'core_invariant'
      ? ['included', 'core invariant required for minimal install']
      : ['available', 'not part of minimal install'];
  }

  if (ctx.mode === 'migration') {
    if (hidden || hasSuperseder) return ['included', 'migration/recovery review item'];
    return ['available', 'not a migration-only item'];
  }

  if (ctx.mode === 'recent') {
    if (cap.stratum === 'core_invariant') return ['included', 'core invariant'];
    if (cap.stratum === 'recent_candidate' && (profileMatch || intentMatch)) return ['included', 'recent candidate matching this context'];
    if (cap.stratum === 'stable_default' && (profileMatch || intentMatch)) return ['included', 'stable default matching this context'];
    if (profileMatch || intentMatch) return ['available', 'matches context but is not recent/default'];
    return ['available', 'does not match this profile/intent strongly'];
  }

  if (ctx.mode === 'expert') {
    if (profileMatch || intentMatch || cap.stratum === 'core_invariant') return ['included', 'expert mode exposes matching non-hidden capability'];
    return ['available', 'non-hidden advanced review item'];
  }

  if (ctx.mode === 'contextual') {
    if (cap.stratum === 'core_invariant') return ['included', 'core invariant'];
    if ((cap.stratum === 'stable_default' || cap.stratum === 'contextual') && (profileMatch || intentMatch)) {
      return ['included', 'matches selected profile or intent'];
    }
    if (cap.stratum === 'recent_candidate' && (profileMatch || intentMatch)) return ['available', 'recent candidate; opt in after review'];
    return ['available', 'not selected for this context'];
  }

  if (cap.stratum === 'core_invariant') return ['included', 'core invariant'];
  if (cap.stratum === 'stable_default' && (profileMatch || intentMatch)) return ['included', 'stable default matching this context'];
  if (cap.stratum === 'contextual' && cap.visibility === 'recommended' && (profileMatch || intentMatch)) {
    return ['included', 'recommended contextual capability'];
  }
  if (cap.stratum === 'recent_candidate' && (profileMatch || intentMatch)) return ['available', 'recent candidate; opt in after review'];
  if (profileMatch || intentMatch) return ['available', 'matches context but is optional'];
  return ['available', 'not selected for this profile/intent'];
}

function sortCaps(a, b) {
  const strata = { core_invariant: 0, stable_default: 1, contextual: 2, recent_candidate: 3, experimental: 4, legacy_or_superseded: 5 };
  return (strata[a.stratum] ?? 9) - (strata[b.stratum] ?? 9) || a.id.localeCompare(b.id);
}

function plan(profilePath, opts) {
  const profile = readJson(profilePath);
  const registry = readJson(path.join(root, 'capabilities', 'registry.json'));
  const ctx = {
    profilePath,
    profile,
    node_id: profile.node_id || 'UNKNOWN',
    mode: opts.mode || profile.install_mode || 'recommended',
    risk: opts.risk || profile.risk_tolerance || 'writes_files',
    profiles: inferProfiles(profile),
    intents: inferIntents(profile, opts.intents)
  };
  ctx.riskLimit = allowedRisk(ctx.risk);

  const groups = { included: [], available: [], withheld: [], hidden: [] };
  for (const cap of registry.capabilities.slice().sort(sortCaps)) {
    const [bucket, reason] = classify(cap, ctx);
    groups[bucket].push({ ...cap, reason });
  }
  return { registry: registry.version, policy: registry.policy, context: ctx, ...groups };
}

function printText(result) {
  const ctx = result.context;
  console.log('=== D-ND Seed Install Plan ===');
  console.log(`Profile file: ${path.relative(process.cwd(), ctx.profilePath)}`);
  console.log(`Node: ${ctx.node_id}`);
  console.log(`Mode: ${ctx.mode}`);
  console.log(`Profiles: ${ctx.profiles.join(', ')}`);
  console.log(`Intents: ${ctx.intents.join(', ')}`);
  console.log(`Risk tolerance: ${ctx.risk}`);
  console.log(`Registry: ${result.registry}`);
  console.log('');

  const emit = (title, list, max = 1000) => {
    console.log(`${title}:`);
    if (list.length === 0) {
      console.log('  - none');
      console.log('');
      return;
    }
    for (const cap of list.slice(0, max)) {
      console.log(`  - ${cap.id} [${cap.type}, ${cap.stratum}, ${cap.risk}]`);
      console.log(`    ${cap.reason}. ${cap.why}`);
    }
    if (list.length > max) console.log(`  ... ${list.length - max} more`);
    console.log('');
  };

  emit('Will include', result.included);
  emit('Available but not included', result.available, 12);
  emit('Withheld by risk', result.withheld);
  if (ctx.mode === 'migration') emit('Hidden/migration items', result.hidden);
  else console.log(`Hidden legacy/deprecated items: ${result.hidden.length}`);
}

function main() {
  try {
    const opts = parseArgs(process.argv.slice(2));
    const profilePath = resolveProfile(opts.profile);
    const result = plan(profilePath, opts);
    if (opts.paths) {
      for (const cap of result.included) console.log(cap.path);
    } else if (opts.json) console.log(JSON.stringify(result, null, 2));
    else printText(result);
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) main();
