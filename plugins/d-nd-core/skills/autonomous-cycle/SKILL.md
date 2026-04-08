---
name: autonomous-cycle
description: Seed-driven autonomous decision cycle. Loads project state from multiple sources, analyzes tensions and momentum, decides ONE action, executes it, verifies the outcome, and updates the seed. Use for autonomous research, maintenance, or any recurring decision-making process.
---

# Autonomous Cycle — Seed-Driven Decision Engine

A project seed (`seed.json`) tracks tensions, blocked potential, variance between cycles, and direction. The cycle reads the seed, integrates multiple sources, decides what to do, does it, and updates the seed.

## The Pattern

```
SEED (seed.json)
  |
  v
LOAD SOURCES (git log, data files, audit results, pipeline state)
  |
  v
ANALYZE (research state, artifact maturity, recent activity)
  |
  v
DECIDE (one action, ranked alternatives, confidence score)
  |
  v
EXECUTE (respecting autonomy levels: Auto / Notify / Approve / Escalate)
  |
  v
VERIFY (did the seed advance? did the action produce results?)
  |
  v
UPDATE SEED (new tensions, resolved tensions, variance, direction)
```

## Seed Structure

The seed is NOT a report (what happened). It IS a direction (where the potential points).

**`piano`**: a monotonic counter. Increments every time the cycle produces a meaningful change (tension resolved, new tension discovered, artifact advanced). If the piano doesn't advance for 3+ cycles, the system is in stasis — next cycle prioritizes a pivot. The piano is NOT a version number — it's a measure of movement.

```json
{
  "timestamp": "ISO-8601",
  "piano": 1,
  "tensioni": [
    {
      "tipo": "contraddizione|confine_inesplorato|simmetria_sospetta|scoperta|tensione_aperta",
      "id": "UNIQUE_ID",
      "claim": "What the tension is about",
      "intensita": 0.8,
      "nota": "Why this matters"
    }
  ],
  "potenziale_bloccato": [
    {
      "tipo": "bloccato",
      "id": "ID",
      "claim": "What can't proceed",
      "dettaglio": "What's missing"
    }
  ],
  "varianza": ["What changed since last cycle"],
  "direzione": "One sentence: where the potential is highest",
  "verifica": {"pass": 10, "fail": 1, "skip": 2, "total": 13}
}
```

## Decision Priority

The decisore ranks actions by type. The ordering reflects structural urgency: contradictions threaten consistency (must fix now), crystallization captures value before it fades, exploration opens new potential. The exact weights are configurable — what matters is the ordering:

1. **Contradiction** — theory and data diverge. Fix first or the system builds on inconsistency.
2. **Crystallize** — confirmed result not yet integrated. The context is still warm — capture it.
3. **Integrate** — mature artifact + fresh results. Bring them together while both are current.
4. **Explore** — open tension with high potential. Unknown territory — could unlock or be noise.
5. **Strengthen** — weakest link in the chain. The system is only as strong as its weakest point.
6. **Unblock** — blocked potential. Small effort might cascade into large movement.
7. **Pivot** — stasis detected (piano unchanged for 3+ cycles). Change approach.
8. **Publish** — artifacts ready but not distributed. Value exists but isn't reaching anyone.

## Autonomy Levels

Every action type has an autonomy level:

| Level | Actions | Behavior |
|-------|---------|----------|
| **Auto** | Lab experiments, seed update, data analysis | Execute and notify after |
| **Notify** | New scripts, minor fixes, state updates | Execute, notify immediately |
| **Approve** | Modify artifacts (papers, pages, code), new formalizations | Propose, wait for confirmation |
| **Escalate** | Modify axioms, contradictions in core, irreversible decisions | Ask the operator |

## Implementation

Use `seed_cycle.py` (in `scripts/`) as the generic engine. Configure via:

- `PROJECT_DIR` — root of the project
- `DATA_DIR` — where seed.json and results live
- `SOURCES` — dict of source loaders (functions that return state dicts)
- `ASSERTIONS` — list of testable claims with test functions
- `EXECUTORS` — dict mapping decision types to executor functions

## When to Use

- **Cron**: run the cycle on a schedule (nightly, hourly)
- **Post-session**: crystallize what happened into the seed
- **On demand**: "what should I do next?" — the decisore answers

## Cron Integration

```bash
# Example: nightly at 03:00
0 3 * * * cd /path/to/project && python seed_cycle.py --execute --update 2>&1 >> logs/cycle.log
```

## Verification

After execution, the cycle checks:
1. Did the seed piano advance? (piano_after > piano_before)
2. Did new tensions emerge or old ones resolve?
3. Was the action executed or only proposed?

If the piano didn't advance and no new tensions emerged, the system is in stasis. Next cycle will prioritize a pivot.

## Learning from Corrections

When the operator corrects an autonomous decision:
1. The correction becomes a rule (via auto-learn)
2. The rule persists in the seed or memory — the same mistake won't happen twice
3. If the correction reveals a structural gap (not just a wrong choice), update the decision priority ordering

When a cascade propagates successfully after an autonomous action, that's a positive signal: the decision was structurally sound. Track this — successful cascades reduce the "contradiction" tension in the next cycle.

## Cognitive Cycle Integration

The autonomous cycle is not isolated. It connects to the full cognitive flow:

```
Seed → Domandatore (5 operators on the top tension)
     → Projector (4 structural lenses on the field)
     → CEC (6 steps on the focus cluster)
     → Godel (invert the risks)
     → Crystallize → Update Seed
```

Not every cycle needs every tool. Use what the tension requires:
- Contradiction → Godel first (invert the assumption)
- Exploration → Domandatore first (generate discriminating questions)
- Many tensions → Projector first (map the field structure)

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
