#!/usr/bin/env python3
"""
projector_phase.py — Scenario Projector as a Cognitive Cycle phase

Registers the projector as an optional phase in the cognitive cycle.
Activates when there are 5+ tensions in the seed, applies the 4 structural
lenses (focus, leverage, risk, blind spots), and returns the field analysis.

Usage:
    # In your cycle configuration:
    from projector_phase import register_projector_phase
    register_projector_phase(cycle, seed_path='path/to/seed.json')

    # Or standalone:
    python projector_phase.py --seed path/to/seed.json

The phase is optional — the cognitive cycle will skip it if it was
ineffective in the previous cycle (adaptation).
"""

import json
import sys
from pathlib import Path

# Projector lives in the same directory
sys.path.insert(0, str(Path(__file__).parent))
from scenario_projector import ScenarioProjector


def make_projector_phase(seed_path=None, seed_data=None, min_tensions=5):
    """
    Create a projector phase function for the cognitive cycle.

    Args:
        seed_path: path to seed JSON (tensions, direction)
        seed_data: or direct seed dict
        min_tensions: minimum tensions to activate (default 5)

    Returns:
        callable that returns {'produced': bool, 'summary': str, ...}
    """

    def projector_phase():
        # Load seed
        data = seed_data
        if data is None and seed_path:
            p = Path(seed_path)
            if not p.exists():
                return {'produced': False, 'summary': f'seed not found: {seed_path}'}
            with open(p) as f:
                data = json.load(f)

        if data is None:
            return {'produced': False, 'summary': 'no seed data'}

        # Extract tensions
        tensions = data.get('tensions', data.get('tensioni', []))
        if len(tensions) < min_tensions:
            return {
                'produced': False,
                'summary': f'{len(tensions)} tensions (need {min_tensions}+)',
            }

        # Run projector
        sp = ScenarioProjector(seed_data=data)
        strat = sp.strategy()
        checks = sp.cross_check()

        # Extract key findings
        focus_count = len(strat['focus'])
        leverage_ids = [l['id'] for l in strat['leverage']]
        risk_ids = [r['id'] for r in strat['risks'] if r['contradictions']]
        blind_ids = [b['id'] for b in strat['blind_spots']]

        verdicts = [c['verdict'] for c in checks]
        confirmed = verdicts.count('confirmed')
        contested = verdicts.count('contested')

        # Build summary
        parts = []
        if leverage_ids:
            parts.append(f"pillars: {', '.join(leverage_ids[:3])}")
        if risk_ids:
            parts.append(f"risks: {', '.join(risk_ids[:3])}")
        if blind_ids:
            parts.append(f"blind: {', '.join(blind_ids[:2])}")
        summary = ' | '.join(parts) if parts else f'{confirmed} confirmed, {contested} contested'

        # Produce action plan
        plan = sp.action_plan()

        return {
            'produced': True,
            'summary': summary[:100],
            'strategy': strat,
            'checks': checks,
            'action_plan': plan,
            'field': {
                'tensions': len(tensions),
                'focus_clusters': focus_count,
                'leverage_points': len(leverage_ids),
                'risks': len(risk_ids),
                'blind_spots': len(blind_ids),
                'confirmed': confirmed,
                'contested': contested,
            },
        }

    return projector_phase


def register_projector_phase(cycle, seed_path=None, seed_data=None,
                              name='projector', min_tensions=5):
    """
    Register the projector as an optional phase in a CognitiveCycle.

    Args:
        cycle: CognitiveCycle instance
        seed_path: path to seed JSON
        seed_data: or direct seed dict
        name: phase name (default 'projector')
        min_tensions: minimum tensions to activate
    """
    phase_fn = make_projector_phase(
        seed_path=seed_path,
        seed_data=seed_data,
        min_tensions=min_tensions,
    )
    cycle.add_phase(name, phase_fn, optional=True)


# === CLI ===

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Projector as cognitive phase')
    parser.add_argument('--seed', type=str, help='Path to seed JSON')
    parser.add_argument('--json', action='store_true', help='JSON output')
    args = parser.parse_args()

    if not args.seed:
        # Try default seed locations
        candidates = [
            Path('./data/seme.json'),
            Path('./seme.json'),
        ]
        for c in candidates:
            if c.exists():
                args.seed = str(c)
                break

    phase_fn = make_projector_phase(seed_path=args.seed)
    result = phase_fn()

    if args.json:
        # Remove non-serializable parts for clean output
        output = {
            'produced': result['produced'],
            'summary': result['summary'],
        }
        if result['produced']:
            output['field'] = result.get('field', {})
            output['action_plan'] = result.get('action_plan', {})
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))
    else:
        produced = result.get('produced', False)
        tag = '✓' if produced else '·'
        print(f"[projector] {tag} {result.get('summary', '')}")

        if produced:
            field = result.get('field', {})
            print(f"\n  Field: {field.get('tensions', 0)} tensions")
            print(f"    Focus clusters: {field.get('focus_clusters', 0)}")
            print(f"    Leverage points: {field.get('leverage_points', 0)}")
            print(f"    Risks: {field.get('risks', 0)}")
            print(f"    Blind spots: {field.get('blind_spots', 0)}")
            print(f"    Verdicts: {field.get('confirmed', 0)} confirmed, "
                  f"{field.get('contested', 0)} contested")
