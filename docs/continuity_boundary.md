# Continuity Boundary

> Scope: portable invariant for agentic systems that must survive context
> compaction, session restart, tool change, node handoff, or state transition.

## Principle

Do not assume continuous state.

Agentic continuity is reconstructed at boundaries:

```text
state change -> condensation -> reentry -> verified orientation
```

The useful operating point is the boundary where context, role, memory, tool or
runtime state changes. At that point the system should preserve orientation,
not pretend that nothing changed.

Short form:

```text
continuity = reentry with preserved angle, not uninterrupted state
```

## Collapse Boundary

A boundary appears when raw context can no longer be trusted to carry the whole
system forward:

- context compaction;
- new session;
- crash or interrupted tool;
- operator correction;
- role or surface switch;
- handoff between agents;
- runtime or deployment boundary;
- transition from draft to publication;
- transition from local note to shared memory.

At a boundary, the agent must separate:

```text
verified:
memory:
inferred:
residue:
not_verified:
```

Then it can choose a safe reentry.

## Awareness Crystals

An awareness crystal is not a raw note. It is a condensed unit of operational
orientation that can be consumed later.

Minimum shape:

```text
trigger:
source_tension:
resultant:
preserved_angle:
where_consumed:
how_consumption_is_verified:
expiry_or_supersession:
residue:
```

Without `where_consumed`, the object is a note. With a consumption point and
verification, it can become a behavior.

## Noise Threshold

Do not turn every readback into durable memory.

Use this threshold:

```text
immediate readback = local coordination
durable memory = what the next cycle needs
```

Preserve only what changes future behavior, reduces reentry latency, proves a
rule, prevents regression, or must be consumed by another agent later.

Do not preserve routine confirmations, ordinary progress, unclassified
thoughts, or local residue that does not change a future node's behavior.

## Automation Levels

Automation should be stratified by side effect:

```text
L0 read-only awareness:
  observe, fetch/status if applicable, classify, report, suggest reads

L1 preparation:
  create skeletons, check crystals, prepare packets/checklists/diffs

L2 gated action:
  write, commit, push, publish, promote, clean up, deploy
```

Default boot automation is L0. L1 is allowed when preparing an artifact. L2
requires explicit gate, verified boundary, and side-effect awareness.

## Shared / Distributed Intelligence

Shared intelligence does not require all agents to share one live state.

Portable rule:

```text
local observation -> durable memory object -> readback -> shared procedure
-> consumption proof -> promotion candidate
```

This belongs to a second layer of the architecture. The first layer is boundary
continuity for a single agent. The second layer is convergence across agents or
surfaces without erasing local context.

## Boot Consumption

At boot or reentry, consume this document as a small check:

```text
boundary_detected:
crystals_or_memory_read:
preserved_angle:
noise_threshold_applied:
automation_level:
action_gate:
```

## Boundary

This document does not claim consciousness, physical continuity, or actual
physics-law preservation. It defines an operational model for preserving
orientation across state changes.
