# MMK ↔ Seed Capability Contract

Status: local candidate, unreleased

Contract: `dnd.seed.mmk_compatibility.v1`

## Roles

`d-nd-seed` is a public, versioned inventory and distribution repository for
portable capabilities. A registry entry proves that a capability is described
and addressable; it does not prove installation, host availability,
activation, freshness, authority, or permission to perform an effect.

MMK remains the private living cognitive and coordination kernel. It owns
identity, intent, continuity, ponderation, authority, current registers, and
receipts. RepoKernel remains the neutral MIT diagnostic compiler and staged
Project Kernel generator. Neither consumer becomes a Seed catalog, and Seed
does not become their kernel.

```text
Seed inventory entry
-> explicit selection
-> consumer-owned mapping
-> host/session compatibility evidence
-> separate owner/effect gate
-> consumer-owned receipt
```

## Selection levels

- `system`: the smallest portable orientation set. Inclusion is plan-only; it
  does not prove that a capability itself is effect-free.
- `default`: `system` plus one small reviewed addition; never synonymous with
  all capabilities marked `core_invariant` in the legacy installer.
- `environment-selected`: `system + default` plus explicit allowlisted
  additions. Its operational status remains unknown until MMK validates the
  current host/session evidence and the owner/effect gate.

`capabilities/mmk-compatibility.json` is the classification and bundle source.
The levels are cumulative. The current system bundle contains two entries;
the default layer adds one. All other entries are environment-selected.
Dependencies are never added implicitly: missing dependencies and conflicts
remain visible in the plan under an explicit review gate.

## Deterministic environment selection

The read-only planner consumes:

1. an explicit profile and runtime id;
2. one selection level;
3. the profile allowlist;
4. the version and SHA-256 of `capabilities/registry.json`;
5. the classification for every registry id;
6. optional ephemeral host/session evidence;
7. the fixed Seed-side target effect `inventory_mapping_only`.

It emits the selected ids, registry path/version/hash, per-source SHA-256,
classification, unresolved effect-review state, registry-risk hint, dependency
and conflict status, authority ceiling, composed gates, license status,
compatibility gate, profile/contract hashes, and an overall selection hash.
The plan does not write a target and does not activate a capability.

Environment-selected entries require both an explicit allowlist and bounded
ephemeral evidence. Seed performs only strict structural, profile-binding and
declared-age-window checks; it does not reproduce MMK Host Capability Field or
current-session validation. MMK must validate the session before activation.
Evidence may inform exposure, access, and operational-path planning only. It
cannot grant authority, alter the effect, or survive as durable session truth.

## Capability lifecycle classification

The compatibility manifest classifies every current registry id as:

- `keep`: portable inventory contract can remain as-is;
- `adapt`: preserve the capability, but map its result or host mechanics to
  the consumer contract;
- `supersede`: the current MMK route should use the named canonical mapping;
  retain the Seed source until a separate deprecation review;
- `retire_candidate`: host-specific implementation should not be selected by
  default; no deletion is authorized;
- `unknown`: owner, runtime, public/network effect, or operational path is not
  verified.

This classification is scoped to MMK-native consumption. It is not a global
removal decision for Claude Code or another established Seed consumer.

## Mapping to canonical MMK contracts

Seed does not define a third envelope.

| Seed field or evidence | MMK consumer mapping |
| --- | --- |
| capability `id` and source path | Extension registry source relation plus explicitly selected adapter |
| `keep/adapt/supersede/retire_candidate/unknown` | routing or drift evidence; never activation |
| selected role and returned bounded result | canonical `ExtensionEnvelope` / `FacultyDelta` adapter owned by MMK |
| runtime id and ephemeral capability evidence | Host Capability Field plus Session Capability Attestation |
| registry/source hashes and dates | evidence/provenance fields on the consumer result |
| registry risk | conservative hint only; actual effects remain unknown until capability review |
| authority ceiling | `inventory_only_no_activation` until the consumer and owner gates complete |

The private MMK schemas remain external read-only references. Seed documents
the mapping and does not copy their schema bodies or private registry state.

## Mapping to RepoKernel

RepoKernel may receive only an explicit selection:

```text
selected capability ids
+ registry version/hash
+ per-source provenance/hash
+ portability classification
+ side-effect and license gates
-> SourceManifest / reviewed SeedSpec mapping
-> GenerationPlan
-> external staged Project Kernel preview
```

The generated Project Kernel may contain selected manifest/faculty guidance
with provenance. It must not contain the whole Seed corpus, MMK identity,
private MMK state, credentials, live memory, or authority. RepoKernel remains
stage-only; target integration requires its separate review gate.

## Authority and side effects

Every Seed selection has an authority ceiling of
`inventory_only_no_activation`. Every selected capability has
`side_effect_class: unknown_until_capability_effect_review`, including entries
whose registry risk is `safe`. Registry risk is a routing hint, not an effect
declaration: a skill or document can describe writes even when its installer
risk label is `safe`.

All selections therefore carry explicit selection, capability-effect review,
host/session, owner/effect/authority and any lifecycle/dependency/conflict
gates. Non-`safe` registry labels add these conservative hints:

| Registry risk | Risk hint | Additional gate |
| --- | --- | --- |
| `safe` | no elevated registry risk declared; not effect proof | capability-effect review still required |
| `writes_files` | local write candidate | selected write owner + dry-run/review |
| `uses_network` | network candidate | verified owner/runtime + network gate |
| `uses_secrets` | secret-adjacent candidate | secret authority + bounded handling gate |
| `publishes` | publication candidate | selected public owner + production gate |
| `runtime` | runtime candidate | selected runtime owner + runtime gate |
| `destructive` | destructive candidate | explicit human gate + recovery proof |

Hooks, cron, polling, global skills, writer targets, network access, provider
calls, publication, and runtime actions are never implied by a bundle.

## License and provenance boundary

Repository evidence currently declares `AGPL-3.0` in the marketplace and
ships the GNU Affero General Public License version 3 text in `LICENSE`.
This contract records that exact repository-level declaration and does not
reinterpret it as a new SPDX choice or legal conclusion.

The current capability registry has no per-capability license/SPDX field.
Therefore the effective default is:

```text
repo_license: AGPL-3.0 (repository declaration)
capability_license: unknown
capability_license_status: not_declared_per_capability
compatibility_gate: review_required_before_copy_or_embedding
```

Reference, id mapping, hashing, and metadata planning do not copy Seed code
into MMK or RepoKernel. Copying, embedding, vendoring, relicensing, or creating
a future source-available MMK distribution requires a separate legal/license
compatibility decision. This task neither changes `LICENSE` nor resolves that
strategy.

## OpenCode profile

`profiles/example-opencode.json` is a dedicated, minimal, plan-only inventory
profile. It is not an OpenCode runtime adapter or execution proof:

- explicit system-level allowlist;
- `safe` risk ceiling;
- no declared model;
- no `.claude` writer assumption;
- no hooks, cron, polling, network, global skill installation, or target write;
- missing session evidence yields `plan_only`, not inferred availability;
- environment-selected planning requires bounded ephemeral evidence, while
  current-session validity remains an MMK responsibility;
- every profile carrying an MMK selection level must remain `plan_only`; a
  future writer must consume a separate owner-gated activation artifact;
- every MMK-selection profile must explicitly name MMK as external validation
  owner, grant no authority, persist no evidence, use a bounded evidence age
  window of at most 3600 seconds, and declare only the known implicit fields,
  all false.

Validate with:

```bash
node scripts/validate_mmk_seed_contract.js
node scripts/mmk_seed_plan.js profiles/example-opencode.json
node scripts/test_mmk_seed_contract.js
```
