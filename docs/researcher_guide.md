# Researcher — from domain to autonomous cycle

> A structured domain + a system that runs every night + a way to know where
> you are in the morning. The plugin brings the cycle. You bring the domain.

---

## The idea

You have a domain. Primes, markets, proteins, language, signals, historical
data, whatever your inquiry covers. It has structure. It has open questions.
You can state tensions — falsifiable statements — about it.

Every night you could pick one tension, design an experiment, run it against
a null baseline, write what you found. You could do this for years. It would
converge.

The Researcher plugin automates this. You write the seed — direction and
tensions — and go to bed. The cycle reads your seed, picks a tension, writes
or reuses an experiment, executes it, produces a report. A second observer
(the Refiner) looks at the step itself and proposes evolution. Before the
next run, an autopsy of the previous one tells the system what happened.

In the morning you read three artifacts:

1. **Scientific report** — what the agent found
2. **Structural health** — whether the run completed, and if not, where the
   missing condition was
3. **Evolution report** — the observer's read on the step, the latency, the
   possibilities

You read. You update the seed. Tomorrow's run picks up your changes.

---

## What this is good for

- Long-running inquiry that benefits from incremental, autonomous exploration
- Domains where numerical signals, structural patterns, or falsifiable
  conjectures can be tested experimentally
- Workflows where you currently run ad-hoc scripts manually and want the
  loop to close on its own
- Work where the method matters more than any single result — the cycle
  is a way to keep discipline over time

## What this is not good for

- One-shot questions — use a regular AI coder session for those
- Domains without structure — the cycle needs tensions it can pick from
- Work that requires real-time data or external API calls during the run
- Pipelines with hard dependency chains — the cycle picks one thing per night

---

## The three principles

**1. Observation precedes proposal.** Before the cycle suggests anything, it
reads. The living field is assembled fresh every night from your seed, last
reports, convergences, and the autopsy. Nothing is invented.

**2. The method is the invariant.** The cycle itself does not know your
domain. You tell it. Primes or markets, physics or linguistics — the cycle
runs the same loop. Your domain changes, the method does not.

**3. Structure, not symptom.** When something in the cycle breaks, the fix
does not live in the present where the bug emerged. The autopsy names the
upstream node where the relational condition was missing. The next run's
field carries this. The agent decides, aware. Do not raise timeouts, add
retries, or add reactive guards — that accumulates. Walk back to the node.

---

## The cycle flow

```
    ┌── previous run's session + report
    │
    ▼
  AUTOPSY ──► lab_health.json  ──┐
  (pure I/O, no LLM, no timeout) │
                                  │
                                  ▼
  SEED (your domain) ──► LIVING FIELD (assembled fresh)
                                  │
                                  ▼
                          ┌── AGENT (AI instance)
                          │   - picks ONE tension
                          │   - writes or reuses an experiment
                          │   - runs it, compares to null
                          │   - writes report
                          └──► scientific_report.md
                                  │
                                  ▼
                          REFINER (separate AI observer)
                          - observes the step, not the result
                          - proposes structural evolution
                          └──► evolution_report.md
                                  │
                                  ▼
                          Morning: you read three artifacts
```

The cycle is one cron job (e.g. `30 3 * * *`). Everything else is driven by
the seed.

---

## Install

Requires: the base D-ND seed installed in your project.

```bash
# From your project root
./install.sh profiles/example-researcher.json
```

The installer:

1. Reads `example-researcher.json`, prompts for your domain name, direction,
   paths
2. Writes `cycle/` into your project with autopsy, refiner, field builder,
   orchestrator (`cycle_agent.sh`), example experiment
3. Writes `config/seed.json` (your seed) and `config/AGENT_CONTEXT.md` (your
   domain context for the agent)
4. Prints the cron line for you to add

Minimum you need to customize before first run:

- `seed.json` — at least one tension with a real claim
- `AGENT_CONTEXT.md` — a paragraph about your domain
- (Optional) One `exp_*.py` — or let the agent write the first one

---

## Outputs

After the first night, you will find:

```
data/
├── seed.json                      ← your seed (edited manually)
├── seed_backup_pre_run.json       ← safety backup (auto)
├── lab_health.json                ← autopsy: status + regressive node
├── reports/
│   ├── agent_YYYYMMDD_HHMM.md     ← scientific report
│   ├── agent_YYYYMMDD_HHMM_raw.log ← raw CLI output
│   └── ...
└── evolution/
    └── evolution_YYYYMMDD_HHMM.md ← refiner's observation
```

Read the three `.md` files. Update the seed. Repeat.

---

## Scaling

**After weeks**: tensions accumulate. Some get verified, some falsified, some
go to the graveyard. The seed becomes a living map of what your domain has
told you.

**After months**: the `evolution_report.md` timeline shows where your cycle
spent energy, where it found structure, where you invested wrong. This is the
meta-signal — what the method itself learned about your domain.

**After a year**: you have a system that has run ~300 autonomous experiments,
produced ~300 autopsies, ~300 refinements. No session was lost. Each morning
started from where the previous night arrived.

---

## Relation to the base seed

The Researcher plugin is one of several profiles the D-ND seed supports
(Coder, Thinker, Publisher, Researcher, Team). It shares the kernel (axioms,
base identity, safety guard, memory, cascade propagation) with the other
profiles. The cycle is specific to Researcher.

If you installed the base seed first and already have skills like
`auto-learn`, `autologica`, `cec`, `autoresearch`, these work alongside the
Researcher cycle. The cycle is the outer loop; the skills are the inner
operations.

---

*A domain that deserves rigor, a method that runs while you sleep, a morning
where you read what the night produced.*
