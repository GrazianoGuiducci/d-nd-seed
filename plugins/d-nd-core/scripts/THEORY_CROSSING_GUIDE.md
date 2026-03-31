# Theory Crossing — Guide

Cross any set of theories. Find what lives between them.

## What it does

Takes N theories (each with a constant and a name). For every pair:
- **Relational constant** — the ratio between their fundamental constants. Belongs to neither theory. Lives in the middle.
- **Zero dipole** — the two theories disagree on what zero means. The disagreement is the structure, not a problem.
- **Bridge** — a physical object or concept that exists only at the intersection of the two theories.
- **Void** — where no bridge exists. Not a gap — the highest potential.

## The mechanic

```
2 theories → 1 pair → 1 constant, 1 dipole, 1 bridge (or void)
3 theories → 3 pairs → 3 constants, 3 dipoles, 3 bridges, 1 triangulation
4 theories → 6 pairs → 6 of each, 4 triangulations, 1 total object
N theories → C(N,2) pairs, C(N,3) triangulations
```

## How to use

### 1. Create a theories file

```json
{
  "theories": [
    {"key": "A", "name": "Theory A", "constant_name": "alpha", "constant_symbol": "a"},
    {"key": "B", "name": "Theory B", "constant_name": "beta", "constant_symbol": "b"},
    {"key": "C", "name": "Theory C", "constant_name": "gamma", "constant_symbol": "g"}
  ],
  "bridges": {
    "AxB": {
      "bridge": "The AB bridge",
      "zero_dipole": "discrete/continuous",
      "relational_constant": "a/b"
    },
    "BxC": {
      "bridge": "The BC bridge",
      "zero_dipole": "static/dynamic",
      "relational_constant": "b*g"
    }
  }
}
```

Leave a pair without a bridge entry to mark it as a void.

### 2. Run

```bash
python theory_crossing.py theories.json    # full crossing
python theory_crossing.py --questions      # show fundamental questions
```

### 3. Read the output

The crossing produces:
- **Fundamental questions**: for each pair with a zero dipole, the question "How do X and Y coexist?" with the bridge as answer (or void).
- **Bridge crossings** (second level): two bridges that share a theory are related. The pivot theory connects them.
- **Pivot frequency**: which theory appears most as a pivot. The theory with fewest connections may have voids around it.

### 4. Feed voids back

When a pair has no bridge, the void itself can be treated as a theory and crossed with the others. This is the autologica applied to the crossing: the system feeds its own gaps back as inputs.

## Fundamental questions

Every pair with a zero dipole generates a question:

```
How do [D-side] and [ND-side] coexist?
→ Answer: [bridge] or [VOID]
```

The questions with answers are the knowledge we have. The question without an answer is the knowledge we don't have — and the highest potential.

## Design choices

- **Theories are provided, not discovered.** The crossing doesn't find theories — it finds what's between them.
- **Bridges are declared, not computed.** The user provides known bridges. The system reveals where bridges are missing.
- **The mechanic is combinatorial.** Adding one theory multiplies the crossings. Start small.
- **The void is a feature.** Where there's no bridge, there's the most interesting question.

## Integration

Use inside a cognitive cycle as one phase:

```python
from theory_crossing import run

def crossing_phase():
    result = run('my_theories.json')
    return {
        'produced': result['voids'] > 0 or result['bridge_relations'] > 0,
        'summary': f"{result['crossings']} pairs, {result['voids']} voids"
    }

cycle.add_phase('crossing', crossing_phase)
```
