#!/usr/bin/env python3
"""
theory_crossing.py — Cross N theories, find what lives between them

Takes any set of theories (each with constants and dipoles).
For each pair: finds the relational constant, the zero dipole, the bridge.
Where there's no bridge: a void (highest potential).

The mechanic:
- 2 theories -> 1 relational constant, 1 zero dipole, 1 bridge
- 3 theories -> 3 pairs, 3 bridges, 1 triangulation
- N theories -> C(N,2) pairs, C(N,3) triangulations

Usage:
    python theory_crossing.py theories.json
    python theory_crossing.py --questions
"""

import json
import sys
from itertools import combinations
from pathlib import Path
from datetime import datetime

DATA = Path(__file__).parent / 'data'


def load_theories(path):
    """Load theories from JSON. Format: {theories: [...], bridges: {...}}"""
    with open(path) as f:
        data = json.load(f)
    return data.get('theories', []), data.get('bridges', {})


def build_crossings(theories, bridges):
    """Generate all crossings between theory pairs."""
    crossings = []
    for t1, t2 in combinations(theories, 2):
        key = f"{t1['key']}x{t2['key']}"
        rev = f"{t2['key']}x{t1['key']}"
        info = bridges.get(key) or bridges.get(rev) or {}
        crossings.append({
            't1': t1['key'], 't2': t2['key'],
            'bridge': info.get('bridge'),
            'zero_dipole': info.get('zero_dipole'),
            'relational_constant': info.get('relational_constant'),
            'void': info.get('bridge') is None,
        })
    return crossings


def fundamental_questions(crossings):
    """Extract questions from zero dipoles."""
    questions = []
    for c in crossings:
        zd = c.get('zero_dipole', '')
        if not zd:
            continue
        parts = zd.split('/')
        d = parts[0].strip() if parts else '?'
        nd = parts[1].strip() if len(parts) > 1 else '?'
        questions.append({
            'pair': f"{c['t1']}x{c['t2']}",
            'question': f"How do {d} and {nd} coexist?",
            'answer': c.get('bridge'),
            'void': c['void'],
        })
    return questions


def cross_bridges(crossings):
    """Second level: cross the bridges. Two bridges sharing a theory are related."""
    bridges = [c for c in crossings if not c['void']]
    relations = []
    for b1, b2 in combinations(bridges, 2):
        t1 = {b1['t1'], b1['t2']}
        t2 = {b2['t1'], b2['t2']}
        shared = t1 & t2
        if shared:
            relations.append({
                'bridge1': f"{b1['t1']}x{b1['t2']}: {b1['bridge']}",
                'bridge2': f"{b2['t1']}x{b2['t2']}: {b2['bridge']}",
                'pivot': sorted(shared),
                'united': sorted(t1 | t2),
            })
    return relations


def run(theories_path):
    """Full crossing cycle."""
    theories, bridges = load_theories(theories_path)
    print(f"\n{'='*60}")
    print(f"THEORY CROSSING — {len(theories)} theories")
    print(f"{'='*60}")

    crossings = build_crossings(theories, bridges)
    n_void = sum(1 for c in crossings if c['void'])
    print(f"\n  {len(crossings)} pairs ({len(crossings)-n_void} bridges, {n_void} voids)")

    for c in crossings:
        mark = '***' if c['void'] else '   '
        b = c['bridge'] or '[VOID]'
        print(f"    {mark}{c['t1']}x{c['t2']}: {b}")

    questions = fundamental_questions(crossings)
    relations = cross_bridges(crossings)

    if relations:
        pivots = {}
        for r in relations:
            for p in r['pivot']:
                pivots[p] = pivots.get(p, 0) + 1
        print(f"\n  Bridge crossings: {len(relations)} | Pivot frequency: {pivots}")

    # Save
    DATA.mkdir(parents=True, exist_ok=True)
    result = {
        'timestamp': datetime.now().isoformat(),
        'theories': len(theories),
        'crossings': len(crossings),
        'voids': n_void,
        'questions': questions,
        'bridge_relations': len(relations),
    }
    with open(DATA / 'crossing_result.json', 'w') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return result


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
        run(sys.argv[1])
    elif '--questions' in sys.argv:
        qpath = DATA / 'crossing_result.json'
        if qpath.exists():
            with open(qpath) as f:
                for q in json.load(f).get('questions', []):
                    mark = '***' if q['void'] else '   '
                    print(f"  {mark}{q['pair']}: {q['question']} -> {q.get('answer') or '[VOID]'}")
    else:
        print("Usage: python theory_crossing.py theories.json")
        print("\nFormat:")
        print(json.dumps({
            'theories': [
                {'key': 'A', 'name': 'Theory A', 'constant_name': 'alpha', 'constant_symbol': 'a'},
                {'key': 'B', 'name': 'Theory B', 'constant_name': 'beta', 'constant_symbol': 'b'},
            ],
            'bridges': {
                'AxB': {'bridge': 'The AB object', 'zero_dipole': 'left/right', 'relational_constant': 'a/b'},
            }
        }, indent=2))
