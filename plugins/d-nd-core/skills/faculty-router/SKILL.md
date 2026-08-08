---
name: faculty-router
description: Select and coordinate the smallest useful palette from the public D-ND faculty registry. Use when a task crosses skills, competences, repositories, products, research, design, business, external systems, authority boundaries, or when the user asks what capabilities should be installed or combined. Route the smallest coherent faculty composition; never activate faculties that do not change the result.
---

# Faculty Router

Use Seed capabilities as operating faculties, not as a checklist to replay to
the user. Read `references/faculty-registry.json` before routing.

## Result First

Start from the useful result the user needs. Then select:

```text
one primary faculty as the normal compact profile, or co-primary faculties
  when the object requires them
+ the smallest result-changing support set (zero to three is the normal profile,
  not a ceiling)
+ one surface adapter when a specific UI, repository, runtime or channel owns truth
+ one learning faculty only when the work creates a reusable correction
```

Do not load or activate the whole registry. A bundle is an orientation aid, not
an execution plan.

## Internal Micro-Check

When the task touches multiple capabilities or any mutation, answer internally:

```text
entity: what exact thing is being handled?
plane: is this method, project, runtime, public surface, state or distribution?
role: which faculty is primary, support, adapter or learning?
relation: which source and consumer are connected?
mutation: what can change?
gate: which authority or safety condition must pass?
receipt: what proves the useful result?
```

Expand this check only when ambiguity changes the action. Do not turn it into a
ceremonial report.

## Routing Contract

Build the smallest useful plan:

```text
requested_result:
runtime_and_surface:
primary_faculty:
support_faculties:
surface_adapter:
learning_faculty:
source_evidence:
effect_class:
required_gate:
non_actions:
validation_or_receipt:
```

`reasoning_only` faculties may analyze or propose without gaining write
authority. `local_write_gated`, `external_action_gated`, and
`sensitive_data_gated` require the target environment's own authorization and
validation. Selection never implies activation.

## Portability Classes

- `portable_method`: the neutral method can be used directly.
- `adapted_contract`: the public invariant is included; product-private state
  and adapters are not.
- `related_resource`: use the named public family or design seed without
  copying its private or differently licensed source into this package.
- `gated_contract`: planning is portable, but execution depends on a verified
  runtime, data source, destination, credential or external-action gate.

## Integration Sequence

1. Identify runtime, project surface, requested result and effect boundary.
2. Use the registry or `scripts/faculty_plan.js` to inspect a bundle or faculty.
3. Select the smallest coherent composition; use the compact one-primary
   profile when it holds, without treating its count as a ceiling.
4. Read the target project's own instructions and current state.
5. Perform only the action authorized by that project and runtime.
6. Validate the result and preserve only a reusable, source-linked delta.

If a requested faculty is absent, do not invent it or silently map it to a
nearby name. Report the gap and use `capability-level-routing` to decide whether
it is residue, a local method, a skill candidate, or a future Seed capability.

## Public Boundary

This skill contains neutral contracts only. It does not transfer private
workspace paths, operator memory, credentials, active runtime state, service
topology, client data, publication permission, or authority from the system
that originated the methods.

## Acceptance

A routing result passes when:

- the primary faculty owns the dominant transformation;
- support faculties add distinct necessary behavior;
- the selected surface remains the truth and write owner;
- effectful actions have an explicit gate;
- no private source or hidden authority is required to understand the plan;
- the receipt proves a useful result rather than the presence of a procedure.
