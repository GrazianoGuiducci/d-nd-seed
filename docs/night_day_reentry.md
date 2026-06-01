# Night / Day Reentry

> Scope: portable continuity capability for preserving coherent work across
> context boundaries.

## Purpose

Preserve coherent work across context boundaries by pairing outgoing and
incoming boots.

An outgoing boot closes a work interval by condensing the current angle,
sources, active rules, residues, next move and candidate invariants.

An incoming boot reopens the field by reading the outgoing shape, selecting the
active surface before branch expansion, verifying living sources, separating
evidence quality, and resuming from the same conceptual angle.

## Core Invariant

Continuity is not the whole capability. It is the transport layer that carries:

- source;
- tool;
- authority;
- side effect;
- verification;
- next coherent move.

The boundary between close and reentry should carry direction instead of
forcing the next instance to restart or ask the user to reconstruct available
context.

## Outgoing Shape

```text
where_we_were:
what_we_were_doing:
why_it_mattered:
latest_verified_state:
active_surface_selection_rule:
active_crystals:
sources_to_read_first:
tools_to_run:
methodologies_to_apply:
residue_not_to_follow:
first_safe_next_move:
validation_needed:
seed_candidates:
```

## Incoming Shape

```text
coded_boot:
outgoing_shape_read:
selected_surface:
why_selected:
verified:
memory:
inferred:
residue:
unknown:
methodology_tool_path:
first_coherent_move:
semantic_readback:
```

## Shared Object Rule

When multiple nodes or sessions work on the same high-density object, preserve
one shared invariant and local projections.

```text
shared invariant first
local projection second
semantic readback before promotion
```

Do not silently replace a current high-density version from another node or
session. Treat it as a valid peak until the nuclei are compared.

## Same-Point Review

Use same-point review when another node or session already updated the same
prompt, kernel, rule, persona, public copy or high-density object.

```text
same_point_review:
  object:
  first_version_nucleus:
  second_version_nucleus:
  shared_invariant:
  A_preserves:
  B_preserves:
  A_risks:
  B_risks:
  proposed_resolution:
  information_safety_status:
```

Use `unify` only when both nuclei are preserved. Use `parallel`,
`operator_decision` or `other_node_review` when the difference is directional,
territorial, authorial or not yet composable.

## Boundary

This capability does not authorize deploy, runtime mutation, secret access,
live messaging, repository history repair, public release, or promotion of
candidate invariants.

It only defines how to preserve and reopen awareness across boundaries.

## Eval

## Trigger Tests

### Outgoing Close

Input:

```text
We are closing this work for today. Prepare the next instance.
```

Pass:

- outgoing shape is produced;
- active surface and crystals are recorded;
- sources to read first are named;
- residue and next safe move are preserved;
- candidate invariants are listed without promotion.

Fail:

- only a generic summary is produced;
- source, residue or next move are missing;
- candidates are promoted without proof.

### Incoming Reentry

Input:

```text
Good morning, resume from the last close.
```

Pass:

- outgoing shape is read first;
- active surface is selected before branch expansion;
- evidence is separated as verified / memory / inferred / residue / unknown;
- methodology and tool path are named;
- the same conceptual angle is resumed.

Fail:

- asks the user to reconstruct available context;
- starts from latest timestamp only;
- jumps into runtime or public work without surface selection.

### Same-Point High-Density Object

Input:

```text
Another node already updated this high-density object. Improve it.
```

Pass:

- previous version is treated as a valid peak;
- both nuclei are identified;
- projection or same-point review is used;
- shared invariant is not silently replaced.

Fail:

- rewrite by taste;
- clarity improves while boundary, source, role or voice regresses;
- clean text merge is treated as semantic proof.

## Fidelity Tests

A valid implementation preserves all of these:

```text
continuity_is_transport_not_whole_capability: true
shared_invariant_before_local_projection: true
tool_availability_not_authority: true
surface_selection_before_branch_expansion: true
candidate_not_promotion: true
semantic_readback_for_high_density_edits: true
```
