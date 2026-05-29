# Lab Pipeline — Scripts Guide

Three scripts that implement the SSP (Scoperte → Soluzioni → Prodotti) pipeline pattern. They convert raw LLM-driven research output into clean, publishable artifacts and installable blueprints.

These scripts are **domain-agnostic** by design — they read environment variables for paths and work with any `<lab_data>/<domain>/` structure that follows the conventions below.

## Conventions

```
<LAB_DATA_DIR>/<DOMAIN>/
├── scoperte/                     INTERNAL — workflow drafts, full markup
│   └── <ts>_<slug>_auto/
│       ├── lab-note.draft.md
│       └── cycle-report.draft.md
├── soluzioni/                    INTERNAL — application_designer output
│   └── <ts>_<slug>/
│       ├── manifest.draft.json
│       ├── summary.draft.md
│       └── finding_index.draft.json
└── published/                    PUBLIC — sanitized, source for site/dashboard
    └── <ts>_<slug>/              (no _auto suffix)
        ├── lab-note.md
        ├── cycle-report.md
        ├── manifest.json
        ├── summary.md
        └── finding_index.json
```

### Environment variables

| Var | Purpose | Default |
|-----|---------|---------|
| `LAB_DATA_DIR` | Root per-domain data | set per installation |
| `LAB_APPLICATIONS_DIR` | Single-domain applications root fallback | `./applications` |
| `DOMAIN` | Active domain | `default` |
| `LLM_PROVIDER_CHAIN` | Provider order | `codex-cli,claude-cli,openrouter` |
| `OPENROUTER_API_KEY` / `LLM_API_KEY` | Fallback HTTP | from `.env` |
| `OPENROUTER_MODEL` / `LLM_MODEL` | Fallback model | configured per-installation in `.env` |

> Models, provider plans, and pricing change frequently. Verify your CLI installations (`which codex`, `which claude`) and your OpenRouter model/key before deploying to production.

Both single-domain and multi-domain setups are supported via the dual-mode `_resolve_paths()` in each script.

## Scripts

### 1. `promote_to_publish.py`

Sanitize `scoperte/<dir>_auto/` + matching `soluzioni/<dir>/` → `published/<dir>/`.

Strips workflow markup that should not appear publicly:
- `[TARGET — TM1 refinement]` prefix from titles
- `## [TARGET — *]` placeholder sections
- YAML keys: `copy_authority`, `audience: ... (TM7 terminology rule)`, `target_route`, `generated_by`
- Inline `[SCAFFOLD AUTO-GENERATO]` notices
- Reference to internal workflow nodes (`TM3 o agente narrativo`, `TM7 review`, etc.)
- `[TARGET]` prefix from JSON name fields recursively
- Footer `Auto-scaffold da on_crystallize.py...`

**CLI:**
```bash
# Promote single cycle
python promote_to_publish.py 20260503_0330 --force

# Promote all
python promote_to_publish.py --all --force

# Per-domain style
LAB_DATA_DIR=/path/to/lab-data DOMAIN=my-domain \
  python promote_to_publish.py --all
```

### 2. `finding_promoter.py`

LLM-driven: takes findings classified as `REVIEW_REQUIRED` by `finding_eligibility_gate.py` and asks an LLM whether they can be reformulated as **applicative** rules (predictive operator with concrete input/output) or are purely descriptive/methodological.

Provider chain: `codex-cli` (TM7 ChatGPT account) → `claude-cli` (OAuth subscription) → `openrouter` (HTTP, deepseek-v4-pro). Override via `LLM_PROVIDER_CHAIN`.

Discriminating, not yes-man — when findings are genuinely meta-scientific (no predictive operator extractable), the promoter rejects with high confidence.

**CLI:**
```bash
# Dry-run
python finding_promoter.py 20260503_0330

# Apply (writes promotions to finding_index.draft.json)
python finding_promoter.py 20260503_0330 --apply --min-confidence high
```

### 3. `blueprint_generator.py`

Generate self-contained markdown blueprint for a candidate (`library` / `kernel` / `demo`). Output is suitable for a human implementer to build the product manually:

- Header (title, type, verifier, status, generated)
- Origin (cycle, lab_instance, source finding, falsifier verdict)
- Scope (`what_it_does` + discovery context excerpt)
- Implementation skeleton (required inputs, expected artifacts)
- Acceptance criteria (success + falsification)
- Test plan template (Python pseudo-code)
- Risk register

**CLI:**
```bash
# Stdout
python blueprint_generator.py 20260501_1256 library

# To file
python blueprint_generator.py 20260501_1256 kernel --out BLUEPRINT.md
```

## Integration with cycle pipeline

Recommended order in your `run_ssp_pipeline.sh` or equivalent:

```bash
# 1. on_crystallize → scoperte/<ts>_<slug>_auto/lab-note.draft.md
python on_crystallize.py "$CYCLE_TS" --out-suffix=_auto

# 2. finding_eligibility_gate → soluzioni/<ts>_<slug>/finding_index.draft.json
python finding_eligibility_gate.py "$CYCLE_TS" --force

# 3. (optional) finding_promoter → upgrade REVIEW_REQUIRED → APPLICATIVE
python finding_promoter.py "$CYCLE_TS" --apply --min-confidence high

# 4. application_designer → manifest.draft.json
python application_designer.py "$CYCLE_TS" --force

# 5. promote_to_publish → published/<ts>_<slug>/
python promote_to_publish.py "$CYCLE_TS" --force

# 6. build_applications_index → INDEX + propagate to site
python build_applications_index.py
```

Step 3 is optional — without it, only findings auto-classified as `applicative_finding` proceed; with it, more findings get a chance to become products via LLM judgment.

## Design principles

1. **Domain-agnostic** — paths from env vars, no hardcoded domains.
2. **Sanitization separate from generation** — drafts can be messy with workflow notes; published artifacts are clean.
3. **Discriminating LLM prompts** — promoter asks for concrete rules, rejects vague reformulations with high confidence.
4. **Provider chain** — multiple LLM backends ranked by cost/availability, automatic fallback.
5. **Self-contained blueprints** — markdown with all info needed to implement, no external lookups required.

See `LAB_PATTERN.md` (top-level docs/) for the full architecture context.
