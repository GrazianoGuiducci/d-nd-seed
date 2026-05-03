# Lab Pattern — D-ND research lab architecture

This document describes the **standard lab pattern** behind D-ND research instances. Any node that auto-configures from this seed inherits the structure, scripts, conventions, and UI components described here.

The pattern was crystallized in the spring 2026 from three concrete instances:
- **MM_D-ND** — production research lab (physics: prime gaps, dipolar order)
- **D-ND_LAB** — installable sandbox (multi-domain, dashboard FastAPI)
- **lab-d-nd-site** — public read-only frontend (static HTML, Astro-style)

The same shape will replicate to any new domain (finance, biology, network security, drug discovery, optimization, ...) the lab is bootstrapped for.

## The 5-stage SSP pipeline (Scoperte → Soluzioni → Prodotti)

```
Stage 1   on_crystallize          report → scoperta scaffold
Stage 1.5 finding_eligibility_gate findings classified by signal score
Stage 1.7 finding_promoter (opt)  REVIEW_REQUIRED → APPLICATIVE via LLM
Stage 2/3 application_designer    manifest.draft.json (3 candidates: library/kernel/demo)
Stage 3.5 promote_to_publish      sanitize draft → published/
Stage 4   stage4_poc_runner       PoC execution with metrics → verification.json
Stage 5   stage5_package          installable Python package (PEP 517) → seed
```

Each stage has a single responsibility and writes a deterministic artifact. The pipeline is resumable: if a stage fails, you can re-run from there once the issue is fixed.

## Draft / Published separation

**Critical architectural decision** (refactor 2026-05-03): workflow markup must not leak to public surfaces.

| Layer | Purpose | Markup |
|-------|---------|--------|
| `scoperte/<ts>_<slug>_auto/` | Internal workflow drafts | full: `[TARGET — TM1 refinement]` prefix, `[TARGET — to fill]` placeholders, governance copy (`copy_authority`, `audience: vocabolario livello 1-2 (TM7 terminology rule)`), inline scaffold notices |
| `soluzioni/<ts>_<slug>/` | Internal candidate manifests | `[TARGET]` prefix on names, `[TO BE VERIFIED]` flags |
| `published/<ts>_<slug>/` | Public, sanitized | none of the above. Title clean, content clean, governance fields stripped |

`promote_to_publish.py` is the single point of truth for sanitization. Any new markup convention added to drafts (e.g. when introducing a new internal workflow node) **must be added** to the strip patterns of this script.

## Provider chain

LLM calls in the pipeline cascade through providers ranked by cost / availability:

```
codex-cli (locally installed CLI, OAuth-based)
   ↓ if unavailable / quota exhausted
claude-cli (locally installed CLI, OAuth-based)
   ↓ if unavailable
openrouter HTTP (paid API, model from LLM_MODEL env var)
```

Override via `LLM_PROVIDER_CHAIN=codex-cli,claude-cli,openrouter` env var. Skipping the CLIs (`LLM_PROVIDER_CHAIN=openrouter`) forces HTTP-only mode useful for CI environments.

> Provider availability, plans, models, and pricing change. The chain is a dispatcher pattern — verify your CLIs are installed and your OpenRouter model+key are current before relying on them in production cron.

Implemented in:
- `core/llm_adapter.py` (D-ND_LAB sandbox, all cycle movements)
- `tools/lab_agent.sh` (MM_D-ND production cron, agent + falsifier)
- `tools/translate_tensions.py` (MM_D-ND tensions translator)
- `core/triggers/finding_promoter.py` (lab pipeline LLM judgment)

The constraint: scripts that need **tool use** (read/write/exec, e.g. lab agent generating exp_*.py) only run on `codex-cli` and `claude-cli`. Openrouter HTTP works only for prompt-in/text-out calls (no native tool use).

## Dashboard UI patterns

### Modal candidate (4-tab + pipeline visualizer)

Card click → modal with:
- Header: type chip (cyan/purple/emerald per library/kernel/demo) + maturity chip (amber transitional / emerald mature) + cycle_ts
- Pipeline visualizer SSP (4 steps: scoperta → candidato → Stage 4 → Stage 5, current stage glows)
- Tabs: Overview / Manifest / Source / Actions / Verification (last shown only if Stage 4 done)
- Footer: dir name + close button

Action buttons:
- 📦 Download Blueprint (always active, calls `blueprint_generator.py` via API)
- 📋 Copy manifest JSON (clipboard)
- 🔍 View Stage 4 verification (active if `verification.json` exists for this cycle+type)
- 🌱 Open in seed repo (active if kernel package exists in `d-nd-seed/kernels/`)
- 🚀 Promote to Stage 4 PoC (placeholder, requires async LLM trigger)

Two implementations:
- Vanilla JS (`applications.html` static site)
- Alpine.js (`dashboard/index.html` FastAPI)

Both fetch from same API endpoints when possible. Static sites generate blueprint markdown client-side from the manifest data they already have.

### Cytoscape diagrams

Use `cytoscape-fcose` plugin (Faster Compound Spring Embedder) for any cluster-aware graph (Knowledge graph, Tassonomia). It's more stable than the built-in `cose` for small compound graphs (the kind a lab produces). CDN:

```html
<script src="https://cdn.jsdelivr.net/npm/cytoscape@3.30.4/dist/cytoscape.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/layout-base@2.0.1/layout-base.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cose-base@2.2.0/cose-base.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/cytoscape-fcose@2.2.0/cytoscape-fcose.min.js"></script>
```

Register at app init: `cytoscape.use(cytoscapeFcose);`. Layout config that works (calibrated 2026-05-03):

```js
{
  name: 'fcose',
  quality: 'proof',
  randomize: true,
  fit: true,
  padding: 60,
  nodeRepulsion: 9000,
  idealEdgeLength: 110,
  edgeElasticity: 0.45,
  gravity: 0.25,
  gravityCompound: 1.0,        // for taxonomy with parent-child clusters
  gravityRangeCompound: 1.5,
  numIter: 2500,
}
```

### Trajectory equispaced

For sequence-of-cycle visualizations (timeline of reports), avoid linear time-axis SVG: when cycles cluster in dense periods, points pile up. Use **equispaced step bar** (each cycle gets fixed width, ordinal not temporal) + cards detail grid below. Implemented in dashboard tab Tassonomia → Trajectory mode.

### Theme coherence

Site CSS variables (must be present in any new lab dashboard / page):

```css
--void: #08080c
--panel: #14151d
--panel-2: #1b1c25
--ink: #f4f5fa
--text: #d8dbe7
--muted: #a5a9b9
--dim: #777d93
--cyan: #22d3ee     /* primary accent */
--purple: #a78bfa   /* kernel chip + selected node */
--emerald: #34d399  /* demo chip + PASS verdict */
--amber: #fbbf24    /* transitional / PARTIAL */
--sky: #38bdf8
--danger: #fb7185   /* FAIL */
--line: rgba(220,222,232,.14)
--line-strong: rgba(220,222,232,.26)
```

Tooltip: `bg rgb(15,23,42)` border `rgb(51,65,85)` font 12px shadow `0 8px 24px rgba(0,0,0,.5)`. Pattern shared between dashboard `.node-tooltip` and site `[data-tip]::after` — they intentionally match.

## Watchdog + cascade hooks

### Cycle watchdog

`cycle_watchdog.sh` (cron 04:30) detects cycles where the night cron (lab_agent.sh at 03:30) has produced a discovery dir but no `valutatore_log.jsonl` entry — indicating the trajectory_evaluator skipped or failed. Auto-recovers by running `lab_valutatore.py --run <TS>` + `run_ssp_pipeline.sh <TS> --auto-commit`.

Pattern: **Autologica Preventiva** — when a bug is fixed (here: HEALTH.run_timestamp dependency in lab_valutatore.py), close the neighborhood by adding a guard for the same class of failure.

### Cascade trigger hook

`cascade_trigger_hook.sh` is a `post-commit` git hook that scans commit messages for semantic patterns (`feat(axiom):`, `fix(concept):`, `feat(kernel):`, `cristallizz`, `regola permanente`) and writes events to `/opt/.cascade_pending.jsonl`. The next session of the agent can read this file to propose `cascade-orchestrator` skill activation.

Pattern: **LLM-first management** — when a recurring cascade is observed, build the trigger that fires it automatically.

## Memory / cristallization

Each lab keeps:
- `condensato/` — distilled findings that survived falsifier
- `cimitero.md` — falsified claims with reasons
- `scoperte/` and `published/` (above)
- `prodotti/<id>/manifest.json` + `verification.json` — Stage 4 output
- `seed.json` (per-domain) — current direction, tensions, piano

When a finding evolves through subsequent cycles, the old version moves to `cimitero.md` with a `replaced_by:` reference. The condensed document is the single source of truth at any moment.

## Anti-patterns

- Hardcoding `/opt/D-ND_LAB/data/physics/` or similar in scripts → use env vars.
- Putting workflow markup in `published/` files → it must be stripped at promote time.
- Skipping the falsifier counter-pole → discoveries marked `NEW` without independent challenge are likely **beauty bias** and will be archived in cimitero.
- Cycle skip / orphan without watchdog → manual recovery becomes the norm, system degrades.
- LLM call without provider chain → single point of failure when one CLI is unavailable.

## References

- Top-level: `README.md`, `kernels/README.md` (catalog of installable kernels)
- Plugin scripts: `plugins/d-nd-core/scripts/lab/` (3 pipeline scripts)
- Plugin guide: `plugins/d-nd-core/scripts/lab/LAB_PIPELINE_GUIDE.md`
- Live instances:
  - `lab.d-nd.com/dashboard/` (sandbox)
  - `lab.d-nd.com/applications.html` (static)
  - `d-nd.com/ai-lab` (production research)
- Source repo: [D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB)
