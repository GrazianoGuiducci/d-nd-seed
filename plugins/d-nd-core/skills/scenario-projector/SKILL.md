---
name: scenario-projector
description: "Structural scenario projection from tensions. Use when facing complex decisions with 5+ competing factors, when cross-checking a strategy or thesis, when prioritizing with limited resources, or when mapping risks."
user-invocable: true
---

# Scenario Projector — Structural Decision Support

Not a prediction tool. A structural lens.
The structure contains the answer — don't interpose numbers between structure and decision.

## When to use

- Before a strategic decision with competing tensions
- When cross-checking a plan, thesis, or roadmap
- When prioritizing with limited resources
- When mapping risks and their correlations
- When the CEC or Domandatore reveals 5+ tensions and you need to see the field

## How it works

Every tension is a dipole D(claim, anti-claim). The anti-claim isn't negation — it's the other pole.
Dipoles resonate (binary: yes/no). The trajectory follows maximum potential.

4 structural lenses:

| Lens | What it reveals |
|------|-----------------|
| **Focus** | Where tensions converge — natural action points |
| **Leverage** | Structural pillars — invest here, it propagates |
| **Risk** | Anti-claim contradicts a neighbor — crack in the thesis |
| **Blind spot** | Isolated from the field — unexplored or noise |

## Usage

### From Python

```python
import sys
# Find scenario_projector.py in the seed scripts directory
# Typical location: d-nd-seed/plugins/d-nd-core/scripts/
sys.path.insert(0, '/path/to/d-nd-seed/plugins/d-nd-core/scripts')
from scenario_projector import ScenarioProjector

# From tensions directly
sp = ScenarioProjector(seed_data={
    'context': 'startup_strategy',  # enables domain-specific language
    'direction': 'What we are trying to achieve',
    'tensions': [
        {'id': 'TENSION_ID', 'claim': 'The thesis but the counter-thesis'},
        # ... 5-15 tensions
    ]
})

# The 4 lenses
checks = sp.cross_check()        # per-tension structural verdict
strat = sp.strategy()             # focus, leverage, risks, blind spots
plan = sp.action_plan()           # prioritized actions with domain language
result = sp.explore(verbose=True) # full trajectory + passages + field
```

### From the command line

```bash
# Cross-check the field
python scenario_projector.py --seed path/to/seed.json --cross-check

# Strategy insights
python scenario_projector.py --seed path/to/seed.json --strategy

# Action plan
python scenario_projector.py --seed path/to/seed.json --action-plan

# Full exploration
python scenario_projector.py --seed path/to/seed.json --explore
```

### Pre-configured domains

Seeds in `d-nd-seed/plugins/d-nd-core/scripts/examples/`:
- `startup_strategy.json` — Series A founder decisions
- `product_roadmap.json` — Feature prioritization
- `due_diligence.json` — Investment thesis cross-check
- `risk_assessment.json` — Digital transformation risks
- `portfolio_management.json` — Multi-asset rebalancing

### Automated integration

See `automation_pattern.py` in examples/ for the full pattern:
```
DATA SOURCE → TensionGenerator → ScenarioProjector → ActionConsumer → EXECUTION
```
The projector is the cognitive middleware: domain-agnostic structural analysis
between domain-specific input (tension generation) and output (action execution).

## Relationship with other tools

| Tool | Role | When |
|------|------|------|
| **CEC** | How to think about each tension | During — deepens individual analysis |
| **Domandatore** | Generates tensions from a question | Before the projector — creates the input |
| **Godel** | Inverts a specific claim (det=-1) | On contested tensions — flip the assumption |
| **Projector** | Maps the field of all tensions | After — sees the structural whole |

Natural flow: Domandatore → Projector → CEC on focus areas → Godel on contradictions.

## Writing good tensions

- Include **both poles** with "but", "however", "while", "yet", or "—"
- Use **concrete numbers** when available
- Keep IDs **semantic** — PRICING_MODEL not T1
- 8-15 tensions is the sweet spot

## Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| confirmed | Structural pillar with high support | Amplify — investment propagates |
| supported | Backed by neighbors, not a pillar | Monitor — it's healthy |
| contested | Anti-claim matches a neighbor's claim | Investigate — there's a crack |
| weak | Few connections, not isolated | Strengthen or deprioritize |
| unverifiable | Isolated — no neighbors to verify | Explore — could be hidden potential |

## Eval

## Trigger Tests
# "analyze this strategy structurally" -> activates
# "I have 8 competing priorities, which ones matter?" -> activates
# "cross-check this thesis" -> activates
# "map the risks in this plan" -> activates
# "what's the git status" -> does NOT activate
# "fix this bug" -> does NOT activate

## Fidelity Tests
# Given 5+ tensions: produces dipole field, trajectory, structural verdicts
# Given a domain seed: uses domain-specific labels in action plan
# Given a single tension: cross-checks it against the field
# Given a mechanical task: does NOT activate, suggests direct execution
