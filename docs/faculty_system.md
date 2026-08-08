# Public Faculty System

Seed now exposes the reusable D-ND competence field through one installable
skill, a public-neutral registry, and a read-only planner.

The purpose is not to copy an internal agent environment. It is to make the
methods understandable and selectable in another project without transferring
private memory, machine paths, credentials, runtime topology, active state, or
authority.

## The Simple Surface

Use three things:

```text
faculty-router/SKILL.md
  the routing method an AI agent can install and read;

faculty-registry.json
  44 neutral faculty contracts with function, expected result, role, bundle,
  portability, and effect class;

faculty_plan.js
  a read-only way to inspect a bundle or an explicit set of faculties.
```

The router is deliberately one skill. Installing 44 overlapping trigger files
would increase context noise and make accidental multi-activation more likely.
The registry keeps the deeper field inspectable while the router selects the
smallest coherent faculty composition for the task. One primary faculty with
up to three supports is the normal compact profile, not a universal ceiling;
co-primary and wider support relations remain available when they materially
change the resultant.

## What Was Transferred

The maintainer-attested source inventory records 41 workspace faculties, one
observer/kernel faculty, and two adjacent workspace skills, represented by 44
public-neutral contracts. The private source identity map is intentionally not
published, so this count is not an independently reproducible proof of source
coverage.

The transfer preserves:

- the practical function;
- useful domains and faculty roles;
- the difference between method, adapter, and execution;
- portability and side-effect class;
- the need for a target-owned gate and result receipt.

The transfer does not preserve:

- internal skill text verbatim;
- private product or operator state;
- local filesystem or node identities;
- service addresses, tokens, client data, or active work packets;
- an assumption that source adapters share the Seed repository license;
- permission to install, publish, send, deploy, or operate a runtime.

## Bundles

Bundles are discovery views, not activation groups.

| Bundle | Use |
|---|---|
| `foundation` | Orientation, routing, safety, topology, continuity, learning |
| `software` | Diagnosis, architecture, repositories, node transfer, recovery |
| `design` | UX, agentic interaction, design systems, communication surfaces |
| `research` | Evidence intake, scenarios, archives, laboratories, media |
| `product` | Productization, client setup, business, editorial work |
| `interaction` | Delegation, review, browser, conversation, personal workflows |
| `operations` | Mutation, runtime, publication, synchronization, recovery |

One faculty may appear in more than one bundle because bundles describe use,
not ownership.

## Portability And Effects

The registry keeps two independent classifications.

Portability:

- `portable_method` — the neutral method can be applied directly;
- `adapted_contract` — the reusable invariant was rewritten without its
  private or product-specific adapter;
- `related_resource` — the method belongs to a separate public resource, such
  as the design seed, and is referenced rather than relicensed here;
- `gated_contract` — planning is portable but use depends on a verified host,
  data source, destination, credential, or external-action boundary.

Effect class:

- `reasoning_only` — selection grants no write authority;
- `local_write_gated` — a target repository or filesystem gate is required;
- `external_action_gated` — network, publication, send, runtime, or another
  external side effect requires explicit authorization and validation;
- `sensitive_data_gated` — private data access and every downstream action need
  their own scope and authority.

These fields prevent a useful method from being mistaken for an executable
permission.

## Inspect Before Installing

Validate and list the system:

```bash
node scripts/validate_faculty_registry.js
node scripts/faculty_plan.js --list
```

Inspect one bundle:

```bash
node scripts/faculty_plan.js --bundle=software
node scripts/faculty_plan.js --bundle=design --json
```

Inspect an explicit combination:

```bash
node scripts/faculty_plan.js \
  --faculty=failure-diagnosis \
  --faculty=deep-module-design \
  --json
```

The planner does not choose the primary faculty for you and does not write
files. Its output is a discovery field. The agent must still identify the
requested result, target surface, source truth, effect class, gate, and receipt.

## Install Through Seed

`faculty-router` is registered in `capabilities/registry.json` as an opt-in
recent candidate. Inspect the normal Seed plan first:

```bash
./install.sh profiles/example.json --plan
./install.sh profiles/example.json --dry-run
```

Profiles must select `faculty-router` deliberately. It has no runtime
dependencies: its skill instructions and registry are bundled together.
Related Seed documents explain the surrounding distribution model but are not
required by the installed router. Normal installation copies the router
directory with its bundled registry into the target skill surface.

### Update status

The installer and updater use `.seed/seed_skill_state.json` to record the Seed
source hash and installed baseline for each selected core skill. A later
upstream change replaces the whole directory atomically only when the target
still matches that baseline. Local modifications and provenance-unknown
targets are preserved while the complete new tree is staged under
`.seed/incoming/skills/<id>/<source-hash>/` for review. A removed selection is
reported and never deleted implicitly.

Claude Code can load the copied skill natively. Codex and other agents should
use the neutral `.seed` manifest and their documented runtime adapter. A host
must not claim native hooks, automatic skill activation, background work, or
external access until that exact runtime proves it.

## Selection Example

A repository bug with an unclear cause should normally route as:

```text
requested_result: explain and prove the failure mechanism
primary_faculty: failure-diagnosis
support_faculties: operational-noise-control
surface_adapter: target repository instructions and current state
effect_class: reasoning_only until a fix is requested
required_gate: target write gate before implementation
receipt: reproduction, falsified alternatives, verified cause, regression test
```

Adding every software faculty would make the result worse. The router selects
only the transformations necessary for the current job.

## Evolution Rule

A new internal skill does not automatically become public Seed material.
Promotion requires:

```text
observed reusable method
-> source and ownership review
-> private-residue filter
-> neutral faculty contract
-> portability and effect classification
-> registry validation and focused tests
-> receipt
```

Copy source code only when its license, provenance, dependencies, and public
boundary are independently verified. Otherwise transfer the neutral method or
reference the owning public resource.
