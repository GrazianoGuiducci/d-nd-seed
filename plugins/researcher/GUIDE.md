# Researcher — Configure your domain

> The plugin is the method. Your domain goes in `data/seed.json` and
> `data/agent_context.md`. This guide shows how.

---

## The minimum viable seed

Every night the cycle reads your seed. The seed tells the agent:

- **Where you are** (current plan / direction)
- **What is open** (tensions — open questions, conjectures, structures to test)
- **What the agent should and should not do** (context + guardrails)

Two files, nothing else is required.

### `data/seed.json`

```json
{
  "piano": 1,
  "direzione": "One sentence on what you are tracking. Write as direction, not as goal.",
  "tensioni": [
    {
      "id": "NAME_OF_TENSION",
      "intensita": 0.9,
      "claim": "A falsifiable statement about your domain — the shorter the better.",
      "porta": "autonomia",
      "stato": "aperta"
    }
  ]
}
```

**Fields**:

- `piano` — integer, increments when the seed's plane shifts structurally
- `direzione` — one sentence, describes the direction (not the destination)
- `tensioni` — the open items the agent can pick from. Sort by `intensita`.
  Each tension needs an `id` (uppercase snake_case), a `claim` (falsifiable),
  and `stato` (aperta / verificata / falsificata / cimitero)

**A good tension is**:

- Falsifiable — it can be shown wrong by an experiment
- Structural — not a single data point, a pattern or relation
- Self-contained — the agent can pick it and work on it in one night
- Written in the language of your domain — the more precise, the better

**A bad tension is**:

- A to-do ("add feature X")
- A vague question ("what is interesting?")
- A task that requires multi-night coordination
- A re-run of something already resolved (send those to the graveyard)

### `data/agent_context.md`

Free-form markdown. Tell the agent about:

- Your domain (one paragraph)
- The concepts it needs (with short definitions)
- Errors to avoid (patterns you have already seen)
- Anti-patterns in your domain (fits that look significant but are not)
- The tools available (your `exp_*.py` files or external data)

Keep it under ~2k words. The agent reads this every night. Dead weight costs
tokens forever.

## The experiment convention

Experiments live in `tools/exp_*.py`. Each experiment:

- Is self-contained — the agent can run it without setup
- Takes at most 5-15 minutes to execute (the nightly budget is ~20 min total;
  the agent spends part of it reading, thinking, writing the report)
- Writes its raw data to `data/exp_{name}.json`
- Has a clear null baseline — compare against shuffle, random, or noise
- Does not require input outside the repo — no network, no live API

Template: `cycle/exp_example.py`.

**The agent can write new experiments.** If your tension calls for one that
doesn't exist, the agent writes `exp_new_thing.py`, runs it, produces the
report. It stays in the repo as a reusable tool for future runs.

## Regressive Repair in practice

When the nightly cycle breaks (and it will), do **not** raise the timeout, add
retries, or add reactive guards. Ask:

> What condition was missing in the field when the agent had to do the thing
> that broke?

Examples:

- Agent timed out regenerating a dataset from scratch → the dataset should have
  been in the field, pre-computed
- Agent wrote a report in a format the next step could not consume → the seed's
  expected output format was not in the context
- Agent picked a tension too wide for one night → the tensions need finer grain

The autopsy in `lab_health.json` names the regressive node. Fix there.

**Never**:

- Raise the nightly timeout (det=+1 — accumulation)
- Add reactive try/except that hides the failure (det=+1 — silencing the
  signal that pointed to the node)
- Patch the experiment code when the field was wrong (det=+1 — the next
  experiment will hit the same wall)

**Always**:

- Read `lab_health.json` and the regressive node it names
- Add the missing condition to the field upstream
- Let the next run decide, aware

## Affinatore — the second pair of eyes

After the scientific report is written, a separate AI instance (the Affinatore)
reads the session, the report, and the health. It observes the **step itself**,
not the result. It produces `evolution/evolution_{TS}.md` — proposals on:

- Where the cycle spent energy without producing
- Where the agent could have inverted earlier
- What possibilities the step opened (for the next cycle)

The Affinatore does not interrupt. Its output enters the field the next night
as consecutio — direction, not correction.

If the Affinatore fails (LLM call timeout, rate limit, whatever), the
scientific report is already saved. The health file marks
`affinatore_status: pending`. The next night's autopsy sees the signal.

## First run

```bash
# Dry-run: see what the agent would see, without calling the LLM
python3 cycle/build_field.py > /tmp/field_preview.md
cat /tmp/field_preview.md

# Run the full cycle once (manual trigger, not cron)
bash cycle/cycle_agent.sh
```

Read the three artifacts produced. Adjust the seed if the direction drifted.
Tomorrow's cron run will pick up your changes.

## Installing the nightly cron

```bash
# Edit your crontab
crontab -e

# Add the line (adjust path and hour to your preference)
30 3 * * * /path/to/your/project/cycle/cycle_agent.sh >> /path/to/logs/cycle.log 2>&1
```

Pick an hour when nothing else competes for resources. Give it a budget
(timeout in `cycle_agent.sh`) consistent with your experiments.

## Boundaries

The Researcher plugin does not:

- Decide what is interesting in your domain — that is your seed
- Validate findings against external datasets — that is your next step
- Publish anywhere — the artifacts stay local until you move them
- Coordinate with other nodes — for multi-node setups, see the base seed's
  Sinapsi pattern

The plugin does one thing: run the autonomous cycle well.

---

*The method is the invariant. Your domain is the variant. The seed carries both.*
