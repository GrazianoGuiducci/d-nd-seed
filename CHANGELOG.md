# Changelog

All notable public changes to `d-nd-seed` are tracked here.

## Unreleased

### Added

- Promoted `youtube-transcript` from a project-bound reference template to an
  opt-in, self-contained public-neutral skill with a stable JSON contract,
  cross-platform instructions, isolated dependency setup, offline tests, and
  explicit network/failure boundaries. It requires no Google OAuth or API key.
- Registered the skill as a network-using recent candidate and added its MMK
  disposition. Selection never implies dependency installation, ingestion,
  project mutation, publication, cookies, proxy use, or access-control bypass.
- Added provenance-aware core-skill reconciliation shared by
  `install.sh --update` and `update.sh`: deterministic tree hashes, atomic whole-directory
  replacement for unchanged baselines, review staging for modified or unknown
  targets, selection-removal reporting, and a neutral installed-skill state.
- Added the Seed freshness candidate contract, deterministic reducer, example,
  tests, documentation and GitHub CI. Automation may detect and stage neutral
  proposals but cannot update registries, merge or publish by itself.
- Added the installable `faculty-router`, a 44-entry public-neutral faculty
  registry, seven discovery bundles, a read-only planner, validator, focused
  tests, integration guide, and local receipt. The package transfers reusable
  methods without copying private adapters, runtime state, paths, credentials,
  client data, or authority.
- Registered `faculty-router` as an opt-in recent candidate with no false
  runtime dependencies. Its capability-level license remains unknown under the
  repository license boundary; source adapters and related resources remain
  separate review surfaces.
- Linked the legacy coder/thinker taxonomy to the new faculty registry without
  giving either taxonomy installer or activation authority.
- Added the opt-in `source-integrity-interference-guard` v0.1.0. It preserves
  exact source, exposes instruction-layer interference and proposes reversible
  cleanup without automatic mutation, policy bypass or provider accusations.
- Registered the skill as a recent candidate, added its MMK disposition and
  public-neutral faculty contract, and added focused boundary tests.

- Added a minimal repository `AGENTS.md` and `CURRENT_STATE.md` continuity gate
  without applying the full autoevolutive scaffold.
- Added `docs/mmk-seed-contract.md` and
  `capabilities/mmk-compatibility.json`: a mapping-only MMK/RepoKernel contract,
  67/67 capability classification, three cumulative selection levels,
  profile/contract/source provenance hashes, composed authority/effect gates
  and an explicit license compatibility boundary.
- Added a dedicated, plan-only `profiles/example-opencode.json`,
  `scripts/mmk_seed_plan.js`, `scripts/validate_mmk_seed_contract.js`, and
  focused nominal and adversarial contract tests. The profile is an inventory
  planning surface, not an OpenCode runtime adapter or execution proof.

- Added `docs/agent_neutral_seed_surface.md` and registered
  `agent-neutral-seed-surface` so non-Claude runtimes can recognize Seed as
  portable capability logic instead of a `.claude` directory.
- `install.sh` now writes a neutral `.seed/` manifest with profile, install
  plan, adapter notes and memory directory while preserving `.claude/`
  compatibility.
- `update.sh` now prefers `.seed/seed_profile.json` when present and saves
  update plans to both `.seed/` and `.claude/`.
- Added `docs/related_seed_resources.md` and install-time references to the
  separate UX/design seed repo and D-ND portfolio.

### Changed

- Advanced the public-neutral Meta Skill awareness layer to `1.3.0` and its
  update-index contract to `1.1.0`. The awareness layer, Seed operating
  principles and faculty router now project whether a movement unnecessarily
  limits the possibilities or evolution of the system it produces, while
  preserving deliberate choices and exact-effect gates.
- Explicit profile allowlists now constrain the existing installer router
  before legacy stratum defaults are considered.
- Profile validation now checks MMK selection level, capability allowlists,
  host/session evidence policy, canonical target containment, write policy and
  implicit-capability declarations. Every MMK-selection profile must keep MMK
  as external validation owner, persist no evidence, grant no authority and
  declare all implicit effects false; it cannot invoke legacy writer paths.
- Registry source paths are confined to the Seed repository. The updater now
  protects untracked/staged hooks, stages provenance-unknown projector changes
  as `.new`, binds its effective CLI target to the saved profile, canonicalizes
  legacy targets, and cannot bypass `plan_only` with `--legacy-all`.
- Registry `risk` is retained as a conservative hint; actual capability
  effects remain unknown until a separate capability-effect review.
- Clarified that Seed is inventory/distribution rather than live memory,
  runtime, activation authority, MMK or RepoKernel.
- Kept the public v4.1, dated registry, and marketplace plugin versions as
  separate existing lines; no release number was invented for this work.
- Marked `skills/catalog.json` as a legacy taxonomy that points to, but does
  not replace, the capability registry or MMK compatibility classification.

- Updated README, GUIDE, `llms.txt`, runtime adapter docs and memory placement
  docs to make `.seed` the neutral installed surface and `.claude` the Claude
  Code adapter.

## v4.1 - 2026-06-12

### Added

- Added `docs/governed_self_improvement.md`, a portable pattern for turning
  verified corrections, failures and compaction lessons into dynamic crystals,
  condensates, bounded plans and testable local rules.
- Registered `governed-self-improvement` in `capabilities/registry.json` as a
  recent candidate capability.
- Added this root changelog as the visible release-history surface for the
  repository.

### Changed

- Clarified the repository positioning in `README.md` and `llms.txt` around
  AI coding agents, runtime memory, guardrails, hooks, continuity, capability
  routing, cognitive kernels and governed self-improvement.
- Updated the public GitHub repository description and topics around concrete
  AI-agent, runtime-memory, guardrail and coding-agent discovery terms.
- Linked the governed self-improvement loop from `README.md`, `GUIDE.md` and
  `llms.txt`.
- Bumped the capability registry version to `2026-06-12`.

### Validation

- `node scripts/validate_capability_registry.js`
- `node scripts/installer_option_router.js profiles/example-codex.json`
- `node scripts/installer_option_router.js profiles/example-app-runtime.json`
- `git diff --check`

## v4.0 - 2026-04-23

### Added

- Mature skills and autonomous cycle release.

## v3.2 - 2026-05-29

### Added

- Added the awareness orchestration layer: shared state schema, boot class,
  action gate, capability selection, verification, memory and cascade.
- Registered awareness orchestration docs, boot router, programmable awareness
  and seed operating principles as core invariants.

## v3.1 - 2026-04-09

### Added

- Added diagram generator, observer positioning and bilingual visual
  specification work.

## v3.0 - 2026-04-08

### Changed

- Made the seed provider-neutral and public-ready.
- Removed internal infrastructure references from the portable surfaces.
