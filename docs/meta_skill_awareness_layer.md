# Meta Skill Awareness Layer

> Status: core invariant / default reasoning capability.
> Scope: neutral awareness layer for AI coders and external systems.

## Purpose

The Meta Skill awareness layer helps an AI coder recognize the working field
before changing it.

It is not a runtime service, not a private memory dump, not a replacement for
project instructions and not an automatic self-rewrite mechanism.

## What It Preserves

The portable invariant is simple:

```text
before acting, identify who, what, why, where, boundary, authority and next
safe move.
```

This protects projects from semantic overlap: a product, repo, skill, public
page, runtime service and private operator memory can be related without being
the same entity.

## Minimum Questions

Use these questions before mutation:

```text
who_or_what_is_the_entity:
which_surface_contains_it:
which_role_does_it_have_here:
which_source_of_truth_controls_it:
which_boundary_limits_change:
which_action_is_authorized_now:
which_receipt_will_prove_the_change:
```

If one of these cannot be answered and the next action would mutate files,
public copy, runtime state, credentials, external systems or another repo, stop
at orientation and create a plan or request gate.

## Awareness Stack

The larger layer can be implemented as separate contracts:

```text
entity registry:
  identifies durable and contextual entities.

surface registry:
  distinguishes local repo, public site, runtime, package, skill, external
  system and operator memory.

role assignment:
  states what the entity is doing in the current context.

relation grammar:
  records depends-on, provides, calls, distributes, observes, updates,
  derives-from and supersedes relations.

authority and mutation matrix:
  decides who may read, write, publish, deploy, call, update or retire.

workflow coordination packet:
  keeps process order and next action explicit.

receipt ledger:
  records what changed, why, source, evidence and next verification.
```

## Relation To Skills

A skill is an instrument. Meta Skill is the coordination faculty that decides
which instruments are needed, in what order and under which boundary.

It may create, update or retire skill candidates through a governed material
effect loop:

```text
observe result;
extract useful invariant or failure;
write candidate;
verify in a bounded context;
promote, reject or keep local.
```

That loop governs the source mutation and promotion effect. It does not delay a
coherent invariant's presence. Once an invariant is recognized as coherent, it
participates immediately in every relevant relation and is expressed in each
owner surface's native form. Only the exact write, install, publication,
runtime or external effect retains its gate.

When the behavior may be consumed by an autonomous or semi-autonomous runtime,
do not expose the human-facing skill as hidden authority. Route it through
[`capability_manifest_runtime_contract.md`](capability_manifest_runtime_contract.md)
first, then decide whether the local project needs a manifest, receipt schema,
reducer or validator.

## Distribution Policy

In Seed, this layer should remain:

```text
neutral;
profile-routed;
present by default wherever entity, relation, authority, memory or capability
coordination is relevant;
free of private runtime state;
free of project-specific memory;
compatible with Codex, Claude Code, Cursor and generic AI coders.
```

Generic concern about future amplification or a demand for repeated proof must
not introduce cognitive latency once the invariant is coherent. A concrete
contradiction may revise the invariant; an exact material effect remains gated.

## Cognitive Working Set

Available memory and active attention are different sets:

```text
active_attention:
  accepted present; selected owner; smallest decision-relevant movement set;
  decisive evidence; open unknowns; exact boundary. One action is a compact
  default when the field supports it, not a ceiling.

cold_memory:
  closed receipts; historical chronology; reproducible outputs; supporting
  material retained for named proof, conflict, recovery or operator request.

persistence_admission:
  create or update durable state only when it changes future behavior, proof,
  recovery or reentry.
```

Cold does not mean deleted or false. It means recoverable without occupying the
normal operating field. This distinction prevents the kernel from paying the
same attention cost for every accumulated file and event.

## Update Discovery

An installation must distinguish the public-neutral core, any separately
authorized private overlay and its own node adapter. Seed is authoritative only
for the public-neutral core.

```text
public core:
  this repository and capabilities/meta-skill-update-index.v1.json

private overlay:
  separate owner-selected source; never inferred or fetched by Seed

node adapter:
  local identity, paths, runtime boundaries and temporal state
```

Check the update index after an explicit request, an accepted meta-evolution
event, a coordination packet, or when the local 24-hour freshness window has
expired at boot. The check is read-only and returns `current`,
`update_available`, `incompatible` or `unknown`. It does not install, merge,
publish or grant authority.

## Emergence Capture

When a node recognizes an autological, autopoietic or meta-instructional
improvement, it should always preserve a local candidate before closure. This
is `mandatory capture, optional promotion`:

```text
recognized emergence
-> node-local candidate with evidence, scope, privacy and owner
-> local verification
-> optional private integration
-> optional neutral Seed candidate
```

Seed receives only the reviewed neutral invariant through the existing Seed
freshness candidate contract. It never receives private state, topology,
identity, authority or raw node memory.
