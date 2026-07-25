# Faculty System Pre-Push Checkpoint — updated 2026-07-25

status: source publication complete through GitHub PR #3

## Result

The Seed candidate now exposes one opt-in `faculty-router` over 43 bounded,
public-neutral faculty contracts and a safe lifecycle for keeping installed
skills and future public candidates current. The earlier writer blocker is
closed: `install.sh` and `update.sh` share a deterministic, provenance-aware
reconciler instead of blindly copying or permanently skipping existing skills.

This checkpoint supersedes the next-action guidance in
`FACULTY_SYSTEM_LOCAL_RECEIPT_2026-07-24.md`. That file remains historical
implementation evidence.

## Accepted Architecture

### Portable faculty layer

- `faculty-router` is candidate, optional, and self-contained.
- Its 43 contracts describe public functions and expected results without
  private identity maps, runtime state, adapters, credentials, or authority.
- Seven bundles support discovery but never activate broad capability groups.
- Coverage is explicitly maintainer-attested, not presented as reproducible
  proof of private-source parity.
- Repository licensing is not promoted into an unproven capability-specific
  license claim.

### Installed-skill reconciliation

```text
selected Seed source + saved plan
-> deterministic source and target tree hashes
-> .seed/seed_skill_state.json baseline
-> new: atomic install
-> unchanged: no write
-> upstream_changed + target matches baseline: atomic whole-tree replacement
-> locally_modified or baseline_unknown: preserve target and stage upstream
   under .seed/incoming/skills/<id>/<source-hash>/
-> selection_removed: report only; explicit removal remains required
```

The state records capability id, relative source and target paths, registry
version, plan hash, source hash, and installed baseline hash. Symlinks and path
escapes fail closed. A state-commit failure rolls the target replacement back.
Dry-run returns the same classification without target writes.

### Seed freshness intake

The freshness mechanism is a capability manifest plus deterministic receipt
reducer, documented in `docs/seed_freshness_protocol.md`.

```text
validated material capability change
-> local queued candidate note
-> public-neutral schema validation
-> privacy, effect, source-owner and license gates
-> reviewed repository diff and CI
-> explicit commit/push/merge gate
```

A memo hook may create or refresh the local queued note after a validated
change. It cannot copy private source, modify the public registry, infer a
license, commit, push, merge, publish, install, or operate a runtime. A periodic
read-only audit may report drift; blind polling and automatic publication are
excluded.

The local `dnd-skill-evolution-guard` now carries this candidate-handoff rule.
That private integration is not part of the public Seed payload.

## Validation Receipt

```text
capability registry strict coverage: 67 valid, 2 declared reference-only warnings
MMK compatibility: 67/67 classified
faculty system: 11/11 pass
skill reconciliation: 11/11 pass, including rollback injection
Seed candidate reducer: 5/5 pass
installer safety and Bash integration: 24/24 pass
MMK contract: 15/15 pass
nested Python kernel: 4/4 pass
```

Final publication preflight completed on 2026-07-25: shell syntax, canonical
skill validation, candidate example reduction, diff/whitespace/privacy review,
and the explicit 33-file staging inventory are clean. GitHub CI must still pass
before merge.

## Publication Boundary

```text
owner_surface: d-nd-seed
remote: GrazianoGuiducci/d-nd-seed
publication_pr: https://github.com/GrazianoGuiducci/d-nd-seed/pull/3
public_main_commit: 8ca8e477c86acc0d6676b86a7b21f06d3da46405
github_ci: Seed contracts passed before merge
push_classification: source_remote_only
known_automatic_public_consumer: none established
seed.d-nd.com owner: separate seed-landing repository
site checkout condition: behind remote with untracked operator work
site action in this release: none
runtime/VPS action: none
```

Publishing this repository updates the public source inventory. It does not
prove that the separate landing page changed and does not authorize repairing
that gap through a direct deploy.

## Preserved Decisions

```text
router_architecture: accepted as an opt-in candidate
default_distribution: optional until broader external proof
update_semantics: baseline-aware, whole-tree, atomic, preserve-on-ambiguity
freshness_semantics: event-driven candidate intake, human-reviewed promotion
automatic_registry_update: forbidden
automatic_publication: forbidden
private_source_transfer: forbidden
authority_transfer: forbidden
license_by_inference: forbidden
```

## Exact Next Action

No further mutation is required for this work unit. On the next validated
material capability change, inspect the local candidate outbox and begin from
a public-neutral candidate. Reconcile `seed.d-nd.com` only through its separate
repository, current-state and publication gate.
