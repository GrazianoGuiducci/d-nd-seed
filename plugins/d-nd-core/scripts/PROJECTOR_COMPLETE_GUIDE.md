# Scenario Projector — Complete Guide

## What it is

**The Scenario Projector sees the future and indicates the path.**

It takes something that exists — a result, a response, an observed context — and projects forward: which possibilities open, which risks emerge, which paths become visible, how to structure strategies.

It is not diagnostic — it is projective. It does not analyze problems — it projects scenarios. Given a set of tensions (each a dipole with two sides), the projector maps how they relate and extracts: where to invest, what to protect, what risks emerge under stress, and what we are not seeing.

The projector comes AFTER the sieve. What survived doubt enters the projector and becomes direction.

**Principle**: every tension is a dipole D(claim, anti-claim). Dipoles resonate when they share concepts. The resonance pattern projected forward IS the strategy.

---

## Quick start (30 seconds)

```bash
# From a pre-configured domain
python scenario_projector.py --seed examples/startup_strategy.json --action-plan

# From your own seed
python scenario_projector.py --seed your_seed.json --strategy
```

No dependencies. Pure Python. Works anywhere.

---

## The 3 levels of output

### Level 1: Cross-check — "Is this solid?"

Each tension gets a structural verdict:

| Verdict | Meaning | What to do |
|---------|---------|------------|
| **confirmed** | Pillar — many connections, high support | Protect and amplify |
| **supported** | Backed by neighbors, not critical | Monitor |
| **contested** | Anti-claim contradicts a neighbor's claim | Investigate — there's a crack |
| **weak** | Few connections | Strengthen or deprioritize |
| **unverifiable** | Isolated — no one to verify it against | Explore or eliminate |

```bash
python scenario_projector.py --seed your_seed.json --cross-check
```

**Example output** (SaaS startup, 12 tensions):
```
✓ PRODUCT_MARKET_FIT    confirmed [PILLAR]  conn=5  support=100%
✓ DATA_MOAT             confirmed [PILLAR]  conn=5  support=80%
✗ HIRING_SPEED          contested [PILLAR]  conn=4  support=75%
    ✗ contradicted by: INTERNATIONAL
~ BURN_RATE              supported           conn=2  support=100%
? ENGINEERING_DEBT       weak                conn=0

Totale: 2 confirmed, 4 supported, 2 contested, 4 weak
```

Reading this: PRODUCT_MARKET_FIT and DATA_MOAT are structural pillars. HIRING_SPEED is a pillar but contested — hiring fast conflicts with international expansion (both need engineers). 4 tensions are isolated (weak) — either noise or blind spots.

### Level 2: Strategy — "Where should I focus?"

Extracts 5 categories from the field:

| Category | Question it answers |
|----------|-------------------|
| **Focus** | Where do tensions cluster? (natural convergence points) |
| **Leverage** | What are the structural pillars? (invest here, it propagates) |
| **Risks** | Where do contradictions sit? (cracks in the strategy) |
| **Blind spots** | What is isolated? (might be hiding something) |
| **Completed** | What is saturated? (done — free up attention) |

```bash
python scenario_projector.py --seed your_seed.json --strategy
```

### Level 3: Action plan — "What do I do first?"

Translates the strategy into prioritized actions with domain-specific language:

```bash
python scenario_projector.py --seed your_seed.json --action-plan
```

**Example output** (startup domain):
```
▶ [1] Strategic convergence — these decisions are coupled
  6 tensions share structural dependencies: competitor funding, data moat, founder bottleneck
  Risk: 1 contested
  
✗ [4] Growth risk — structural contradiction in the thesis
  HIRING_SPEED contested by INTERNATIONAL
  Risk: each bad hire costs 6 months and poisons culture

? [5] Under-explored — could be hidden opportunity or noise
  ENGINEERING_DEBT is disconnected from the field (0 connections)
```

---

## How to configure for your context

### Step 1: Write your seed

A seed is a JSON file with a direction and tensions:

```json
{
  "name": "My scenario",
  "context": "startup_strategy",
  "direction": "What you're trying to achieve",
  "tensions": [
    {
      "id": "SEMANTIC_ID",
      "claim": "The assertion — include both poles with 'but', 'however', 'while'"
    }
  ]
}
```

**Rules for good tensions:**
- **Include both poles**: "Revenue is growing *but* unit economics are negative" — the "but" creates the dipole
- **Use semantic IDs**: `PRICING_MODEL` carries meaning, `T1` does not. The ID contributes to concept extraction
- **10-15 tensions** is the sweet spot. Fewer gives sparse results, more gets noisy
- **Use `"gate": "confirmed"` or `"gate": "falsified"`** for resolved tensions — they become saturated and free up potential

### Step 2: Choose or create a domain

5 pre-configured domains with domain-specific language:

| Domain | Context key | Best for |
|--------|------------|----------|
| Startup Strategy | `startup_strategy` | Founders deciding where to focus |
| Product Roadmap | `product_roadmap` | PMs prioritizing with limited resources |
| Due Diligence | `due_diligence` | Investors cross-checking a thesis |
| Risk Assessment | `risk_assessment` | Teams managing transformation risks |
| Portfolio Management | `portfolio_management` | Allocations and hedging |

To add your own domain, add an entry to `_DOMAIN_LABELS` in `scenario_projector.py`:

```python
'your_domain': {
    'focus': 'What convergence means in your context',
    'risk': 'What contradictions mean',
    'blind_spot': 'What isolation means',
    'leverage': 'What pillars mean',
},
```

### Step 3: Run and iterate

```bash
# Start with cross-check to see the landscape
python scenario_projector.py --seed your_seed.json --cross-check

# Then strategy for the categories
python scenario_projector.py --seed your_seed.json --strategy

# Then action-plan for priorities
python scenario_projector.py --seed your_seed.json --action-plan

# Or full exploration (trajectory + passages + field)
python scenario_projector.py --seed your_seed.json --explore
```

After the first run: add tensions you missed, mark resolved ones as confirmed/falsified, re-run. The field evolves.

---

## Pre-configured examples

Each example is ready to run in `examples/`:

### Startup Strategy (12 tensions)
```bash
python scenario_projector.py --seed examples/startup_strategy.json --action-plan
```
B2B SaaS post-seed, $2M ARR, preparing Series A. Maps hiring speed vs international expansion, product-market fit as pillar, engineering debt as blind spot.

### Product Roadmap (13 tensions)
```bash
python scenario_projector.py --seed examples/product_roadmap.json --strategy
```
Feature prioritization with competing user segments, platform vs tool decision, API-first vs UI-first trade-offs.

### Due Diligence (14 tensions)
```bash
python scenario_projector.py --seed examples/due_diligence.json --cross-check
```
Investment thesis verification. Revenue quality, customer concentration, competitive dynamics, governance structure.

### Risk Assessment (12 tensions)
```bash
python scenario_projector.py --seed examples/risk_assessment.json --action-plan
```
Digital transformation risk mapping. Cloud migration, vendor lock-in, cybersecurity, regulatory compliance.

### Portfolio Management (seed available)
```bash
python scenario_projector.py --seed examples/portfolio_management.json --strategy
```
Correlated positions, hedging gaps, structural fragility under stress.

---

## Integration patterns

The projector works at 5 different levels. Choose what fits your context.

### Pattern 1: Standalone CLI

Run directly on a seed file. Best for: one-time analysis, manual exploration.

```bash
python scenario_projector.py --seed my_scenario.json --action-plan
```

### Pattern 2: Python library

Import and use in any Python code. Best for: automated pipelines, custom workflows.

```python
from scenario_projector import ScenarioProjector

sp = ScenarioProjector(seed_data={
    'context': 'startup_strategy',
    'direction': 'Scale to $8M ARR in 18 months',
    'tensions': [
        {'id': 'PRICING', 'claim': 'Moving upmarket increases ACV but lengthens sales cycles'},
        {'id': 'HIRING', 'claim': 'Hiring fast captures the window but bad hires cost 6 months'},
        # ...
    ]
})

checks = sp.cross_check()
strat = sp.strategy()
plan = sp.action_plan()
result = sp.run('full')  # everything at once
```

### Pattern 3: API endpoint

Expose as a REST API for web applications. Best for: SaaS products, funnel integration.

```javascript
// Node.js — see services/projector.js for the JS port
const { ScenarioProjector } = require('./services/projector');

app.post('/api/projector', (req, res) => {
    const { context, tensions, source } = req.body;
    const projector = new ScenarioProjector(tensions, context);
    const result = projector.run('demo'); // cross_check + summary
    res.json(result);
});
```

The API can track what people bring (insight accumulator):
```javascript
// After each call, log: which domain, which verdicts, which patterns are contested
accumulateInsight(context, result, source);
// The system learns from use — the narrative evolves
```

### Pattern 4: Inside the Cognitive Cycle (CEC)

The projector takes the **risultante** (output of the CEC sieve) and projects forward:

```
Tension enters
    ↓
CEC (the sieve — 6 phases, contains everything):
    ├── Condizioni    — observe the field
    ├── Firma         — extract invariant structure
    ├── Espansione    — 5 discriminating angles (Domandatore)
    ├── Inversione    — flip the hidden assumption (Godel)
    ├── Verifica      — 6 independent tests
    └── Risultante    — what survives doubt
    ↓
Projector → takes the risultante, applies 4 lenses (focus, leverage, risk, blind spot)
    ↓
Direction → where the risultante points, what to do, what risks remain
    ↓
Seed updates → the cycle restarts with new tensions
```

The projector does NOT come before the CEC. It comes after. It works on filtered, crystallized tensions — the output of the sieve — not on raw input.

Integration via `projector_phase.py`:
```python
from projector_phase import projector_phase

# In your cognitive cycle, AFTER crystallization (not before)
result = projector_phase(seed_path='seed.json')
# Returns: confirmed count, contested count, leverage points, blind spots
```

### Pattern 5: Interactive funnel

Build a user-facing funnel that collects tensions and projects them. Best for: consulting, decision support.

Flow:
1. User selects a context (founder, product manager, investor, analyst)
2. User selects tensions from pre-configured dipoles (3-4 steps, multi-select)
3. System calls the projector with selected tensions
4. System shows verdicts, strategy summary, CTA for deeper analysis

The frontend sends:
```json
{"context": "startup_strategy", "tensions": [...], "source": "funnel"}
```

The projector returns cross-check + summary. The funnel renders verdicts with color-coded badges: green (confirmed), amber (contested), gray (weak).

---

## The 4 structural lenses

These are the cognitive framework behind the projector. They work with or without code.

### 1. FOCUS — Where tensions converge
"If I resolve this, which others move with it?"
Clusters of 3+ interconnected tensions = natural action points.

### 2. LEVERAGE — The pillars
"If I remove this, what collapses?"
Pillars with 4+ connections and high support = foundations to protect.

### 3. RISK — Where contradictions live
"What am I assuming that contradicts another assumption?"
Anti-claim of A matches claim of B = structural crack.

### 4. BLIND SPOT — What is disconnected
"Why is this alone? Did I forget something?"
Isolated tensions = noise, hidden potential, or real blind spots.

**Full guide**: see `STRUCTURAL_LENSES_GUIDE.md`

---

## How the projector works internally

1. **Concept extraction**: each tension yields concepts from its claim, anti-claim, and ID. Stemming normalizes ("protection" and "protect" match).

2. **Dipole field**: every claim generates an anti-claim (the text after "but", "however", "while" — or auto-generated).

3. **Assonance matrix**: binary matrix — two dipoles resonate if they share 1+ concepts (2+ for long claims). This is not correlation — it's structural overlap.

4. **Lagrangian trajectory**: follows the path of maximum potential release through the assonance field. The steps with highest δV are the productive moves.

5. **Cross-check**: each tension checked from 4 angles — neighborhood (who resonates?), removal (what disconnects if you remove it?), support (neighbors at high potential?), contradiction (anti-claim matches a neighbor's claim?).

6. **Strategy + Action plan**: the cross-check results, grouped by the 4 lenses, translated into domain-specific language.

---

## Creating a new domain from scratch

Example: you want to analyze **hiring decisions** for a scale-up.

### 1. Define the seed

```json
{
  "name": "Scale-up Hiring — Q3 2026",
  "context": "hiring_decisions",
  "direction": "Hire 20 people in 3 months without losing culture or burning cash",
  "tensions": [
    {
      "id": "SPEED_VS_QUALITY",
      "claim": "Hiring fast fills the gap but bad hires cost 6 months and poison the team"
    },
    {
      "id": "SENIOR_VS_JUNIOR",
      "claim": "Seniors deliver faster but cost 2x and expect autonomy we can't give yet"
    },
    {
      "id": "REMOTE_VS_OFFICE",
      "claim": "Remote widens the pool 10x but culture transmission requires physical presence"
    },
    {
      "id": "REFERRAL_BIAS",
      "claim": "Referrals produce better hires but create homogeneous teams that miss market shifts"
    },
    {
      "id": "EQUITY_BUDGET",
      "claim": "Equity attracts believers but dilutes the cap table before Series B"
    }
  ]
}
```

### 2. Add domain labels (optional)

In `scenario_projector.py`, add:
```python
'hiring_decisions': {
    'focus': 'Hiring cluster — these decisions interact',
    'risk': 'Hiring conflict — these constraints contradict each other',
    'blind_spot': 'Unexamined — this hiring dimension is disconnected',
    'leverage': 'Hiring foundation — get this right and the rest follows',
},
```

### 3. Run

```bash
python scenario_projector.py --seed hiring_q3.json --action-plan
```

### 4. Iterate

After the first run:
- Add tensions you missed (compensation structure? employer brand? internal mobility?)
- Mark resolved tensions with `"gate": "confirmed"` or `"gate": "falsified"`
- Re-run — the field evolves, new clusters emerge

---

## From guide to narrative

This guide is the territory. The narrative for a website, a presentation, or a pitch is the map derived from it.

**What the guide says** → **What the narrative shows**:
- "Cross-check reveals structure" → "Your tensions have a pattern you can't see"
- "4 lenses extract insight" → "Where to invest, what to protect, what you're missing"
- "The projector takes the risultante and projects forward" → "From what survived, here's where it leads"
- "Iterate: add, resolve, re-run" → "Every decision updates the map"

The narrative doesn't describe the projector. It describes what happens to the person who uses it. They arrive with a mess of competing decisions. They leave with a structural map: pillars to protect, cracks to investigate, blind spots to explore, and a prioritized action plan.

That is the story.

---

## Related guides

| Guide | What it covers |
|-------|---------------|
| `SCENARIO_PROJECTOR_GUIDE.md` | CLI reference, API usage, format details |
| `STRUCTURAL_LENSES_GUIDE.md` | The 4 lenses as cognitive framework |
| `examples/DOMAINS_GUIDE.md` | Pre-configured domains, how to adapt |
| `COGNITIVE_CYCLE_GUIDE.md` | How the projector fits in the full cycle |
| `DOMANDATORE_GUIDE.md` | Generating tensions (input for the projector) |
