# Domandatore — Guide

> An autopoietic research engine that takes a tension (open question)
> and applies 5 operators derived from duality logic to find the non-obvious answer.

## Quick Start

```bash
# Ask a single question
python domandatore.py --ask "Should I hire before or after revenue?"

# With a business domain (vocabulary + experiment banks)
python domandatore.py --ask "Flat pricing or per-seat?" --domain examples/business/domain.py

# Run from a seed file
python domandatore.py --seed examples/business/seed.json --domain examples/business/domain.py

# Run all tensions in the seed
python domandatore.py --seed seed.json --all
```

## The 5 Operators

Every tension passes through 5 question operators. Each one attacks the problem from a different angle:

| Operator | Question | What it does |
|----------|----------|-------------|
| **DUAL** | If X is true, what does 1/X say? | Inverts the claim. If "scaling is the solution", it tests "what if scaling is the problem?" |
| **BOUNDARY** | If A and B are opposites, what's at the border? | Finds the third option — the one that's neither A nor B but contains both |
| **DOMAIN** | If it holds here, does it hold there? | Tests the claim in a different domain. If true in pricing, is it true in hiring? |
| **BREAK** | What would break this claim? | Finds the conditions under which the claim fails |
| **SCALE** | Does it hold at large N as at small N? | Tests whether the claim survives scale changes |

## How to Use It Well

### 1. Start with a specific tension

A tension is a point where the choice isn't obvious.

Good: `"Flat pricing is simpler but per-seat pricing captures more value from larger customers"`
Bad: `"What pricing should I use?"` (too vague — nothing to invert or break)

### 2. One tension per run

Each run produces one report. If you have multiple questions, run them sequentially.
The Domandatore has a `split_tensions()` method that can help break complex inputs apart.

### 3. The BOUNDARY operator is often the most productive

It finds the "third included" — the option that resolves the apparent dichotomy.
- "Problem or promise?" → "Neither: a fact."
- "Hire early or late?" → "Hire one person now for the specific bottleneck."
- "Content or paid?" → "Paid to test, content to compound what works."

### 4. Use the results as constraints for the next question

The output of one run constrains the next. This is how the Domandatore becomes a
thinking sequence, not a single tool call:

1. "Should I open with the problem or the promise?" → Result: open with a fact
2. "When do I introduce the solution?" → Constraint: after the fact, not before
3. "What does the reader leave with?" → Constraint: coherent with both above

### 5. Read all 5 operators, not just BOUNDARY

- DUAL verifies robustness (if the inverse is also true, the claim is weak)
- BREAK finds the failure conditions (these become your risk map)
- SCALE tests limits (what works at 10 users may fail at 10,000)
- DOMAIN tests generality (if it only works in your context, it's fragile)

## Custom Domains

The Domandatore is domain-independent. To apply it to your field:

1. Create a domain file (see `examples/business/domain.py`)
2. Define:
   - `PRELUDE` — shared code injected into every experiment
   - `VOCABULARY` — measurable quantities with computation code
   - `BODIES` — experiment code blocks
   - `CATALOG` — named experiment banks with keyword routing
3. Run: `python domandatore.py --ask "your tension" --domain your_domain.py`

## Anti-patterns

- **Vague brief** → the operators echo the input without discriminating
- **Rhetorical question** ("should I write a good article?") → nothing to discriminate
- **Skipping responses** → questions without answers are noise
- **Self-reflection** ("what should I do now?") → the Domandatore discriminates external objects (decisions, strategies, architectures), not internal states. Use judgment for those.

## Architecture

```
Tension (input)
    │
    ├── DUAL operator    → inverted experiment
    ├── BOUNDARY operator → border experiment
    ├── DOMAIN operator   → cross-domain experiment
    ├── BREAK operator    → failure experiment
    └── SCALE operator    → scaling experiment
         │
         ▼
    Execute experiments
         │
         ▼
    Evaluate results (multi-level: JSON, named comparison,
                      transition detection, convergence, keyword)
         │
         ▼
    New tensions (discoveries, confirmations, open questions)
         │
         ▼
    Report (saved to results directory)
```

## Programmatic Use

```python
from domandatore import Domandatore

# Basic
engine = Domandatore(seed_path='seed.json')
report = engine.ask("Should I raise prices or add a free tier?")

# With custom domain
from examples.business.domain import PRELUDE, VOCABULARY, BODIES, CATALOG
engine = Domandatore(
    seed_path='seed.json',
    prelude=PRELUDE,
    vocabulary=VOCABULARY,
    bodies=BODIES,
    catalog=CATALOG,
)
report = engine.cycle()  # runs highest-intensity tension from seed

# Split complex input into tensions
tensions = engine.split_tensions(
    "Should I hire a marketer or a developer, and should I use equity or salary?"
)
for t in tensions:
    engine.cycle(t)
```

## License

MIT — use it, adapt it, build on it.
