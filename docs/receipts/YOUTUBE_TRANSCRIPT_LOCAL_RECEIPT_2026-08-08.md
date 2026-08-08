# YouTube Transcript Capability — Local Receipt

Date: 2026-08-08
State: source validated and committed locally; publication and VPS adoption await explicit effect approval

## Result

Promoted the old project-bound `youtube-transcript` template into an opt-in,
self-contained public-neutral Seed skill. The package includes a Python
extractor, stable JSON schema, pinned dependency, offline tests, environment
doctor, cross-platform instructions and explicit network/failure boundaries.

The skill requires neither Google OAuth nor a YouTube Data API key. It does not
install dependencies, ingest content, write project memory, publish, use
cookies/proxies or bypass access controls automatically.

## Source Commits

```text
THIA:      ef1b857 fix: restore cross-platform YouTube transcripts
d-nd-seed: 8ccfced feat: publish portable YouTube transcript skill
```

The commits are local and ahead of `origin/main`. An authenticated push attempt
was rejected by the publication gate pending explicit operator approval; no
anonymous, interactive or indirect fallback was used.

## THIA Correction

- Windows now selects `python`; Linux/macOS select `python3`.
- `THIA_TRANSCRIPT_PYTHON` can select an isolated host interpreter.
- `yt-dlp` is actually resolved from `PATH` before conventional fallback paths.
- Telegram transcript commands, `ExtractorSkill` and knowledge ingestion use
  the complete fallback chain by default.
- `tools/requirements-transcript.txt` declares the proven dependency version.

## Seed Promotion

- `plugins/d-nd-core/skills/youtube-transcript/` is installable as one package.
- Capability registry: `uses_network`, optional recent candidate.
- MMK disposition: `unknown`, environment-selected, because host reachability
  and every downstream effect remain consumer-owned.
- The obsolete THIA-dependent reference template was removed.

## Validation

```text
THIA Node syntax: pass
THIA platform tests: 5/5 pass
THIA full fallback smoke: pass (python-fallback)
Seed transcript tests: 5/5 pass
Seed skill-creator validation: pass
Capability registry: 69/69 pass, one declared geo-seo warning
Faculty registry/tests: 44/44 and 13/13 pass
Seed candidate tests: 5/5 pass
Skill reconciliation: 11/11 pass
MMK contract/tests: 69/69 and 15/15 pass
Installer safety: 24/24 pass in the real Windows user context
Nested kernel: 4/4 pass
Seed public-video smoke: pass, en generated, 14,147 words, 1,980 segments
git diff --check: pass before commit
```

## VPS Evidence And Boundary

Read-only VPS inspection found Python 3.12.3 and Node 22.22.0, but no
`youtube-transcript-api`, no `yt-dlp`, and no Codex/OpenCode transcript skill.
The `/opt/THIA` checkout is materially dirty on a checkpoint branch, so no pull,
patch, reset or dependency vendoring was performed there.

After explicit approval, the safe adoption is a versioned package at
`/opt/dnd-seed-capabilities/youtube-transcript/1.0.0` with an isolated virtual
environment and reversible Codex/OpenCode skill links, followed by doctor,
offline tests and the selected public-video smoke test.

No update to `seed.d-nd.com`, MAIOS Atlas, public site, RepoKernel, shared TM7
state, THIA live checkout, service configuration or scheduler was performed.
