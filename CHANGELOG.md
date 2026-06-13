# Changelog

All notable public changes to `d-nd-seed` are tracked here.

## Unreleased

### Added

- Added `docs/agent_neutral_seed_surface.md` and registered
  `agent-neutral-seed-surface` so non-Claude runtimes can recognize Seed as
  portable capability logic instead of a `.claude` directory.
- `install.sh` now writes a neutral `.seed/` manifest with profile, install
  plan, adapter notes and memory directory while preserving `.claude/`
  compatibility.
- `update.sh` now prefers `.seed/seed_profile.json` when present and saves
  update plans to both `.seed/` and `.claude/`.

### Changed

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
