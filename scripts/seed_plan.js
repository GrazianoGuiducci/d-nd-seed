#!/usr/bin/env node
const { spawnSync } = require('child_process');
const path = require('path');

const root = path.resolve(__dirname, '..');
const nodeBin = process.execPath;

process.stdout.on('error', err => {
  if (err.code === 'EPIPE') process.exit(0);
  throw err;
});

function usage() {
  console.log(`D-ND Seed read-only planner

Usage:
  node scripts/seed_plan.js <profile.json> [options]

Options:
  --mode=<mode>                Override install mode for the plan
  --agent=<runtime>            Override agent runtime for the plan
  --intent=<a,b>               Add planning intents
  --risk=<risk>                Override risk tolerance for the plan
  --target-policy=read-only    Validate as read-only (default)
  --target-policy=dry-run      Validate as dry-run, without writing
  --json                       Emit router JSON only
  --paths                      Emit included capability paths only
  --help                       Show this help

This command never writes target files and never calls install.sh/update.sh.`);
}

function parseArgs(argv) {
  const args = {
    profile: null,
    targetPolicy: 'read-only',
    routerArgs: [],
    json: false,
    paths: false,
    help: false
  };

  for (const arg of argv) {
    if (arg === '--help' || arg === '-h') args.help = true;
    else if (arg === '--json') {
      args.json = true;
      args.routerArgs.push(arg);
    } else if (arg === '--paths') {
      args.paths = true;
      args.routerArgs.push(arg);
    } else if (arg.startsWith('--target-policy=')) {
      args.targetPolicy = arg.slice('--target-policy='.length);
    } else if (
      arg.startsWith('--mode=') ||
      arg.startsWith('--agent=') ||
      arg.startsWith('--intent=') ||
      arg.startsWith('--risk=')
    ) {
      args.routerArgs.push(arg);
    } else if (arg.startsWith('--')) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!args.profile) {
      args.profile = arg;
    } else {
      throw new Error(`Unexpected argument: ${arg}`);
    }
  }

  return args;
}

function runScript(scriptRel, scriptArgs, label) {
  const result = spawnSync(nodeBin, [path.join(root, scriptRel), ...scriptArgs], {
    cwd: root,
    encoding: 'utf8'
  });

  if (result.error) {
    throw result.error;
  }

  if (result.status !== 0) {
    if (result.stdout) process.stderr.write(result.stdout);
    if (result.stderr) process.stderr.write(result.stderr);
    throw new Error(`${label} failed`);
  }

  return {
    stdout: result.stdout || '',
    stderr: result.stderr || ''
  };
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    if (args.help) {
      usage();
      return;
    }
    if (!args.profile) {
      usage();
      process.exit(1);
    }
    if (!['read-only', 'dry-run'].includes(args.targetPolicy)) {
      throw new Error('seed_plan.js only supports --target-policy=read-only or --target-policy=dry-run');
    }

    const quiet = args.json || args.paths;

    const registry = runScript('scripts/validate_capability_registry.js', [], 'registry validation');
    const profileResult = runScript(
      'scripts/validate_profile.js',
      [args.profile, `--target-policy=${args.targetPolicy}`, '--json'],
      'profile validation'
    );
    const profile = JSON.parse(profileResult.stdout);
    const router = runScript(
      'scripts/installer_option_router.js',
      [args.profile, ...args.routerArgs],
      'installer option routing'
    );

    if (quiet) {
      process.stdout.write(router.stdout);
      return;
    }

    console.log('=== D-ND Seed Read-Only Plan ===');
    console.log('Runtime boundary: Node planner only; no install/update writer invoked.');
    console.log('');
    process.stdout.write(registry.stdout);
    if (!registry.stdout.endsWith('\n')) console.log('');
    if (profile.warnings.length) {
      console.log('PROFILE WARNINGS');
      for (const warning of profile.warnings) console.log(`- ${warning}`);
      console.log('');
    }
    console.log(`Profile validation: OK (${profile.targetPolicy})`);
    console.log('');
    process.stdout.write(router.stdout);
  } catch (err) {
    console.error(`ERROR: ${err.message}`);
    process.exit(1);
  }
}

main();
