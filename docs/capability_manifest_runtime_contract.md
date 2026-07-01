# Capability Manifest Runtime Contract

> Status: recent candidate / optional Seed capability.
> Scope: neutral contract for skill-like behavior entering autonomous or
> semi-autonomous runtimes.

## Purpose

Some capabilities begin as instructions for a human-facing AI coder. A runtime,
agent loop, Lab cycle, product workbench or external system should not call
those instructions as hidden authority.

Before skill-like behavior enters an autonomous or semi-autonomous surface,
convert it into a capability manifest with explicit receipts and a bounded next
action.

## Core Rule

```text
skill-like behavior
-> capability manifest
-> bounded action
-> validation
-> receipt
-> reducer or validator
-> next legal action
```

The manifest is not a hook, scheduler, provider call, hidden agent, deploy
step or permission grant. It is a reviewable contract that tells the system what
may happen and what must stop.

## Manifest Shape

```text
capability_id:
purpose:
trigger_state:
required_inputs:
allowed_actions:
blocked_actions:
side_effect_class:
validation:
receipt_schema:
memory_policy:
human_gate_required_when:
stop_condition:
```

## Receipt Shape

```text
receipt_id:
capability_id:
created_at:
input_state:
selected_action:
why_selected:
blocked_stronger_action:
validation:
authority_flags:
side_effects:
next_legal_action:
stop_condition:
```

## Reducer Rule

If a receipt class becomes stable, prefer a small deterministic reducer or
validator over asking a model to reinterpret the whole situation.

The reducer may map a receipt to:

```text
finite_state:
next_legal_action:
blocked_stronger_action:
validation_errors:
```

The reducer must not:

```text
call providers;
read secrets;
download raw source material;
mutate runtime authority;
write target project state;
publish or deploy;
promote results;
clean up or delete files;
hide human approval requirements.
```

## Human Gate

Use a human gate when the next action crosses one of these boundaries:

```text
provider or paid API;
runtime mutation;
target project write;
source intake, raw download or extraction;
measurement, promotion or authority move;
public sync, publish or deploy;
secret, credential or private data;
cleanup, deletion or irreversible operation.
```

## Relation To Seed, RepoKernel And Meta Skill

Seed carries the neutral contract.

RepoKernel may project the contract into a generated Project Kernel when a
project needs autonomous or semi-autonomous capability use.

Meta Skill decides whether the observed behavior is a local lesson, a
capability manifest candidate, a receipt reducer, a metaskill or a product
capability.

## Adoption Policy

Keep this capability optional until a target project actually needs
autonomous/semi-autonomous use. For a normal human-driven coder workflow, a
procedure or checklist may be enough.

Do not bulk-convert all skills into manifests. Convert only behavior that will
be consumed by a runtime, product surface or agent loop and has clear inputs,
boundaries, validation and receipts.
