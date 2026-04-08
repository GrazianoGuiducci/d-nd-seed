#!/usr/bin/env python3
"""
automation_pattern.py — Pattern for automated projector integration

Shows how to connect the Scenario Projector to automated systems:
  DATA SOURCE → TENSION GENERATOR → PROJECTOR → ACTION CONSUMER

The projector is the cognitive middleware: it doesn't know about markets,
portfolios, or any specific domain. It knows about structure.

The domain-specific parts are:
  1. TensionGenerator — reads data, produces tensions
  2. ActionConsumer — reads projector output, executes

Example: portfolio rebalancing based on structural analysis.

No external dependencies beyond the projector itself.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add projector to path
sys.path.insert(0, str(Path(__file__).parent.parent))
# or just: sys.path.insert(0, '/opt/d-nd-seed/plugins/d-nd-core/scripts')
from scenario_projector import ScenarioProjector


# ═══════════════════════════════════════════════════════════════════
# TENSION GENERATOR — domain-specific, reads data, produces tensions
# ═══════════════════════════════════════════════════════════════════

class PortfolioTensionGenerator:
    """
    Reads portfolio data and market conditions,
    generates structural tensions for the projector.

    In production: connect to Bloomberg/Reuters/internal API.
    Here: simulated data for demonstration.
    """

    def __init__(self, portfolio_data=None):
        self.portfolio = portfolio_data or self._sample_portfolio()

    def _sample_portfolio(self):
        """Sample portfolio for demonstration."""
        return {
            'positions': [
                {'asset': 'US_EQUITY', 'weight': 0.45, 'return_1y': 0.22, 'vol': 0.16},
                {'asset': 'INTL_EQUITY', 'weight': 0.15, 'return_1y': 0.08, 'vol': 0.18},
                {'asset': 'FIXED_INCOME', 'weight': 0.25, 'return_1y': -0.02, 'vol': 0.08},
                {'asset': 'ALTERNATIVES', 'weight': 0.10, 'return_1y': 0.11, 'vol': 0.05},
                {'asset': 'CASH', 'weight': 0.05, 'return_1y': 0.05, 'vol': 0.001},
            ],
            'constraints': {
                'max_single_asset': 0.50,
                'min_fixed_income': 0.20,
                'max_drawdown_target': 0.15,
                'tracking_error_budget': 0.02,
            },
            'market': {
                'rate_direction': 'rising',
                'vix': 14,
                'eq_bond_correlation': 0.35,  # positive = bad for diversification
                'credit_spread': 1.2,  # tight
            }
        }

    def generate(self):
        """Generate tensions from portfolio state."""
        p = self.portfolio
        pos = {x['asset']: x for x in p['positions']}
        market = p['market']
        constraints = p['constraints']

        tensions = []

        # Concentration
        for asset_data in p['positions']:
            asset = asset_data['asset']
            w = asset_data['weight']
            if w > constraints['max_single_asset'] * 0.7:
                tensions.append({
                    'id': f'CONCENTRATION_{asset}',
                    'claim': (f"{asset} at {w:.0%} is near the {constraints['max_single_asset']:.0%} limit "
                              f"— strong recent returns ({asset_data['return_1y']:.0%}) "
                              f"but reversion risk increases with concentration"),
                })

        # Correlation regime
        if market['eq_bond_correlation'] > 0.2:
            tensions.append({
                'id': 'CORRELATION_REGIME',
                'claim': (f"Equity-bond correlation at {market['eq_bond_correlation']:.2f} "
                          f"— diversification benefit eroded but rebalancing the mix "
                          f"would crystallize losses in fixed income"),
            })

        # Rate exposure
        if market['rate_direction'] == 'rising':
            fi = pos.get('FIXED_INCOME', {})
            tensions.append({
                'id': 'RATE_SENSITIVITY',
                'claim': (f"Fixed income at {fi.get('weight', 0):.0%} in a rising rate environment "
                          f"— reducing duration helps but minimum allocation is "
                          f"{constraints['min_fixed_income']:.0%} per mandate"),
            })

        # Volatility regime
        if market['vix'] < 16:
            tensions.append({
                'id': 'VOL_COMPLACENCY',
                'claim': (f"VIX at {market['vix']} signals complacency — hedging is cheap now "
                          f"but the cost drags returns in continued calm markets"),
            })

        # Credit spread
        if market['credit_spread'] < 1.5:
            tensions.append({
                'id': 'SPREAD_COMPRESSION',
                'claim': (f"Credit spreads at {market['credit_spread']}% are historically tight "
                          f"— yield is low relative to risk but widening would cause "
                          f"mark-to-market losses in alternatives book"),
            })

        # Cash drag
        cash = pos.get('CASH', {})
        if cash.get('weight', 0) > 0.03:
            eq_return = pos.get('US_EQUITY', {}).get('return_1y', 0.1)
            cash_return = cash.get('return_1y', 0.04)
            gap = eq_return - cash_return
            tensions.append({
                'id': 'CASH_OPPORTUNITY_COST',
                'claim': (f"Cash at {cash.get('weight', 0):.0%} earns {cash_return:.0%} while equities "
                          f"returned {eq_return:.0%} — {gap:.0%} opportunity cost "
                          f"but liquidity buffer protects against forced selling"),
            })

        # Drawdown budget
        tensions.append({
            'id': 'DRAWDOWN_BUDGET',
            'claim': (f"Maximum drawdown target is {constraints['max_drawdown_target']:.0%} "
                      f"but current portfolio vol implies possible drawdown of "
                      f"{constraints['max_drawdown_target'] * 1.5:.0%} in a 2-sigma event"),
        })

        return {
            'name': 'Portfolio Structural Analysis',
            'context': 'portfolio_management',
            'direction': 'Optimize allocation within constraints given current market regime',
            'tensions': tensions,
            'generated_at': datetime.now().isoformat(),
        }


# ═══════════════════════════════════════════════════════════════════
# ACTION CONSUMER — reads projector output, produces actionable signals
# ═══════════════════════════════════════════════════════════════════

class PortfolioActionConsumer:
    """
    Reads projector output and produces portfolio signals.

    In production: connect to OMS (Order Management System).
    Here: produces human-readable recommendations.
    """

    def consume(self, action_plan, strategy):
        """Convert projector output to portfolio signals."""
        signals = []

        for action in action_plan['actions']:
            signal = {
                'type': action['type'],
                'priority': action['priority'],
                'action': self._translate(action),
                'tensions': action.get('ids', []),
                'risk_note': action.get('risk', ''),
            }
            signals.append(signal)

        # Add field summary
        field = action_plan.get('field', {})
        summary = action_plan.get('summary', {})

        return {
            'timestamp': datetime.now().isoformat(),
            'signals': signals,
            'field_health': {
                'total_tensions': field.get('dipoles', 0),
                'connected': field.get('assonances', 0),
                'confirmed_anchors': summary.get('leverage_points', 0),
                'structural_risks': summary.get('risks', 0),
                'blind_spots': summary.get('blind_spots', 0),
            },
            'recommendation': self._overall_recommendation(signals, summary),
        }

    def _translate(self, action):
        """Translate structural action to portfolio language."""
        atype = action['type']
        if atype == 'focus':
            return f"MONITOR: {len(action.get('ids', []))} correlated positions — stress test as a group"
        elif atype == 'risk':
            return f"REVIEW: structural fragility detected — evaluate hedge or reduce"
        elif atype == 'blind_spot':
            return f"INVESTIGATE: disconnected from risk framework — add monitoring"
        elif atype == 'leverage':
            return f"HOLD/INCREASE: portfolio anchor — this allocation stabilizes the rest"
        return f"INFO: {action.get('what', '')}"

    def _overall_recommendation(self, signals, summary):
        """Generate overall portfolio recommendation."""
        risks = summary.get('risks', 0)
        anchors = summary.get('leverage_points', 0)
        blind_spots = summary.get('blind_spots', 0)

        if risks > anchors:
            return 'DEFENSIVE — more structural risks than anchors. Reduce exposure or add hedges.'
        elif blind_spots > 2:
            return 'CAUTIOUS — multiple unmonitored exposures. Add monitoring before acting.'
        elif anchors >= 2 and risks <= 1:
            return 'CONSTRUCTIVE — strong anchors, limited fragility. Maintain or selectively add.'
        return 'NEUTRAL — balanced structure. Continue monitoring.'


# ═══════════════════════════════════════════════════════════════════
# MAIN — the full cycle
# ═══════════════════════════════════════════════════════════════════

def run_cycle(portfolio_data=None, verbose=True):
    """
    Full automated cycle:
    1. Generate tensions from portfolio data
    2. Project scenarios
    3. Produce actionable signals
    """
    # 1. Generate
    generator = PortfolioTensionGenerator(portfolio_data)
    seed = generator.generate()

    if verbose:
        print(f"Generated {len(seed['tensions'])} tensions from portfolio data")
        for t in seed['tensions']:
            print(f"  {t['id']}")

    # 2. Project
    sp = ScenarioProjector(seed_data=seed)
    strategy = sp.strategy()
    plan = sp.action_plan()

    if verbose:
        print(f"\nProjection complete:")
        print(f"  Focus clusters: {len(strategy['focus'])}")
        print(f"  Leverage points: {len(strategy['leverage'])}")
        print(f"  Risks: {len([r for r in strategy['risks'] if r['contradictions']])}")
        print(f"  Blind spots: {len(strategy['blind_spots'])}")

    # 3. Consume
    consumer = PortfolioActionConsumer()
    result = consumer.consume(plan, strategy)

    if verbose:
        print(f"\n--- PORTFOLIO SIGNALS ---")
        for s in result['signals']:
            sym = {'focus': '▶', 'risk': '✗', 'blind_spot': '?', 'leverage': '✓'}.get(s['type'], '·')
            print(f"  {sym} [{s['priority']}] {s['action']}")
            if s['risk_note']:
                print(f"       {s['risk_note'][:100]}")
        print(f"\n  Overall: {result['recommendation']}")

    return result


if __name__ == '__main__':
    result = run_cycle()
    if '--json' in sys.argv:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
