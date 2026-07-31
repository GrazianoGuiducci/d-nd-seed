# Seed Freshness Protocol

Seed should notice useful THIA/D-ND capability changes without copying private
workspaces or silently publishing them. The safe unit of transfer is a neutral
candidate manifest, not a changed `SKILL.md` directory.

## Classification

This protocol is a capability manifest plus a deterministic receipt reducer.
A memo or hook may remind an agent to create the manifest after a validated
skill change, but it does not own the registry and cannot commit, push, merge,
install, publish, or grant a license.

```text
validated source capability change
-> local dissemination recommendation
-> public-neutral candidate manifest
-> deterministic validation and reduction
-> draft repository change with CI
-> source-owner, privacy, license and effect review
-> registry/faculty/docs update
-> tests, receipt, commit and push gates
```

## Candidate Contract

Use `capabilities/seed-update-candidate.schema.json` and start from
`docs/examples/seed-update-candidate.example.json`.

Validate a candidate:

```bash
node scripts/seed_candidate.js --file=path/to/candidate.json
node scripts/test_seed_candidate.js
```

The reducer returns one of:

- `invalid`: malformed, secret-bearing, private-path-bearing, or authority
  transferring;
- `blocked`: structurally valid but still awaiting privacy, effect, or license
  evidence;
- `ready_for_registry_review`: safe enough for a human-reviewed repository
  proposal, never for automatic merge or publication.

## Automation Boundary

Safe automation may:

- detect that a validated local capability changed;
- create or refresh a local candidate note;
- run the deterministic validator;
- open or update a draft PR containing only reviewed neutral artifacts;
- run repository CI and report stale or blocked state.

Safe automation must not:

- copy internal skill text, state, paths, credentials, topology, client data,
  or identity maps into Seed;
- infer a capability license from the repository license;
- mark a capability available without a reviewed registry diff;
- merge, release, update the landing, install into a target, or operate a
  runtime without its separate gate.

## Freshness Signal

Use an event-driven signal after a material skill or competence change has
passed its local validation. Do not poll every file modification and do not use
blind cron as proof of freshness. A periodic read-only audit may compare the
last accepted source receipt with the candidate queue as a safety net, but it
should report drift rather than manufacture updates.

The public freshness state is therefore observable:

```text
no candidate: no reviewed portable delta is waiting
queued: neutral proposal exists but is not public availability
blocked: evidence or boundary is incomplete
ready_for_registry_review: proposal may enter a reviewed diff
integrated: registry/docs/tests and receipt identify the accepted delta
```

Only `integrated` capability entries are publicly available Seed inventory.

## Meta-Skill Channel Index

The neutral Meta Skill layer publishes a small, machine-readable freshness
index at `capabilities/meta-skill-update-index.v1.json`. A node may compare its
installed public contract versions with that index when a relevant event occurs
or its 24-hour read-only freshness window expires.

The index covers only Seed-owned public-neutral capabilities. It does not
advertise, locate or authorize a private organization overlay. Fetch, install,
target writes, canonical-source updates, publication and push remain separate
actions.

Node-side emergence uses the complementary invariant:

```text
mandatory local capture;
optional owner-reviewed private integration;
optional neutral Seed promotion.
```

Do not make every observation a registry diff. Seed sees only a validated,
neutralized candidate produced through the existing candidate contract.
