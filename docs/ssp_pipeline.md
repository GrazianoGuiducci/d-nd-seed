# SSP Pipeline — Scoperte / Soluzioni / Prodotti

> The autopoietic cycle does not stop at the report. It traverses 4 stages
> that take a scientific discovery to an empirically verified product —
> autonomously, with metrics on the table, and with the operator deciding
> the use case based on data, not a priori intuition.

---

## The 4 stages

The SSP pipeline runs after the cycle's `trajectory_evaluator` movement and
before `notify`. Each stage reads the output of the previous one and
applies a strict gate before continuing.

### Stage 1 — Scoperta (always runs)

**Trigger**: `on_crystallize.py <cycle_ts>`

The cycle's report becomes a publishable scoperta with metadata:
- `lab-note.draft.md` — the discovery statement, oriented to a public reader
- `cycle-report.draft.md` — the technical companion (claims, falsifier, refiner)

Status: `mature_eligible` · `transitional` · `pre_discovery`. The status is
derived from the falsifier high-flag count + valutatore decision. Pre-discovery
and transitional are visible (with `visible_risks` declared and disclaimer)
but **do not propagate to Stage 2+**.

Output: `LAB_DATA_DIR/<domain>/scoperte/<ts>_<slug>_auto/`

### Stage 1.5 — Eligibility gate (always runs)

**Trigger**: `finding_eligibility_gate.py <cycle_ts>`

Multi-signal classifier on each `Key Finding` of the report:
- `applicative_finding` — operative claim, computable consequence
- `literature_rediscovery` — known result, not new
- `methodology_note` — framework reflection, not operative
- `boundary_warning` — limit/constraint without quantitative claim
- `verdict_summary` — NEW/CONSTRAINT/CONFIRMED tag, not a discrete finding
- `negative_result` — "X has no closed form", "Y is not a family"
- `REVIEW_REQUIRED` — ambiguous, operator needed before Stage 2
- `ambiguous` — insufficient signal

No silent skip — every finding goes into `finding_index.draft.json` with
`scores`, `matched_signals`, and `skip_reason` if not eligible.

### Stage 2 — Application designer (mature_eligible only)

**Trigger**: `application_designer.py <cycle_ts>`

For each finding marked `application_eligible: true`, propose **3 candidate
applications** (canonical scaffold, all marked `[TARGET]`):

1. **library** — computational application (verifier_form: benchmark)
2. **kernel** — cognitive prompt template (verifier_form: human_review or dataset_comparison)
3. **demo** — interactive visualization (verifier_form: reproduction)

Each candidate carries a `verification_spec` with `required_inputs`,
`success_criteria`, `falsification_criteria`, `expected_artifacts`, `risks`.
Status: `SPEC_ONLY` — these specs say *how it would be verified*, not
*what was verified*.

Skip if scoperta is `pre_discovery` or `transitional` — claims not mature
enough to seed product proposals (override: `--force-pre-discovery`).

Output: `LAB_DATA_DIR/<domain>/soluzioni/<ts>_<slug>/manifest.draft.json` +
`finding_index.draft.json` (eligibility output) + `summary.draft.md`.

### Stage 4 — PoC runner empirico (multi-candidate)

**Trigger**: `stage4_poc_runner.py <cycle_ts> --auto` (default tests all 3 types)

For each candidate type (library, kernel, demo) of the chosen finding:
1. Build a prompt from the verification_spec + agent report excerpt + candidate metadata
2. Send to `claude-cli` (OAuth, no paid API) with `Write` tool only enabled —
   forces the LLM to produce a standalone Python file `poc.py` in the product
   directory (no internal execution, no shell, no network)
3. Execute `poc.py` sandboxed (timeout 90s, no network, deterministic if seeds
   are fixed). The script must define `method_naive(...)` and
   `method_informed(...)` and write `metrics.json` with at minimum
   `{naive_score, informed_score, delta, n_trials, details}`
4. Compare metrics against `success_criteria` / `falsification_criteria` of
   the verification_spec → verdict: `PASS` (delta > 0.05), `FAIL` (delta < -0.05),
   `INCONCLUSIVE` (marginal), `UNTESTABLE` (PoC declared the finding can't be
   A/B tested — e.g., it's a negative_result).

Output: `LAB_DATA_DIR/<domain>/prodotti/<id>/` containing `poc.py`,
`poc.log`, `metrics.json`, `verification.json` (real, not .spec),
`manifest.json`, `prompt.txt`.

The verdict on each type is **independent** — a finding can produce a
strong kernel and a weak library, or vice versa. Operator decides which
form is the use case.

### Stage 5 — Packaging (automated, claude-cli OAuth)

Implemented: `core/triggers/stage5_package.py`. Takes any product with
`verdict=PASS` from Stage 4 and generates an installable Python package
under `LAB_DATA_DIR/<domain>/prodotti/<id>/package/`:

- `pyproject.toml` (PEP 517, `setuptools.build_meta` backend)
- `src/<package_name>/__init__.py` + `kernel.py` — code refactored from
  `poc.py` as a reusable library, with `method_naive` / `method_informed`
  as public API plus a high-level `Kernel*` class
- `src/<package_name>/prompt_template.md` — versioned prompt template
  (only for type=`kernel`, the cognitive form of the finding)
- `tests/test_kernel.py` — at minimum: import smoke + A/B replication at
  reduced scale (deterministic, seed-fixed)
- `README.md` — what / why (citing the finding) / use case / install /
  quick start / verification table / lineage to the cycle
- `LICENSE`, `CHANGELOG.md`

Generation uses claude-cli with `Write` tool only (no Bash, no Edit).
Stage 5 runner then verifies: package importable via `PYTHONPATH=src` +
tests pass via `unittest discover`. Verdict: `PACKAGED` / `INCOMPLETE` /
`FAILED`. Output: `stage5_verification.json`.

The use case is provided by the operator (`--use-case "..."`) and lands
in README + CHANGELOG. The product becomes installable locally with
`pip install -e <package_dir>` and is ready for PyPI / npm publication
once the operator approves.

**Worked example**: the kernel `z=12,813` (Δ=+68.6pp) packaged as
`dnd_kernel_z_12_813_l_ordine_sequenziale` v0.1.0, verdict PACKAGED,
4 tests passing. Use case declared: "Kernel cognitivo D-ND installabile
per agenti LLM: predittore informato per sequenze con struttura Markov
nascosta."

---

## Why multi-candidate matters

If we tested only one type per finding (say, always `library`), we would
miss findings whose primary value is **cognitive** (kernel) or
**educational** (demo). Multi-candidate means: the system observes the
finding from 3 angles, gets 3 verdicts, and lets the operator align with
the strongest signal.

**Worked example** — finding `z = 12,813 — l'ordine sequenziale porta informazione massiva`
on prime gaps mod 6 (D-ND_LAB physics, cycle 20260501_1256):

| Type | Naive | Informed | Δ | Verdict |
|---|---|---|---|---|
| library | 41.5% | 48.6% | **+7.2pp** | PASS |
| kernel  | 31.2% | 99.7% | **+68.6pp** | PASS |
| demo    | 40.4% | 49.5% | **+9.1pp** | PASS |

All three PASS, but the **kernel cognitive form** has a margin one order
of magnitude larger than the library or demo form. Reading: this finding
is most powerful as a **prompt template / cognitive guide**, not as a
computational library. The operator now has data to choose the use case.

---

## Lineage

A14 cascade: every node that installs this seed gets the full SSP
pipeline. The procedure embodies the autopoietic cycle (A5) with strict
gates (Stage 1.5 + Stage 4 verdict) — the system produces what it
produces, but only what survives empirical verification becomes a product.

---

## Local instances

| Lab | Source | UI | Notes |
|---|---|---|---|
| MM_D-ND | `/opt/MM_D-ND/tools/triggers/` | `d-nd.com/ai-lab` (private research) | Source pipeline |
| D-ND_LAB physics | `/opt/D-ND_LAB/core/triggers/` | `lab.d-nd.com/dashboard/` | Sandbox + product UI |

The `core/ssp_pipeline.py` movement (D-ND_LAB) automatically chains all
4 stages post `trajectory_evaluator`. The cycle wakes up tomorrow with
scoperta + applicazioni + 3 prodotti verified, no manual step.
