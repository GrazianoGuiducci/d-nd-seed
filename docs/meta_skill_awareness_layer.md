# Meta Skill Awareness Layer

> Status: recent candidate / optional Seed capability.
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

It may create, update or retire skill candidates only through a governed loop:

```text
observe result;
extract useful invariant or failure;
write candidate;
verify in a bounded context;
promote, reject or keep local.
```

## Distribution Policy

In Seed, this layer should remain:

```text
neutral;
profile-routed;
optional until proven stable across users;
free of private runtime state;
free of project-specific memory;
compatible with Codex, Claude Code, Cursor and generic AI coders.
```

It may become recommended later only after repeated use proves that it reduces
confusion without adding excessive latency.
