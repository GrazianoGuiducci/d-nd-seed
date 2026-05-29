# Lab Pattern — D-ND research lab architecture

This document describes the **standard lab pattern** behind D-ND research instances. Any node that auto-configures from this seed inherits the structure, scripts, conventions, and UI components described here.

The pattern was crystallized from the interaction of three neutral surfaces:
- a production research lab;
- an installable multi-domain sandbox;
- a public read-only frontend.

The same shape can replicate to any new domain the lab is bootstrapped for.

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

## Cycle architecture (21 movements)

A single lab cycle is a deterministic sequence of 21 movements. Each writes its artifact and the next reads what it needs from disk. No movement holds the next hostage — failure of a non-critical step degrades gracefully and the cycle still produces what it can.

```
0  autopsy              read previous run, find regressive node
1  trajectory_apply     apply previous cycle's REDESIGN to seed (loop A8+A15)
2  build_field          assemble live field from seed + reports + tensions
3  agent                LLM agent runs autonomous experiment, writes report
4  bias_corrector       A8 autologic: rewrite biased claims pre-falsifier
5  report_falsifier     5-lens counter-pole, checks report internal coherence
6  bicono_extractor     parse "Bicono della scoperta" into structured JSON
7  validate_seed        integrity + bootstrap from seed_tensions
8  verify_assertions    domain claims: PASS / FAIL / SKIP
9  structural_check     scan code, inject META tensions on anti-patterns
10 build_lab_data       snapshot piano + tensions + last report
11 build_graph          knowledge graph nodes + edges
12 sync                 propagate state to declared targets
13 verify_endpoints     downstream consumer health checks
14 refiner              second LLM observes the STEP, not the result
15 semantic_bridge      map findings to domain categories
16 refresh_detector     event-driven regeneration trigger
17 seed_integrator      crystallize new seed (also from verify_assertions)
18 veritas_score        ρ ∈ [0,1] aggregating 3 independent vectors → SCARTO/SOSPENSIONE/COLLASSO
19 trajectory_evaluator decide REDESIGN / NEXT_CYCLE / CRYSTALLIZE / STOP
20 promotion_proposer   extract finding → skill/hook/system rule (no auto-apply)
21 ssp_pipeline         scoperta → soluzione → prodotto packageable
22 narrative_writer     200-word human-readable narrative of the cycle
23 notify               webhook to operator (Telegram / Sinapsi / etc.)
```

> Numbers above 19 reflect the post 2026-05-05 expansion. Pre-expansion the cycle was 19 movements (no Aeternitas/Veritas gate, no trajectory_apply, no narrative_writer). The four additions close the autopoietic loop: gate quality, gate lineage, apply the next-cycle decision automatically, expose every iteration as readable narrative.

### Aeternitas + Veritas — structural gate

Two checkpoints between report and promotion. They run in parallel inside `seed_integrator` (Aeternitas) and as standalone movement (`veritas_score`).

| Gate | Code | What it verifies |
|------|------|------------------|
| **Aeternitas P0** | Lignaggio | Every tension carries `condensato_ref` traceable to an axiom (A1–A16) or fact (F1–F6). No claim without lineage. |
| **Aeternitas P1** | Integrità | Piano advances strictly (N → N+1, never backwards or static when there are new tensions). No duplicate tension IDs. |
| **Aeternitas P5** | Autopoiesi | Cycle produced new tensions OR changed direction. A cycle that only repeats is not generative. |
| **Veritas ρ** | quality score | Aggregates V_a (telemetric: assertions ratio + falsifier penalty + bicono completeness + report size) + V_b (logico-historic: aeternitas P0/P1/P5 + direction evolution) + V_c (environmental confirmation: report structured sections + tools invoked + bicono in report). |

Decision bands:
- **ρ < 0.4**: SCARTO (cycle quality below floor; finding cannot be promoted)
- **0.4 ≤ ρ < 0.9**: SOSPENSIONE (cycle valid but not promotable yet — wait for further evidence)
- **ρ ≥ 0.9**: COLLASSO (high-quality cycle, finding eligible for promotion)

Default mode is `warn`: gate decision is logged in `data/<lab>/aeternitas/aeternitas_<ts>.json` and `data/<lab>/veritas/veritas_<ts>.json`, but the seed write proceeds even on VETO. Set `movements.seed_integrator.params.aeternitas_mode='hard'` for strict blocking.

### Trajectory loop A8 + A15

`trajectory_evaluator` (movement 19) decides the next cycle's posture: `NEXT_CYCLE / REDESIGN / CRYSTALLIZE / STOP`, with `confidence` and an `action` blob describing what should change in the seed.

`trajectory_apply` (movement 1, runs at start of every cycle) reads the previous cycle's trajectory log and **automatically applies** the decision to the seed when:
- `confidence == 'high'`
- `action.type == 'modify_seme'`

This closes the autopoietic loop concretely (axioms A8 — autologic, A15 — vehicle without driver). The system corrects itself between cycles without operator intervention. Lower-confidence or `trigger_cycle`-only decisions are skipped (logged), preserving operator authority over architectural REDESIGN.

### Narrative writer

`narrative_writer` (movement 22) takes the cycle's technical artifacts (agent report, falsifier flags, veritas vectors, aeternitas decision, trajectory verdict, bicono) and asks an LLM (via the standard provider chain) to produce a ~200-word narrative for non-technical readers. No jargon, three-act structure: what was tested → what the system found → what changes now.

Output: `data/<lab>/narratives/narrative_<ts>.md` with frontmatter (cycle_ts, lab, word_count, verdict_band, aeternitas, trajectory_decision) + body. The frontmatter is consumed by public-facing routes that render it as styled HTML (e.g. `lab.d-nd.com/n/<lab>/<ts>`).

This makes every cycle shareable — a LinkedIn-ready URL per iteration, structured for consumption beyond the technical operator.

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

Implemented by the lab runtime through:
- a provider adapter for cycle movements;
- an agent runner for experiment generation and falsification;
- a tension translator when a domain needs one;
- a finding promoter for lab pipeline LLM judgment.

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

## Observable hygiene (registry pattern)

**Soglia di adozione**: quando un dominio del lab cresce oltre **2 script `exp_*.py` che condividono nomi di osservabili** (es. `SR`, `triple_var`, `effect_z`), instaurare un registry centrale `observables_registry.py` come Source of Truth. Sotto questa soglia il pattern è opzionale.

### Il problema che il registry risolve

Pattern real observed in a lab cycle and generalized as an installable rule:

- `SR` definito come `spacing_ratio` in 6 script, ma come `spectral_rigidity` in 1 script
- `triple_var` raw in 3 script, ma normalizzato (`/ var(gaps)`) in 1 script
- Cross-cycle reports usavano `SR` come label assumendo coerenza → **stavano confrontando funzioni matematiche diverse pensando fossero la stessa**

L'agent autonomo del lab ha catturato il bug da solo nel report 06:25 (sezione META Findings + Consecutio) — ma per evitare che si ripeta in altri lab, il pattern va istituzionalizzato.

### Struttura del registry

`tools/observables_registry.py` (o equivalente per dominio):

```python
"""Source of Truth per gli observables del lab <dominio>."""

OBSERVABLES_REGISTRY_VERSION = "1.0.0-YYYY-MM-DD"

# Canonical: la convention dominante (più script la usano), immutabile dentro la versione
def SR(gaps): ...
def triple_var(gaps): ...
OBSERVABLES_CANONICAL = {"SR": SR, "triple_var": triple_var, ...}

# Variants: nomi distinti per formulazioni alternative — niente shadowing del canonical
def SR_local_rigidity(gaps): ...
def triple_var_normalized(gaps): ...
OBSERVABLES_VARIANTS = {"SR_local_rigidity": SR_local_rigidity, ...}

def compute_canonical(gaps): return {n: f(gaps) for n, f in OBSERVABLES_CANONICAL.items()}

def report_header():
    return f"observables_registry: {OBSERVABLES_REGISTRY_VERSION}\nobservables_used: [...]"
```

### Convention per i report

Ogni cycle report che usa observables nominati DEVE dichiarare:

```
observables_registry: 1.0.0-2026-05-06
observables_used: [SR, SR2, L1, L2, triple_var]
```

Se un cycle usa una variante esplicita, va dichiarata accanto al canonical:

```
observables_used: [SR, SR_local_rigidity, triple_var]
```

### Convention per gli exp scripts

```python
# Canonical use
from observables_registry import OBSERVABLES_CANONICAL, compute_canonical
results = compute_canonical(gaps)

# Variant use (esplicito, no shadowing)
from observables_registry import SR, SR_local_rigidity  # nomi distinti
```

**Anti-pattern**: ridefinire localmente un nome canonico (`def SR(gaps): ...` dentro `exp_foo.py` con formulazione diversa). Il registry diventa carta straccia se gli script lo bypassano.

### Versioning

Cambiare una definizione canonica = bump del registry version + nota nel changelog del registry. Le definizioni canoniche sono **immutabili dentro una versione**: cycle storici devono restare riproducibili.

### Quando NON serve

- Lab con 0 o 1 exp script (nessuna possibilità di collision)
- Lab dove gli observables sono unici per nome e mai condivisi tra script
- Lab in fase esplorativa pura, dove il vincolo bloccherebbe l'esplorazione (ma considerare adozione appena la fase si chiude)

## Anti-patterns

- Hardcoding absolute lab data paths in scripts → use env vars.
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
