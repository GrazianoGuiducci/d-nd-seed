# Researcher — Autonomous research cycle for your domain

> A system that observes a domain, picks a tension, runs, verifies, accumulates —
> and corrects the structure, not the symptom.

---

## What this is

The Researcher plugin installs an **autonomous nightly research cycle** in your
environment. You bring the domain (primes, markets, proteins, language, signals,
your data). The cycle brings the method: observe, run, autopsy, refine, accumulate.

It is not a pipeline of scripts. It is an AI agent that reads its field, chooses
one tension, writes an experiment, executes it, and produces a report. Another
separate observer watches the step itself (not the result) and proposes evolution.
An autopsy of the previous run is injected into the next run's field — the
system is aware of what happened last night when it starts tonight.

## Who this is for

- Researchers who have a domain but no automated loop for incremental discovery
- Analysts who track structural patterns across time
- Professionals conducting manual or ad-hoc inquiry who want to systematize
  it into an autonomous cycle that learns
- Thinkers who want a partner that runs while they sleep
- Anyone with a set of open questions, a structured domain, and the patience
  to let a system work

If you already have a sharp domain with structured tensions and you want the
experiment loop to run on its own, this is the seed.

## What you get

- **Nightly cycle** — an orchestrator that boots an AI instance, assembles the
  live field, picks a tension, runs one experiment, writes a report
- **Regressive autopsy** — before each run, the system classifies the previous
  outcome (completed / timeout-during-tool / api-error / report-missing / ...)
  and identifies the regressive node where the relational condition was missing.
  Pure I/O, no LLM call, cannot time out for the same reason the cycle can
- **Reflective observer (Affinatore)** — after each run, a separate AI observer
  analyzes the step itself (not the result), flags superfluous latency, proposes
  structural evolution. Degrades gracefully if it fails
- **Living field** — a fresh context assembled every run from seed, tensions,
  last reports, convergence map, autopsy health
- **Pluggable domain** — experiments live in your own `exp_*.py` files. The cycle
  runs your domain, not a fixed one

## Regressive Repair — the principle

When something breaks in the cycle, the fix does not live in the present where
the bug emerged. It lives in the upstream node where the relational condition
was missing. The bug is a signal of the node, not the object of the fix.

- **det=+1** — patch on the present (raise timeout, add retry, add reactive
  guard). Accumulates. The same shape of failure comes back.
- **det=-1** — inversion at the node (add the missing condition to the field,
  reduce scope, restructure so the failure form is no longer possible).
  Maturates upstream.

The autopsy names the regressive node. The next run's field receives it. The
agent decides, aware.

## Install

Requires: the base D-ND seed installed in your project (see root repo README).

```bash
# From your project root (where your seed is installed):
./install.sh profiles/example-researcher.json
```

The installer reads the researcher profile, adapts the templates to your
domain name and paths, writes the cycle agent, autopsy, affinatore, field
builder, and example experiment. Your domain-specific configuration goes in
`data/seed.json` (tensions, direction) and `data/agent_context.md` (guidance
for the nightly agent).

## Minimal setup — what you fill in

1. **Domain name** and **direction** (one sentence on what you are tracking)
2. **One or more tensions** (open questions, conjectures, structures to test)
3. **Your first `exp_*.py`** — a self-contained experiment the agent can run
   (optional; you can let the agent write the first one)

Everything else — the cycle, autopsy, affinatore, field builder, regressive
repair — is already wired.

## Output

Each night produces three artifacts:

1. **Scientific report** (`reports/agent_{TS}.md`) — what the agent found
2. **Structural health** (`lab_health.json`) — autopsy of the run (status,
   regressive node, recommendation)
3. **Evolution report** (`evolution/evolution_{TS}.md`) — the observer's read
   on the step itself, latency, possibilities

The morning brings all three. You read, decide, feed back into the seed.

## What this is not

- Not a research paper generator
- Not a benchmark suite
- Not a pipeline — the agent chooses its own next move within the field you
  gave it
- Not opinionated on domain — the method is the invariant, the domain is yours

## See also

- `GUIDE.md` — configure your domain
- `cycle/` — all the cycle components
- `config/` — seed and agent context templates
- Base seed kernels: `kernels/axioms.md` (A2 boundary, A5 autopoietic cycle,
  A8 autologic, A15 corrections-already-inside — the derivation of regressive
  repair)
- `docs/observation_precedes_proposal.md` — the methodological precondition
- `docs/directives_registry.md` — how directives propagate across your nodes
