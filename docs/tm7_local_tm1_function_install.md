# TM7-Local TM1-Function Boot Router Install

> Scope: install the boot-router pattern for TM7-local when it covers the TM1
> function, without creating a separate `CodexTM1` identity and without
> copying TM7-vps state.

## Goal

TM7-local should inherit the portable boot-router pattern from `d-nd-seed`,
then adapt it to its own local project paths, memory files, context window and
field surfaces when it operates in TM1-function coverage.

This is not a clone of TM7-vps and not a new TM1 identity. It is TM7-local
covering a function.

```text
d-nd-seed = invariant pattern
TM7-local = local adapter and local truth
CodexTM1 = shorthand for TM7-local while covering TM1 function
TM1-function = role/function covered by TM7-local when needed
existing TM1 memory = compatibility/source surface for TM1 work, not identity transfer
```

## Before Installing

From the local TM7 workspace, verify:

```bash
pwd
git status --short --branch
```

Then locate existing local memory and boot files. Common candidates:

```bash
find . -maxdepth 3 \( -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'MEMORY.md' -o -name '*BOOT*' -o -name '*STATE*' \) 2>/dev/null
```

Do not overwrite them blindly.

## Read From Seed

Read these files in `d-nd-seed`:

```text
docs/boot_router.md
docs/crystallization.md
docs/memory_single_source.md
docs/OPERATIONAL_MATURITY.md
GUIDE.md
```

If the local node is a coding agent that reads `AGENTS.md`, add a short local
adapter there. If it reads `CLAUDE.md`, add the adapter there instead. If both
exist, choose one as primary and point the other to it. Name the adapter as
TM7-local in TM1-function coverage, not as a separate `CodexTM1` node.

## Local Adapter Contract

Add a local section named `Boot Router` with this shape:

```markdown
## Boot Router

Before broad work, classify the transition:

- `new_instance`
- `post_compact`
- `post_crash`
- `unexpected_correction`
- `field_reentry`
- `pre_compact`
- `unclassified`

Default gates:

- unknown/small signal -> `unclassified`, observe only
- new instance/day start -> stop after boot report and wait for validation
- post-crash -> diagnose side effects before rerun
- post-compact -> reconcile compact summary with local memory and repo state
- field reentry -> observe field before editing
- pre-compact -> preserve active point, why/how, evidence, deep sources,
  residue, boundary and next exact read

Context window dynamics:

- early/mid window: accumulate; do not write memory noise
- around 75-80%: structure how/why and deep-source pointers
- near limit: write compact-ready handoff before broad work

Never treat the latest packet, newest dirty file, or compact summary as the
truth by itself.
```

## Local Files To Create

Create only if they do not already exist:

```text
.codex/boot_router.md
.codex/active_context.md
.codex/field_boots/
```

If the project already uses `.claude/`, use:

```text
.claude/boot_router.md
.claude/hooks/active_context.md
.claude/field_boots/
```

The local `boot_router.md` should point to the local sources of truth, not to
TM7-vps paths.

## Minimal Local `boot_router.md`

```markdown
# Local Boot Router

Source pattern: d-nd-seed/docs/boot_router.md

## Local Sources

- identity:
- current state:
- project memory:
- active context:
- field maps:
- test command:
- deploy/run command:

## Local Boot Classes

Use the seed boot classes unchanged.

## Context Window

- limit:
- structure threshold:
- handoff threshold:

## Field Boots

- main project:
- docs/site:
- runtime/service:
- tests:

## Boundary

Boot observes and classifies. It does not deploy, commit, sync, delete, or
read secrets.
```

## Optional Executable Router

An executable router is useful but not mandatory. If added, keep it local and
small:

```bash
python3 .codex/boot_router.py --signal "<operator signal>" --context-tokens "<approx>"
```

It should output:

```text
boot_class:
context_phase:
field_modules:
required_commands:
action_gate:
stop_condition:
```

Do not hard-code another node's paths. The local router must read local paths.

## Validation Matrix

Before declaring installed, test the local trigger matrix:

```text
continua                         -> unclassified / observe_only
ok                               -> unclassified / observe_only
buongiorno / boot                -> new_instance / stop_for_validation
post compact                     -> post_compact / stop_for_validation
pre compact                      -> pre_compact / observe_only
crash / timeout                  -> post_crash / diagnose_only
unsafe / presumptive correction  -> unexpected_correction / stop_for_validation
named local field                -> field_reentry / observe_only
```

Also test context phases at local thresholds:

```text
low        -> accumulate
mid        -> light_realign
high       -> structure_for_compact
near limit -> handoff_now
```

## First TM7-Local TM1-Function Boot After Install

Run:

```bash
git status --short --branch
```

Then produce a boot report:

```text
role/function:
boot_class:
local sources read:
verified:
memory:
inferred:
residue:
active point:
boundary:
validation needed:
```

Stop there unless the operator explicitly authorizes action.

## What Not To Do

- Do not copy TM7-vps current state.
- Do not copy private packets.
- Do not copy secrets, tokens, cookies, env files or service unit bodies.
- Do not replace existing TM1 memory with seed docs.
- Do not create a fake `CodexTM1` identity. The local node remains TM7-local.
- Do not make packet writing mandatory for every session.
- Do not let the router interrupt every normal linear task.

## Promotion Back To Seed

After several real local uses, record what changed:

```text
trigger:
context phase:
router recommendation:
action taken:
reentry result:
what was missing:
what was noise:
```

Only promote patterns that repeatedly improve recovery or prevent regression.
