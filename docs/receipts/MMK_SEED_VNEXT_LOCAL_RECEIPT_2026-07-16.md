# MMK Seed vNext Local Receipt

date: 2026-07-16

status: independently reviewed source candidate; formal release remains separate

## Surface

```text
branch: codex/seed-mmk-native-vnext-20260716
base: b947ecb32dcddf2cb5f5f8640cd35815e5354ada
owner: isolated d-nd-seed worktree only
mutation: local_doc + local_code + temporary test fixtures
```

The primary checkout remained clean during preparation. Source integration is
authorized only through the reviewed topic-branch/PR path and is recorded by
Git metadata. No tag, release, deploy, target install, global configuration,
runtime, public runtime surface or adjacent repository mutation belongs to this
receipt. Temporary installer fixtures were created only under the operating
system temporary directory and were not retained as project state.

## Result

- Added the smallest Seed continuity layer: root `AGENTS.md` and
  `CURRENT_STATE.md`. The full autoevolutive scaffold was intentionally not
  generated.
- Added one mapping-only MMK ↔ Seed contract. It keeps Seed as versioned
  inventory, MMK as the living consumer kernel, and RepoKernel as a neutral
  stage-only compiler. Consumer schema ids are referenced, not copied.
- Classified all 65 current registry capabilities for MMK consumption:
  `keep=10`, `adapt=21`, `supersede=1`, `retire_candidate=14`, `unknown=19`.
  No capability was deleted or globally deprecated.
- Added cumulative `system`, `default`, and `environment-selected` layers. The
  system bundle contains two entries and default adds one; environment-selected
  adds an explicit allowlist. Dependencies are reported, never silently added.
- Added a dedicated minimal OpenCode inventory profile with
  `write_policy: plan_only`, no model/provider default and no implicit hooks,
  cron, polling, network, global skills, target writes or `.claude` writer. It
  is not an OpenCode runtime adapter or execution proof.
- Added a read-only MMK Seed planner with registry, profile, compatibility
  contract and per-source hashes; classification; dependency/conflict status;
  registry-risk hints; unresolved effect review; composed gates; evidence
  provenance; license status; and a deterministic selection hash. It never
  activates a capability or writes a target.
- Kept MMK session validity external. Seed rejects malformed, stale-by-profile,
  future, duplicate, unbound or authority-bearing evidence, but labels its own
  check as structural/profile-bound and still requires MMK session validation.
  Every MMK-selection profile must provide the restrictive external policy and
  explicit false declarations for the closed set of implicit effects. Empty or
  non-string selection levels, unknown implicit fields and evidence windows
  above 3600 seconds are rejected.
- Closed writer-boundary defects found during independent review:
  `--legacy-all` can no longer bypass `plan_only`; MMK-selection profiles cannot
  use legacy writers; validation and writers resolve relative targets from the
  same working directory; the updater canonicalizes its actual CLI target and
  binds it to the saved profile; canonical containment rejects Seed descendants
  and symlink/junction escapes even in legacy mode; registry sources cannot
  escape the repository.
- Hardened update preservation: untracked or staged hooks are not treated as
  pristine, and provenance-unknown projector/example updates are staged as
  `.new` for manual review. Empty hook selections no longer abort installation.
- Clarified that registry `risk` is a conservative routing hint, not proof of
  actual capability effects. Every selection retains an explicit capability
  effect-review gate.
- Preserved the license boundary: repository declaration `AGPL-3.0` is recorded
  from existing evidence; per-capability license remains `unknown`; copying or
  embedding requires a separate compatibility review.

## Files changed

```text
AGENTS.md
CURRENT_STATE.md
README.md
CHANGELOG.md
capabilities/mmk-compatibility.json
docs/agent_neutral_seed_surface.md
docs/mmk-seed-contract.md
docs/receipts/MMK_SEED_VNEXT_LOCAL_RECEIPT_2026-07-16.md
install.sh
profiles/example-opencode.json
scripts/installer_option_router.js
scripts/mmk_seed_plan.js
scripts/test_installer_safety.js
scripts/test_mmk_seed_contract.js
scripts/validate_capability_registry.js
scripts/validate_mmk_seed_contract.js
scripts/validate_profile.js
skills/catalog.json
update.sh
```

`capabilities/registry.json`, `.claude-plugin/marketplace.json`, and `LICENSE`
were not changed.

## Validation

```text
PASS  node scripts/validate_mmk_seed_contract.js
      65/65 classified; cumulative bundle 2+1

PASS  node scripts/test_mmk_seed_contract.js
      15/15, including cumulative levels, evidence rejection, mandatory MMK
      policy, provenance, dependencies, effect gates and writer rejection

PASS  node scripts/test_installer_safety.js
      23/23, including canonical target/source containment, CLI/profile target
      binding, Git Bash no-hook install and legacy writer bypass regressions

PASS  node scripts/validate_capability_registry.js --strict-coverage
      65 valid; two expected reference-only warnings

PASS  profile matrix
      9/10 current profiles valid, including the OpenCode inventory profile;
      one origin example retains its pre-existing validation failure

PASS  nested Python kernel tests with project src on PYTHONPATH
      4/4

PASS  Git Bash syntax for install.sh and update.sh
PASS  Git Bash install integration with a no-hook allowlist
PASS  Git Bash updater rejection of plan_only plus --legacy-all
PASS  Node syntax checks for all changed/new JavaScript
PASS  JSON parsing for manifest, profile and legacy catalog
PASS  git diff --check
```

The dedicated OpenCode profile and planner were exercised locally through Git
Bash/Node planning and safety paths. This is not a live OpenCode host proof and
does not establish runtime equivalence.

## Baseline debt, not regressions

- One origin example profile still contains a placeholder rejected as a
  shell-control value. The failure existed at the base and was not required by
  this candidate.
- Strict registry coverage still emits two declared reference-only template
  warnings.
- Version lines remain intentionally distinct: README public release v4.1,
  registry `2026-06-28`, marketplace `1.0.0`/`1.1.0`, and legacy skill catalog
  `2026-03-06`. No public release was invented.
- The legacy registry has no `agent_support.opencode` field in its 65 entries.
  The dedicated plan therefore avoids claiming equivalent runtime support.

## Risks and unresolved gates

- Capability classification is a first MMK-consumption review and may be
  refined by verified owners; `retire_candidate` is not deletion authority.
- Registry `risk: safe` does not prove observe-only behavior. Capability effects
  remain unknown until the relevant source and intended use are reviewed.
- A real OpenCode host plus MMK current-session validation is still required
  before claiming environment-selected availability or execution equivalence.
- Capability-specific license/SPDX data is absent. No Seed code should be
  copied into another distribution until a separate compatibility/legal review.
- Tag, public release, registry/marketplace version change and distribution
  remain separate operator gates after source integration.

## First next gate

Integrate this exact reviewed diff through the topic branch and PR without a
tag or release. After merge, the next independent gates are live OpenCode/MMK
session proof and the future public version/release decision.
