# Boot System Map

> Scope: portable organic map for boot routers, operational plans, local
> adapters and maintenance hygiene.

## Purpose

The boot system keeps an AI coding node from acting out of stale memory,
compressed context, packet recency, or ambiguous operator signals.

It is not a bigger instruction list. It is a small operating structure:

```text
identity -> transition -> map -> continuity -> field -> particular -> gate
```

The system should explain itself to a new instance before that instance edits,
commits, deploys, cleans, or continues work.

## Levels

### Local Adapter

The local adapter is the node-specific implementation.

It owns:

- real paths;
- local memory files;
- local active context;
- local field boot tools;
- local service/repo checks;
- local context window and validation policy.

It may contain node-specific names and paths. It should not be copied as a
portable invariant.

### Portable Seed

The seed owns the invariant pattern:

- boot classes;
- action gates;
- context-window dynamics;
- operational-plan shape;
- hygiene-before-cleanup policy;
- installation guidance.

The seed does not own a node's current state, packet archive, secrets, dirty
repo facts, or runtime paths.

### Local Function Adapter

A node may temporarily cover another function. The local identity remains the
same; only the function changes.

When adapting a seed pattern to a local function:

- name the real local node;
- name the function it covers;
- read compatibility sources;
- avoid creating a fake new identity;
- do not overwrite existing memory.

## Modules

### Boot Router

Classifies the transition and selects awareness modules.

It answers:

```text
what kind of reentry is this?
what needs to be read before action?
what is the default gate?
```

It does not decide the project task.

### Field Boot

Observes the named surface.

Examples:

- site field;
- runtime/service field;
- seed/docs field;
- maintenance/custodian field;
- local function adapter field.

A field boot should be read-only unless the operator has already validated a
specific action.

### Operational Plan

Carries work after awareness.

Use it when work spans files, repos, services, nodes, compact boundaries, or
ambiguous residue.

```text
awareness -> plan -> one work unit -> verification -> plan update -> closure
```

### Hygiene Report

Classifies residue before cleanup.

It should identify:

- active context versus latest visible packet;
- dirty repo buckets;
- generated/runtime data;
- packet density;
- custodian report status;
- suggested autonomy tier.

Cleanup comes after classification.

## Action Gates

```text
observe_only
  read and report only

stop_for_validation
  report state and wait

diagnose_only
  inspect side effects before rerun

one_bounded_action
  one verified, reversible action

escalate
  secrets, irreversible changes, deploy/runtime, or authority conflict
```

## Field Registry Shape

A local router should keep field definitions small:

```json
{
  "field": "example",
  "markers": ["example", "repo-name", "service-name"],
  "command": "read-only command",
  "source": "primary local source"
}
```

Do not route broad fields to write commands.

## Completion Criteria

A boot system is complete enough for a local node when:

1. the boot classes are documented;
2. router output is tested against a trigger matrix;
3. field boots exist for currently active real fields;
4. compact/context behavior is advisory and calibrated;
5. operational-plan use is explained;
6. maintenance starts with hygiene, not deletion;
7. local identity/function boundaries are explicit;
8. promotion from local adapter to seed keeps only invariants.

## Non-Goals

- no automatic deletion of ambiguous memory;
- no secret reads;
- no deploy/restart from boot;
- no copying local packets into the seed;
- no fake identity creation;
- no full audit when a small scoped boot is enough.
