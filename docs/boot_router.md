# Boot Router Pattern

> Version: 0.1
> Scope: portable boot classification for AI coding agents

## Purpose

A mature AI coding node should not treat every reentry as the same event.

New instance, post-compact, post-crash, operator correction, field reentry and
pre-compact handoff have different risks. The boot router is the small layer
that classifies the transition before the agent decides what to read or do.

The router does not replace project memory, hooks, or field-specific boot
tools. It chooses which awareness modules should run before action.

## Boot Stack

```text
00 temporal boot
  -> current time, freshness, transition kind

01 general map boot
  -> identity, territory, source hierarchy, secret boundary

02 continuity boot
  -> last conscious point, residues, validation gaps, active/foreign packets

03 field boot
  -> live territory for the selected surface

04 particular boot
  -> exact file, route, service, dataset, or task evidence

05 action gate
  -> observe, validate, diagnose, act one bounded step, or escalate
```

The general map should enter the particular only when it changes:

- surface ownership;
- source of truth;
- side effects;
- temporal validity;
- residue classification;
- verification procedure;
- known regression prevention.

If it changes none of these answers, it is background orientation and should
not bloat the working context.

## Boot Classes

| Class | Trigger | Default gate | Main risk |
|---|---|---|---|
| `new_instance` | fresh session, day-start, no reliable context | `stop_for_validation` | continuing from memory or latest packet |
| `post_compact` | compressed context, summarized history | `stop_for_validation` | trusting compact summary as complete truth |
| `post_crash` | crash, timeout, interrupted command | `diagnose_only` | rerunning before side effects are bounded |
| `unexpected_correction` | operator says logic is wrong/unsafe | `stop_for_validation` | turning correction into blind doctrine |
| `field_reentry` | user names a field/repo/service/site | `observe_only` | editing before live field is observed |
| `pre_compact` | long task, handoff, expected context loss | `observe_only` | writing too little for the next instance |
| `unclassified` | small/context-dependent signal | `observe_only` | inventing a class or active point |

Do not classify a signal as `post_compact` merely because it discusses compact,
context windows, packet strategy, or maintenance around compaction. Use
`post_compact` only for an actual return from compressed context or compact
summary reconciliation.

## Context Window Dynamics

Context pressure should be advisory, not a rigid interrupt.

For a large 258K window, a useful starting calibration is:

```text
0-150K     accumulate
150-200K   light realign
200-235K   structure for compact
235K+      handoff now
```

Meaning:

- `accumulate`: let work flow. Do not create extra memory unless a reusable
  correction, verified rule, or residue emerges.
- `light_realign`: restate active stack/residue only if work is branching.
- `structure_for_compact`: begin shaping how/why/deep-source pointers.
- `handoff_now`: write continuity before more broad work.

The compact mechanism compresses chat-visible information. It usually does not
see deep layers outside the chat: local docs, source trees, packets, runbooks,
service state, private transcripts, or repository-specific truth. A useful
handoff therefore preserves pointers and logic, not only a story.

## Minimum Pre-Compact Content

```text
active point:
why it matters:
how we got here:
verified evidence:
deep sources to read next:
files/tools changed:
residue not to mistake for active work:
boundary / what was not tested:
next exact read or move:
```

The `why` and `how` are not decoration. They are what lets the next instance
reconstruct the movement from sources instead of guessing from chat fragments.

## Operational Plan Layer

Boot reaches awareness. An operational plan carries the work after awareness.

Use one when a task:

- spans multiple files, repositories, services, or nodes;
- may cross compaction, crash, or a new instance;
- has visible residue that could become the wrong branch;
- requires staged validation;
- needs the `how` and `why` preserved, not only a todo list.

The loop:

```text
awareness -> operational plan -> one work unit -> verification -> plan update
-> next work unit -> closure/handoff
```

Minimum fields:

```text
objective:
why it matters:
system levels involved:
sources already verified:
sources still required:
work units:
verification per unit:
residue and non-goals:
decision gates:
compact/crash recovery point:
completion criteria:
```

This plan is not mandatory for small, linear, low-risk work. In those cases,
letting the task flow normally is often better for performance.

## Trigger Calibration

Trigger rules should be tested like code.

Minimum trigger matrix:

```text
continua                                      -> unclassified / observe_only
ok                                            -> unclassified / observe_only
good morning / boot / start of day            -> new_instance / stop_for_validation
post compact / summarized context             -> post_compact / stop_for_validation
pre compact / handoff                         -> pre_compact / observe_only
crash / timeout / interrupted command          -> post_crash / diagnose_only
unsafe / presumptive / not aware               -> unexpected_correction / stop_for_validation
named field, repo, service, or site            -> field_reentry / observe_only
maintenance / custodian / cleanup             -> field_reentry / observe_only
```

Avoid the common failure modes:

- defaulting unknown signals to `new_instance`;
- treating "continue" as authorization without context;
- making the router call itself recursively;
- forcing a field boot when no field was named or inferable;
- writing packets too often during linear work.

## Portable Router Output

A router report should expose:

```text
boot_class:
transition:
temporal_state:
context_window:
map_modules:
continuity_modules:
field_modules:
required_commands:
stop_condition:
action_gate:
```

For reentry, post-compact, broad awareness, or latest-instance recovery, append
a final autological check:

```text
final_autological_check:
  closest_source_read:
  verified_vs_memory:
  next_move_emerges_from:
  adjacent_regression_risk:
  stop_or_action_gate_confirmed:
```

This turns the router from a mechanical classifier into a short awareness gate.
The agent confirms it read the closest source, separated verified territory
from memory, checked adjacent regression risk, and is not continuing only
because a previous packet said "next".

## Prior-Deposit Review Before Resultant Projection

When a task asks for a public recommendation, strategic position, site/page
direction, portfolio framing, knowledge-safety rule, or any resultant that must
carry the system through a passage, the boot layer should recover relevant
prior deposits before producing the projection.

Minimum review:

```text
active context -> current memory pointer -> relevant handoff/closure notes ->
task-specific docs/private notes -> live repo state ->
verified / memory / inferred / residue split -> projection aligned to now
```

This is not a full historical audit. It is a knowledge-safety pass: search the
places where the relevant past could have been deposited, enough to prevent an
old note, latest artifact, or partial summary from becoming the projected
result.

Action gates:

- `observe_only`: read/report only.
- `stop_for_validation`: report state and wait for operator validation.
- `diagnose_only`: post-crash or unknown side effects.
- `one_bounded_action`: only after verified field and explicit action signal.
- `escalate`: irreversible, secret-bearing, deploy/runtime, or authority conflict.

## Installation Shape

Do not copy one node's local boot files into another node.

Use this pattern to create a local adapter:

```text
project/.codex or project/.claude
  boot_router.md          # local policy
  boot_router.py/sh       # optional executable classifier
  active_context.md       # current continuity
  field_boot_<name>.md    # optional field-specific map
```

The seed provides the invariant. The local node supplies:

- real paths;
- real services;
- local source-of-truth files;
- field boot tools;
- context window size;
- operator-specific validation policy.

## Monitoring

Treat thresholds as calibration, not doctrine.

Track:

- when the router interrupted too early;
- when it failed to interrupt and compact lost meaning;
- whether packets helped reentry;
- whether packets created noise;
- boot time cost versus work value;
- which fields need structure and which work better flowing normally.

Promote only the patterns that repeatedly improve recovery or prevent
regression.

## Hygiene Before Cleanup

When a boot router detects maintenance, custodian, or cleanup intent, the first
tool should be a read-only hygiene report. It should classify:

- active workstream versus latest visible packet;
- dirty repos by known residue bucket;
- generated/runtime data versus source changes;
- packet density and likely reentry noise;
- existing custodian report status;
- suggested autonomy tier.

Cleanup is a later decision. The default policy is:

- `auto`: only reversible, tool-owned rotations with an existing policy;
- `notify`: boot residue, seed promotion, dirty repo interpretation;
- `escalate`: secrets, source-of-truth rewrites, deploy/runtime changes,
  cross-node memory deletion.
