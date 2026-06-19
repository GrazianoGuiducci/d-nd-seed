# Semantic Kernel Entity Contract

> Status: recent candidate / optional Seed contract.
> Scope: neutral contract for systems that need to instantiate a semantic
> kernel without inheriting local project memory, private paths or runtime
> identity.

## Purpose

This contract describes the minimum structure required for a Seed-born entity
to perform work, preserve state, evaluate results and improve its operating
rules through explicit verification gates.

It is not an installer change, not a runtime entity, and not a copy of any
local Codex, Claude, TMx, THIA or project memory.

## Compatibility Rule

The contract is valid only when used as:

```text
additive;
opt-in;
neutral;
registry-routed;
reversible;
single-source.
```

It must not change existing Seed identity, installed default surfaces,
profiles, adapter contracts, installer behavior or package publishing.

## Entity Purpose

A semantic-kernel entity exists to bind work, memory, tools and review gates
into a coherent operating process.

It should be able to:

```text
read intent;
preserve state;
route tools and skills;
evaluate outputs;
turn validated results into reusable rules;
keep unresolved residue explicit;
improve its operating structure only through governed gates.
```

## Identity Minimum

The entity must know:

```text
what it is for;
what it must preserve;
which surface it is operating in;
which boundaries define the field;
which register it is using: internal, private, public or runtime;
which action is the next safe action.
```

Anything beyond this minimum is local state and must remain in the receiving
context unless separately promoted as a portable invariant.

## State Model

The portable state model is:

```text
intent:
active_surface:
source_of_truth:
evidence:
boundary:
working_memory:
residue:
next_safe_action:
KLI_or_learning_item:
verification_needed:
rollback_or_retraction:
```

## Skill Model

Skills are instruments of the kernel. They are not the kernel itself.

```text
operative_skill:
  performs domain work.

metaoperative_skill:
  observes, routes, evaluates, compresses, improves or preserves the system.

promotion_gate:
  decides whether a result becomes rule, residue, packet, interface or Seed
  candidate.

verification_gate:
  proves that the promoted object behaves as intended.
```

## Operative Layer

Operative skills perform work in a selected domain:

```text
write;
inspect;
implement;
communicate;
package;
verify;
translate;
publish only when explicitly authorized by the receiving runtime.
```

Operative skills do not decide by themselves what should become system
structure.

## Metaoperative Layer

Metaoperative skills let the entity read and govern its own operation.

Required metaoperative functions:

```text
continuity_guard:
  preserve the active intent, surface, boundary, evidence and next action.

source_router:
  select the closest source of truth and classify source quality.

boundary_guard:
  separate internal, private, public and runtime registers.

combo_orchestrator:
  assemble tools, files, states, gates and actions as routed capability
  combinations.

result_evaluator:
  classify an output as result, evidence, reusable rule, residue, proof,
  packet or promotion candidate.

compression_guard:
  preserve compact reentry handles without creating redundant archive weight.

capability_evolution_guard:
  decide whether a correction or repeated lesson becomes a state note,
  procedure, skill candidate, capability candidate or Seed candidate.

self_improvement_reviewer:
  compare behavior against intent, evidence and boundary; propose change only
  after proof.
```

The `capability_evolution_guard` is the neutral Seed form of local
skill-evolution practices. It does not copy any local skill package. It
preserves the invariant:

```text
correction / friction / failure
-> candidate rule
-> where_consumed
-> verification_needed
-> bounded behavior change
-> preserve, reject or promote.
```

## Learning And Improvement Loop

The entity may improve only through this loop:

```text
observe result;
compare with intent and boundary;
extract invariant, failure or residue;
update state/rule/capability candidate;
verify;
preserve or reject;
promote to Seed only when the invariant is portable.
```

This loop composes with `docs/governed_self_improvement.md`. It does not
authorize hidden edits, autonomous self-rewrite, deployment, service restarts,
public release or shared memory mutation.

## Neutral Transfer Unit

When a kernel pattern must move into another context, use:

```text
source_signal:
dipole:
singular:
invariant:
possible:
non_possible:
movement_rule:
state_transition:
KLI_or_residue:
interface_needed:
promotion_gate:
verification_required:
rollback_or_retraction:
```

Transfer the movement and the gate, not the local incident.

## Visibility Policy

```text
internal:
  may use kernel terms directly.

private:
  may reference project state only inside the owning context.

public:
  function-first; no private memory, secrets, raw local state or unreviewed
  sensitive register.

runtime:
  exact surface, permissions, tests and rollback path required.
```

## External Contract

External systems interact through documented interfaces and import/export
rules. They do not receive raw entity memory.

Minimum external contract:

```text
inputs:
outputs:
allowed_registers:
state_model:
capability_surface:
verification_path:
rollback_or_retraction:
```

## What Must Not Be Promoted

Do not transfer:

```text
local paths;
operator-only context;
private outreach or business memory;
tokens, credentials or secrets;
raw session logs;
unresolved claims;
runtime-specific implementation assumptions;
chat-only residue;
default installer behavior.
```

Promote only:

```text
invariants;
state transition rules;
skill layer separation;
promotion gates;
verification rules;
rollback or retraction paths;
compact reentry structure.
```

## Consumption

This contract is a recent candidate. A consuming project may read it to design
or evaluate a semantic-kernel entity, but it should not become default runtime
behavior until at least one real consuming context verifies the contract.

If it becomes installable later, route it through `capabilities/registry.json`
as an explicit optional capability.

## Eval

### Trigger Tests

Use this contract when:

- a Seed consumer needs to instantiate a semantic-kernel entity;
- a project needs operative and metaoperative skill separation;
- local lessons need neutral transfer without copying local memory;
- an external system needs a contract for state, review and learning gates.

Do not trigger it for:

- ordinary documentation edits;
- local-only project memory;
- runtime deployment;
- public marketing copy;
- broad sync between nodes.

### Fidelity Tests

Pass when:

- the receiver can state identity minimum, state model and boundary;
- operative and metaoperative skills are separated;
- capability evolution has a verification gate;
- private/local state is not copied;
- rollback or rejection is named;
- the contract remains opt-in and reversible.

Fail when:

- local memory is treated as Seed truth;
- an entity runtime is implied without implementation;
- capability evolution becomes hidden self-modification;
- public copy exposes private state;
- installer behavior changes without explicit promotion.
