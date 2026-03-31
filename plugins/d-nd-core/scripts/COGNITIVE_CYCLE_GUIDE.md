# Cognitive Cycle — Guide

A self-learning autonomous cycle. It runs, reflects, learns, adapts.

## What it does

Each run:
1. **Reads** memory from the previous cycle (what worked, what didn't, direction)
2. **Adapts** — skips ineffective phases, follows the direction
3. **Executes** — runs configured phases in sequence
4. **Reflects** — between phases, detects stalls (2/3 phases empty = stall)
5. **Learns** — records what produced, what didn't, the question for next time
6. **Persists** — saves memory for the next cycle

## How to use

### 1. Register phases

```python
from cognitive_cycle import CognitiveCycle

cycle = CognitiveCycle(memory_path='data/my_memory.json')

def my_research_phase():
    # do something
    return {'produced': True, 'summary': 'found 3 new patterns'}

def my_analysis_phase():
    # do something else
    return {'produced': False, 'summary': 'nothing new'}

cycle.add_phase('research', my_research_phase)
cycle.add_phase('analysis', my_analysis_phase, optional=True)
```

### 2. Run

```bash
python cognitive_cycle.py          # run with registered phases
python cognitive_cycle.py --status # show memory state
python cognitive_cycle.py --reset  # reset memory
```

### 3. Memory

The cycle stores memory in a JSON file:

```json
{
  "version": 1,
  "last_cycle": "2026-03-31T18:00:00",
  "learnings": [
    {
      "timestamp": "2026-03-31T18:00:00",
      "phases_total": 5,
      "phases_produced": 3,
      "what": "found patterns in crossing A×B",
      "effective": ["research", "crossing"],
      "ineffective": ["analysis"]
    }
  ],
  "effective_tools": ["research", "crossing"],
  "ineffective_tools": ["analysis"],
  "open_question": "What connects the A×B bridge with the C×D bridge?"
}
```

The next cycle reads this and adapts: it skips `analysis` (marked ineffective) and starts from the open question.

### 4. Reflection

Between phases, the cycle checks: are the last 3 phases producing nothing? If 2 out of 3 are empty, it signals a stall. This is not a stop — it's a signal to change direction.

### 5. Adaptation

Optional phases that were ineffective in the previous cycle are skipped. The cycle doesn't repeat what doesn't work. It tries something different.

## Integration with other tools

The cognitive cycle is a container. Fill it with phases from other tools:

- **Theory crossing** → one phase
- **Domandatore** (5 operators on a tension) → one phase
- **Eval** (measure what works) → one phase
- **Any custom research** → one phase

The cycle manages the learning loop. The phases do the work.

## When NOT to use

- For a single specific task → just do it
- When the operator gives a clear direction → follow the direction, don't cycle
- When the system needs input from outside → the cycle can't generate external input

## Principle

The cycle that doesn't learn is a loop. The cycle that learns is a spiral. Each run starts from where the previous one ended — not from scratch.
