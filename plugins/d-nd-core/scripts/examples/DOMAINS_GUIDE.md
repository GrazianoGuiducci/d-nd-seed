# Scenario Projector — Domain Pre-configurations

The scenario projector works on any domain with competing tensions.
These pre-configured seeds show high-value use cases ready to use.

## Available Domains

| Domain | Seed file | Tensions | Best for |
|--------|-----------|----------|----------|
| **Startup Strategy** | `startup_strategy.json` | 12 | Founders deciding where to focus — hiring, pricing, moat, burn |
| **Product Roadmap** | `product_roadmap.json` | 13 | PMs prioritizing features with limited squads |
| **Due Diligence** | `due_diligence.json` | 14 | Investors cross-checking an investment thesis |
| **Risk Assessment** | `risk_assessment.json` | 12 | Teams managing digital transformation risks |

## How to use

```bash
# Run on a pre-configured domain
python scenario_projector.py --seed examples/startup_strategy.json --action-plan

# Cross-check a specific tension
python scenario_projector.py --seed examples/due_diligence.json --cross-check --tension REVENUE_QUALITY

# Strategy overview
python scenario_projector.py --seed examples/product_roadmap.json --strategy

# Full exploration with trajectory
python scenario_projector.py --seed examples/risk_assessment.json --explore
```

## How to adapt

Each seed is a starting point. To adapt for your specific situation:

1. **Edit the tensions** — replace claims with your actual decisions/tensions
2. **Keep the `context` field** — it controls domain-specific output language
3. **Use `"gate": "confirmed"` or `"gate": "falsified"`** for resolved tensions — they become "saturated" and free up potential for others
4. **IDs are semantic** — `PRICING_MODEL` carries meaning, `T1` does not

## What each mode reveals

### `--cross-check`
For each tension: is it a **pillar** (structural foundation), **supported** (backed by neighbors), **contested** (anti-claim matches neighbor claims), **weak** (few connections), or **unverifiable** (isolated)?

### `--strategy`
- **Focus**: where tensions cluster — natural convergence points
- **Leverage**: confirmed pillars — invest here, it propagates
- **Risks**: anti-claims of the most connected tensions
- **Blind spots**: isolated tensions that could hide something
- **Completed**: saturated — done, free to move on

### `--action-plan`
Prioritized actions with domain-specific framing. Each action has:
- **What**: domain-appropriate label (e.g., "Thesis contradiction" for due diligence)
- **Detail**: which tensions are involved
- **Risk**: the anti-claim — the thing that could go wrong
- **Tensions**: IDs for tracking

## Domain-specific labels

| Type | Startup | Product | Due Diligence | Risk Assessment |
|------|---------|---------|---------------|-----------------|
| Focus | Strategic convergence | Feature cluster | Correlated metrics | Risk cascade |
| Risk | Growth risk | Roadmap conflict | Thesis contradiction | Counter-risk |
| Blind spot | Under-explored | Orphan feature | DD gap | Unmonitored risk |
| Leverage | Foundation | Platform foundation | Thesis anchor | Mitigation pillar |

## Adding new domains

Create a JSON seed with:
```json
{
  "name": "Your Domain Name",
  "context": "your_domain_key",
  "direction": "What you're trying to achieve",
  "tensions": [
    {
      "id": "TENSION_ID",
      "claim": "The tension — ideally with 'but' to make the dipole explicit"
    }
  ]
}
```

To add domain-specific labels, add an entry to `_DOMAIN_LABELS` in `scenario_projector.py`.

Tips for good tension claims:
- Include **both poles** with "but", "however", "while", "yet", or "—"
- Use **concrete numbers** when available (they become part of the risk)
- Keep IDs **semantic** — they contribute to concept extraction
- 10-15 tensions is the sweet spot — fewer gives sparse results, more gets noisy
