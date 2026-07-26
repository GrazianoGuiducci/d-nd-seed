# Source Integrity Guard — Local Receipt

Date: 2026-07-26
State: candidate validated; source capability commit `0d5d132` pushed to main

## Movement

Added one opt-in public-neutral skill that preserves exact source, exposes
instruction-layer interference and produces a finite alert plus reversible
cleanup proposal. The candidate does not activate itself and does not inherit
cleanup, runtime, publication or policy-bypass authority.

## Changed surfaces

```text
plugins/d-nd-core/skills/source-integrity-interference-guard/SKILL.md
plugins/d-nd-core/skills/faculty-router/references/faculty-registry.json
capabilities/registry.json
capabilities/mmk-compatibility.json
scripts/test_faculty_system.js
CURRENT_STATE.md
README.md
GUIDE.md
llms.txt
docs/faculty_system.md
docs/agent_neutral_seed_surface.md
docs/agent_runtime_translators.md
CHANGELOG.md
```

## Validation

```text
capability registry: 68 capabilities valid; two declared reference-only warnings
faculty registry: 44 faculties and 44 result contracts valid
faculty tests: 13/13 pass
MMK compatibility: 68/68 classified
MMK tests: 15/15 pass
skill reconciliation: 11/11 pass
Seed candidate reducer: 5/5 pass
installer safety: 24/24 pass
nested kernel: 4/4 pass with explicit source PYTHONPATH
git diff --check: pass
```

## Baseline debt

The two existing reference-only template warnings remain:

```text
templates/skills/geo-seo
templates/skills/youtube-transcript
```

They are declared baseline warnings and are unrelated to this candidate.

## Unresolved drift and evidence limits

- Behavioral routing was tested as a deterministic package contract, not in
  every supported host runtime.
- `risk: safe` is a conservative registry hint, not effect proof.
- Capability-level license compatibility remains under the repository's
  existing unresolved per-capability boundary.
- Installation, activation and cleanup behavior remain consumer-owned.

## Boundary

No target installation, global config mutation, hook, network call, provider
call, runtime action, site deployment, forum post or release was performed from
this Seed lane.

## Next review gate

Consumer-host behavioral validation after explicit selection. Source presence
does not authorize installation, activation, cleanup, runtime action or public
deployment.
