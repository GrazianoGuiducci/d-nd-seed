#!/usr/bin/env node
'use strict';

const { defaultRegistryPath, readJson, validateRegistry } = require('./validate_faculty_registry');

function usage() {
  console.log(`Usage:
  node scripts/faculty_plan.js --list
  node scripts/faculty_plan.js --bundle=software
  node scripts/faculty_plan.js --faculty=failure-diagnosis --faculty=deep-module-design
  add --json for machine-readable output

This command is read-only. It selects contracts; it does not activate skills or write target files.`);
}

function values(prefix) {
  return process.argv
    .filter(arg => arg.startsWith(prefix))
    .map(arg => arg.slice(prefix.length))
    .filter(Boolean);
}

function main() {
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    usage();
    return;
  }

  const registry = readJson(defaultRegistryPath);
  const validation = validateRegistry(registry);
  if (validation.errors.length) throw new Error(validation.errors.join('; '));

  const requestedBundles = values('--bundle=');
  const requestedFaculties = values('--faculty=');
  const knownBundles = new Set(Object.keys(registry.bundle_definitions));
  const byId = new Map(registry.faculties.map(faculty => [faculty.id, faculty]));

  for (const bundle of requestedBundles) {
    if (!knownBundles.has(bundle)) throw new Error(`Unknown bundle: ${bundle}`);
  }
  for (const id of requestedFaculties) {
    if (!byId.has(id)) throw new Error(`Unknown faculty: ${id}`);
  }

  if (process.argv.includes('--list')) {
    const list = {
      bundles: registry.bundle_definitions,
      faculties: registry.faculties.map(({ id, title, public_function, bundles, portability, effect_class }) => ({
        id,
        title,
        public_function,
        result_contract: registry.result_contracts[id],
        bundles,
        portability,
        effect_class
      }))
    };
    if (process.argv.includes('--json')) console.log(JSON.stringify(list, null, 2));
    else {
      console.log('Bundles:');
      Object.entries(list.bundles).forEach(([id, description]) => console.log(`  ${id}: ${description}`));
      console.log('\nFaculties:');
      list.faculties.forEach(item => {
        console.log(`  ${item.id} [${item.bundles.join(', ')}]`);
        console.log(`    ${item.public_function}`);
        console.log(`    result=${item.result_contract}`);
      });
    }
    return;
  }

  if (requestedBundles.length === 0 && requestedFaculties.length === 0) {
    usage();
    process.exitCode = 2;
    return;
  }

  const selectedIds = new Set(requestedFaculties);
  registry.faculties.forEach(faculty => {
    if (faculty.bundles.some(bundle => requestedBundles.includes(bundle))) selectedIds.add(faculty.id);
  });
  const selected = registry.faculties
    .filter(faculty => selectedIds.has(faculty.id))
    .map(faculty => ({
      ...faculty,
      result_contract: registry.result_contracts[faculty.id]
    }));
  const gated = selected.filter(faculty => faculty.effect_class !== 'reasoning_only');
  const result = {
    schema: 'dnd.seed.faculty_plan.v1',
    registry: { schema: registry.schema, version: registry.version },
    requested: { bundles: requestedBundles, faculties: requestedFaculties },
    selection_count: selected.length,
    selected,
    gates_required: [...new Set(gated.map(faculty => faculty.effect_class))],
    activates_faculties: false,
    writes_files: false,
    next: 'Choose the smallest coherent faculty composition; one primary with up to three supports is the normal compact profile, not a ceiling. Then apply the target project and runtime gates.'
  };

  if (process.argv.includes('--json')) console.log(JSON.stringify(result, null, 2));
  else {
    console.log(`Faculty plan: ${selected.length} available contracts (no activation)`);
    selected.forEach(faculty => {
      console.log(`  ${faculty.id}`);
      console.log(`    ${faculty.public_function}`);
      console.log(`    result=${faculty.result_contract}`);
      console.log(`    portability=${faculty.portability} effect=${faculty.effect_class}`);
    });
    if (result.gates_required.length) console.log(`Gates: ${result.gates_required.join(', ')}`);
    console.log(`Next: ${result.next}`);
  }
}

try {
  main();
} catch (error) {
  console.error(`ERROR: ${error.message}`);
  process.exit(1);
}
