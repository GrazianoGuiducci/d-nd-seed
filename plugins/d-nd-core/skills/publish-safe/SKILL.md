---
name: publish-safe
description: "Five mechanical gates for any content publish pipeline with CMS + rendering layers. Prevents false security: 'API returned 200' does not mean 'visitor sees clean content'. Use when writing content to a multi-layer serving system (CMS API, static files, prerendered HTML, cached copies)."
---

# Publish Safe — Five-gate pattern

> A publish operation is not atomic. Content traverses layers, and each layer
> can silently fail to update. This skill enforces mechanical checks so the
> operator does not rely on a single measurement to declare success.

## The anti-pattern this prevents

"HTTP 200 = clean" — but HTTP 200 only confirms the API accepted the write.
It says nothing about:
- whether input had encoding artifacts that got propagated
- whether internal links in the content point to valid destinations
- whether the file actually reached the serving layer
- whether cached/prerendered copies got invalidated
- whether the visitor sees new content or stale HTML

Each of these is a separate layer. Each layer can fail independently.
A gate-less publish has a combinatorial false-positive space.

## The five gates (mechanical, sequential, fail-fast)

### Gate 1 — SANITIZE (pre-write input normalization)

Normalize known encoding artifacts before the write. Common sources:
- UTF-8 double-encoded through latin-1 (curly quotes appear as `â€œ`, arrows as `â†'`)
- Copy-paste from rich text producing mixed codepoints
- Platform-specific substitutions (cp1252 em-dash, smart apostrophes)

Maintain a `MOJIBAKE_MAP` table ordered **long-first** (longer patterns before
their prefixes — otherwise short-match eats part of long sequences).

**Scope — which fields to scan:** scan every field that ends up rendered
to a consumer, not just the primary content body. Pages typically carry:
- `content` / `content_en` (body — the obvious target)
- `description` / `description_en` (injected into `<meta name="description">`,
  `og:description`, `twitter:description` — crawlers and AI ingest these)
- `title` / `title_en`, `summary`, alt-text fields on embedded media
- `visual_spec`, `diagram_spec`, or any structured JSON field that
  produces rendered text (diagram titles, labels, tooltips, detail
  sentences) — these ship as HTML inside the page and are visible to
  both humans and LLMs
- Any field interpolated into SEO templates or OpenGraph tags

Gate-1 misses here are invisible: the body looks clean, the meta layer
ships with mojibake or bias, and crawler/AI indexing picks up the bad
version because the API echo only reported the body's cleanliness. If
the stack has a meta layer or an embedded structured-content layer
(like `visual_spec`), sanitize must include it by scope declaration —
not as a later patch.

**Server-generated fields caveat.** Some fields are regenerated
server-side after the write (e.g., a CMS extractor re-derives the field
from the body and overwrites what the client sent). If the gate scans
these at write time but the server regenerates them downstream with a
different process, the gate output is stale — the server version
shipped, not the sanitized one. Two rules:

1. **Sanitize at the source of regeneration, not at the API boundary.**
   If `visual_spec` is re-extracted from the body by a server process,
   the server's extraction logic must contain the same sanitization
   rules as Gate 1. Gate 1 alone at the API client is not enough.
2. **Gate 4 VERIFY must scan the final layer, post-regeneration.** Do
   not trust that what the client sent is what the consumer reads.
   Re-fetch after the server has regenerated and verify.

If input still contains known-bad sequences after sanitize, raise — do not
pass poisoned content through the gate.

### Gate 2 — INTEGRITY (pre-write relational check)

Scan content for internal references (links, includes, cross-refs). For each:
- extract the target identifier (slug, id, path)
- verify it exists in the current registry (live list of valid targets)
- whitelist static/hardcoded routes that are not in the registry
- ignore external/mailto/anchors

**Scope — same discipline as Gate 1:** apply link-integrity scans across
every field that can hold a reference, including `description` /
`description_en` and any metadata field that may contain a URL or slug.
Links inside meta-description shipped broken are the same class of silent
failure as body links — crawler previews and AI summaries surface them.

If a link points to a target that does not exist and is not whitelisted: raise
(or at minimum: warn and require explicit override). Broken internal links
silently shipped are a recurring failure class.

### Gate 3 — SAFE WRITE (explicit encoding at the boundary)

Write with explicit encoding and correct content-type:
- `POST` with `Content-Type: application/json; charset=utf-8`
- Use `--data-binary @file` (not `-d "..."`) to preserve bytes exactly
- File written as UTF-8 without BOM
- Verify bytes-in-flight match bytes-intended (len check)

The failure mode here: content-type not set, server infers latin-1, re-encodes.
This is how mojibake gets introduced in the first place — Gate 1 cleans what
previous Gate 3 failures created.

### Gate 4 — VERIFY (post-write scan of all serving layers)

For every layer that can serve the content to a consumer:
- **Layer 1**: API echo (read back what was written)
- **Layer 2**: static file served by edge/cache (may be different path)
- **Layer 3**: rendered HTML (prerender, SSR, cached fragment)
- **Layer N**: any other serving path specific to your stack

For each layer: scan for the same MOJIBAKE_MAP patterns (byte-level where
possible — unicode normalization in a JSON parser can hide byte-level
double-encoded sequences) + integrity check.

Critical: **Layer 1 clean does not imply Layer 3 clean.** If they differ,
investigate before declaring success.

Also critical: a verify gate is itself a measurement with a scope. Make the
scope explicit ("scanned for these 17 patterns") — a passing verify does not
mean "everything is clean at every layer", it means "the scanned patterns
were absent". This is autologica applied to verification itself.

### Gate 5 — REBUILD TRIGGER (propagation completion)

If Gate 4 reveals a serving layer that did not pick up the write (e.g., prerender
HTML is stale despite API clean), trigger the rebuild/invalidation hook for
that layer. Do not declare the publish complete until all layers converge.

Common patterns:
- Static site generators: invoke `npm run build` + deploy dist
- Edge caches: issue purge request
- CDN: flush endpoint

If no rebuild hook exists, the gate must emit a concrete warning: "content
written at Layer 1+2, Layer N stale — requires manual rebuild". Do not
paper over the gap.

## Autologica applied to the skill itself

This skill is content. Does it pass its own gates?

1. SANITIZE: this file contains no mojibake (verified).
2. INTEGRITY: references to other skills (cec, autologica, etc.) must point to
   skills that exist in the same seed.
3. SAFE WRITE: when this skill is installed by the seed installer, it is
   written as UTF-8 explicitly.
4. VERIFY: after install, verify the file content on disk matches the source.
5. REBUILD TRIGGER: installing a new skill may require restarting the agent
   system to pick up the new capability.

The skill is the pattern applied to itself — the gate is the measurement.

## Relation to axioms

- **C2 (coincidence is not proof)**: a single measurement passing is not
  evidence the whole system is clean. The 5-gate structure encodes C2
  mechanically instead of relying on operator discipline.
- **A2 (determinant is the necessity of the boundary)**: each gate defines
  a boundary — what does it measure, what does it not measure. Scope-explicit
  verification prevents false security.
- **A8 (autologica)**: the skill is subject to itself (gate 4 applied to
  gate 4 — verify the verify).
- **Riparazione regressiva**: a Layer 3 stale failure has its root at Gate 5
  (rebuild not triggered), not at Gate 4 (verify caught the stale — that is
  gate 4 working correctly). Fix upstream.

## Anti-patterns

- **Ceremonial verify**: running the scan but declaring pass without reading
  the output. Make the assertions fail-fast so silence equals success.
- **Single-layer claim**: "API returned 200" is not "content is live clean".
  Always name which layer was verified and which were not.
- **Gate skipping for speed**: "this is a small edit, skip Gate 2". The edit
  that breaks Gate 2 is typically the one you skipped it on.
- **Sanitize during write instead of before**: if the write layer cleans
  content, the upstream source of mojibake is never found and fixed.

## Eval

## Trigger Tests
# "publish this content to the site" -> activates
# "POST to the CMS" -> activates
# "write new page X with content Y" -> activates
# "what color should the button be" -> does NOT activate

## Fidelity Tests
# Given input with mojibake: Gate 1 sanitizes before POST
# Given broken internal link: Gate 2 raises (or warns with explicit override)
# Given stale prerender after API success: Gate 5 triggers rebuild
# Given all layers clean: publish declared complete with explicit layer list
# Given verify scope incomplete (e.g., only patterns X,Y scanned but not Z):
#   skill output must name the scope — "scanned for X,Y" not "clean"
