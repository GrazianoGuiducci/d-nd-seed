# d-nd-seed Entry Gate

This repository is the public AGPL-3.0 capability inventory and distribution
surface for portable D-ND functions. It is not live memory, an authority
source, a runtime, MMK, or RepoKernel.

Before changing capability contracts, profiles, routing, installers, or
runtime adapters:

1. Read `CURRENT_STATE.md`, `capabilities/registry.json`, and the closest
   contract under `docs/`.
2. Identify the acting host, selected environment, target project, write
   owner, effect evidence, and validation path independently.
3. Treat capability presence as inventory only. Selection, host/session
   compatibility, activation, and material authority require separate gates.
4. Prefer mapping to the canonical consumer contract. Do not create a Seed
   copy of MMK `ExtensionEnvelope`, Host Capability Field, Session Capability
   Attestation, or RepoKernel schemas.
5. Keep `system`, `default`, and `environment-selected` capability layers
   cumulative and distinct. Environment additions require an explicit
   allowlist and plan or dry-run; dependencies are reported, never silently
   added. No hooks, network, polling, cron, global skills, or writer targets
   become implicit.
6. Preserve provenance: registry version/hash, capability id/path, source hash
   when a plan is produced, authority ceiling, registry-risk hint, unresolved
   effect-review state, and composed gates. Registry `risk` is not proof of a
   capability's actual effects.
7. Preserve the license boundary. Repository-level license evidence does not
   prove a capability-specific license. Unknown values remain `unknown`, and
   copying or embedding into another distribution requires its own
   compatibility review.

## MMK and RepoKernel boundary

- MMK may consume an explicitly selected Seed inventory entry through its own
  canonical ExtensionEnvelope and host/session evidence. Seed never activates
  an MMK faculty or supplies MMK identity, memory, authority, or current state.
- RepoKernel may stage only selected capability manifests and portable
  faculties with provenance into a Project Kernel. It must not vendor the full
  Seed corpus or import MMK authority.
- Research, Lab, Godel, Sinapsi, network, publishing, provider, and runtime
  capability status stays `unknown` until the relevant owner and operational
  path are verified.

## Mutation and receipt

Allowed by a bounded local repository gate: documentation, registries,
profiles, read-only planners, validators, tests, and a local receipt.

Require a separate explicit gate: install/update writers, target-project
writes, hook activation, network/provider calls, secrets, publication,
deployment, runtime changes, global configuration, cross-repository changes,
commit, push, release, or license changes.

Every material contract change must leave a local receipt naming changed
files, tests, baseline debt, unresolved drift, boundaries, risks, and the next
review gate.
