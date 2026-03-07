# Autopoietic Cycle Pattern — Self-Generating Knowledge

> How to build a system that asks its own questions, tests its own answers,
> and grows its own knowledge. The cycle that feeds itself.

## The Problem

AI systems answer questions. But who asks the questions? If the human stops
asking, the system stops growing. An autopoietic system generates its own
questions from its own tensions — gaps, contradictions, untested claims.

## The Cycle

```
Tension → Questioner → Experiment → Execution → Result → New Tension
    ↑                                                          |
    └──────────────────────────────────────────────────────────┘
```

Each result either resolves a tension (confirmed/falsified) or generates
new tensions (unexpected findings, edge cases, contradictions).

## Core Components

### 1. The Seed (tensions)

A tension is an open question in your system. It has:
- A **claim**: something you believe but haven't tested
- A **confidence**: how sure you are (0-1)
- A **domain**: where it lives in your system

```json
{
  "id": "T-001",
  "claim": "The cache invalidation handles concurrent writes correctly",
  "confidence": 0.3,
  "domain": "infrastructure",
  "status": "open",
  "source": "code review observation"
}
```

### 2. The Questioner (operators)

The questioner takes a tension and generates experiments using question
operators. Each operator attacks the claim from a different angle:

| Operator | Logic | Example |
|----------|-------|---------|
| **Dual** | If X is true, what about 1/X? | "If the cache works for writes, what about deletes?" |
| **Boundary** | If A and B are opposites, what's at the edge? | "What happens at exactly the TTL expiry moment?" |
| **Domain** | If it works here, does it work there? | "Does it work under high load, not just unit tests?" |
| **Break** | What would break this claim? | "What input would cause cache corruption?" |
| **Scale** | Does it work at N=1M as well as N=10? | "Does performance degrade at 100k concurrent keys?" |

### 3. The Experiment

An experiment is executable. It has:
- An **hypothesis**: what you expect
- **Code**: something that runs and produces data
- A **criterion**: how to judge success or failure

### 4. The Evaluator

The evaluator classifies results:

| Level | Meaning | Action |
|-------|---------|--------|
| **Confirmed** | Claim holds under this test | Increase confidence, mark tension resolved |
| **Weakened** | Claim partially holds | Generate narrower tension |
| **Falsified** | Claim fails | Generate fix tension, decrease confidence |
| **Unexpected** | Result outside predictions | Generate new tension (discovery) |

## Questioner (Python example)

```python
import json
from pathlib import Path
from datetime import datetime

TENSIONS_FILE = Path('data/tensions.json')
RESULTS_DIR = Path('data/experiments')

def load_tensions():
    if TENSIONS_FILE.exists():
        return json.loads(TENSIONS_FILE.read_text())
    return []

def save_tensions(tensions):
    TENSIONS_FILE.write_text(json.dumps(tensions, indent=2))

# ── Question Operators ──────────────────────────────────

def operator_dual(tension):
    """If X is true, what about 1/X?"""
    claim = tension['claim']
    return {
        'id': f"EXP-{tension['id']}-dual",
        'operator': 'dual',
        'hypothesis': f'The inverse of "{claim[:60]}" also holds',
        'tension_id': tension['id'],
        'generated': datetime.now().isoformat()
    }

def operator_boundary(tension):
    """What happens at the edge?"""
    claim = tension['claim']
    return {
        'id': f"EXP-{tension['id']}-boundary",
        'operator': 'boundary',
        'hypothesis': f'"{claim[:60]}" holds at the boundary condition',
        'tension_id': tension['id'],
        'generated': datetime.now().isoformat()
    }

def operator_break(tension):
    """What would break this claim?"""
    claim = tension['claim']
    return {
        'id': f"EXP-{tension['id']}-break",
        'operator': 'break',
        'hypothesis': f'There exists an input that falsifies "{claim[:60]}"',
        'tension_id': tension['id'],
        'generated': datetime.now().isoformat()
    }

def operator_scale(tension):
    """Does it work at different scales?"""
    claim = tension['claim']
    return {
        'id': f"EXP-{tension['id']}-scale",
        'operator': 'scale',
        'hypothesis': f'"{claim[:60]}" holds at 100x the current scale',
        'tension_id': tension['id'],
        'generated': datetime.now().isoformat()
    }

def operator_domain(tension):
    """Does it work in a different context?"""
    claim = tension['claim']
    return {
        'id': f"EXP-{tension['id']}-domain",
        'operator': 'domain',
        'hypothesis': f'"{claim[:60]}" transfers to a different domain',
        'tension_id': tension['id'],
        'generated': datetime.now().isoformat()
    }

OPERATORS = [operator_dual, operator_boundary, operator_break,
             operator_scale, operator_domain]

def generate_experiments(tension, max_ops=3):
    """Apply question operators to a tension."""
    experiments = []
    for op in OPERATORS[:max_ops]:
        experiments.append(op(tension))
    return experiments


# ── Evaluator ───────────────────────────────────────────

def evaluate_result(experiment, result):
    """
    Classify the result and generate follow-up tensions.

    result: { 'passed': bool, 'data': any, 'unexpected': bool, 'notes': str }
    """
    tension_id = experiment['tension_id']
    tensions = load_tensions()
    tension = next((t for t in tensions if t['id'] == tension_id), None)
    if not tension:
        return None

    if result.get('unexpected'):
        # Discovery — generate new tension
        new_tension = {
            'id': f"T-{len(tensions)+1:03d}",
            'claim': f"Unexpected finding from {experiment['id']}: {result.get('notes', '')}",
            'confidence': 0.1,
            'domain': tension['domain'],
            'status': 'open',
            'source': experiment['id']
        }
        tensions.append(new_tension)
        save_tensions(tensions)
        return {'level': 'unexpected', 'new_tension': new_tension['id']}

    elif result['passed']:
        # Confirmed — increase confidence
        tension['confidence'] = min(1.0, tension['confidence'] + 0.2)
        if tension['confidence'] >= 0.9:
            tension['status'] = 'confirmed'
        save_tensions(tensions)
        return {'level': 'confirmed', 'new_confidence': tension['confidence']}

    else:
        # Falsified or weakened
        tension['confidence'] = max(0.0, tension['confidence'] - 0.3)
        fix_tension = {
            'id': f"T-{len(tensions)+1:03d}",
            'claim': f"Fix needed: {tension['claim']} fails under {experiment['operator']}",
            'confidence': 0.0,
            'domain': tension['domain'],
            'status': 'open',
            'source': experiment['id']
        }
        tensions.append(fix_tension)
        save_tensions(tensions)
        return {'level': 'falsified', 'fix_tension': fix_tension['id']}


# ── Full Cycle ──────────────────────────────────────────

def run_cycle(max_tensions=3):
    """
    One cycle of the autopoietic engine.
    Select open tensions, generate experiments, return them for execution.
    """
    tensions = load_tensions()
    open_tensions = [t for t in tensions if t['status'] == 'open']

    # Priority: lowest confidence first
    open_tensions.sort(key=lambda t: t['confidence'])
    selected = open_tensions[:max_tensions]

    cycle = {
        'cycle_id': f"CYC-{datetime.now().strftime('%Y%m%d-%H%M')}",
        'tensions': len(open_tensions),
        'selected': len(selected),
        'experiments': []
    }

    for tension in selected:
        experiments = generate_experiments(tension)
        cycle['experiments'].extend(experiments)

    return cycle


if __name__ == '__main__':
    # Initialize with example tensions if empty
    if not load_tensions():
        save_tensions([
            {
                'id': 'T-001',
                'claim': 'The system maintains context across compactions',
                'confidence': 0.5,
                'domain': 'context',
                'status': 'open',
                'source': 'initial'
            },
            {
                'id': 'T-002',
                'claim': 'Safety guards catch all destructive patterns',
                'confidence': 0.7,
                'domain': 'safety',
                'status': 'open',
                'source': 'initial'
            }
        ])

    cycle = run_cycle()
    print(json.dumps(cycle, indent=2))
    print(f"\nGenerated {len(cycle['experiments'])} experiments from {cycle['selected']} tensions")
```

## The Knowledge State

Track what you know and what you don't:

```json
{
  "area": "authentication",
  "known": ["OAuth2 flow works", "Token refresh tested"],
  "unknown": ["Concurrent session handling", "Token revocation under load"],
  "last_jump": "2026-03-01 — confirmed OAuth2 edge case"
}
```

The ratio `known / (known + unknown)` is your coverage. The autopoietic cycle
works to expand both: confirming claims increases `known`, discovering gaps
increases `unknown`. Growth is when `unknown` grows faster than `known` —
it means you're exploring, not just confirming.

## Integration with Self-Maintenance

The custodian (see `self_maintenance.md`) can feed the autopoietic cycle:

- **Anomaly found** → generates a tension ("this shouldn't happen")
- **Fix applied** → generates a test tension ("the fix actually works")
- **Drift detected** → generates a domain tension ("does the new version still pass?")

## Discipline

- Don't run the cycle constantly. Once per day or per significant change.
- Not every tension deserves 5 operators. Start with `break` and `scale`.
- The cycle is NOT CI/CD. It generates KNOWLEDGE, not green checkmarks.
- If all tensions are confirmed at 0.9+, you're not asking hard enough questions.
