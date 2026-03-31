#!/usr/bin/env python3
"""
cognitive_cycle.py — Self-Learning Autonomous Cycle

A cycle that learns from itself. Each run:
1. READS memory from the previous cycle
2. ADAPTS — skips ineffective tools, follows the direction
3. EXECUTES — runs the configured phases
4. REFLECTS — detects stalls between phases
5. LEARNS — writes what worked, what didn't, the question for next time
6. PERSISTS — memory survives for the next cycle

Unlike seed_cycle.py (which decides ONE action), this runs a full cycle
of phases and learns from the aggregate result.

Configuration:
    Set PROJECT_DIR, DATA_DIR, and register phases via add_phase().

Usage:
    python cognitive_cycle.py              # run cycle
    python cognitive_cycle.py --status     # show memory state
    python cognitive_cycle.py --reset      # reset memory
"""

import json
import sys
from pathlib import Path
from datetime import datetime


# === CONFIGURATION ===

PROJECT_DIR = Path(".")
DATA_DIR = Path("./data")


class CognitiveMemory:
    """
    The cycle's memory. Persists between runs.
    Each cycle reads it, adapts, then updates it.
    """

    def __init__(self, path):
        self.path = Path(path)
        self.data = {
            'version': 1,
            'last_cycle': None,
            'learnings': [],
            'current_direction': '',
            'effective_tools': [],
            'ineffective_tools': [],
            'open_question': '',
        }
        self.load()

    def load(self):
        if self.path.exists():
            try:
                with open(self.path) as f:
                    self.data = json.load(f)
            except Exception:
                pass

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False, default=str)

    def add_learning(self, learning):
        self.data['learnings'].append(learning)
        self.data['learnings'] = self.data['learnings'][-10:]
        self.data['last_cycle'] = datetime.now().isoformat()

    def should_skip(self, phase_name):
        """Check if this phase was ineffective last time."""
        return phase_name.lower() in [t.lower() for t in self.data.get('ineffective_tools', [])]

    @property
    def direction(self):
        return self.data.get('current_direction', '')

    @property
    def open_question(self):
        return self.data.get('open_question', '')


class CognitiveCycle:
    """
    The self-learning cycle.

    Register phases with add_phase(). Each phase is:
    - name: identifier
    - fn: callable() -> dict with at least {'produced': bool, 'summary': str}
    - optional: if True, can be skipped by adaptation
    """

    def __init__(self, memory_path=None):
        self.phases = []
        self.results = []
        self.memory = CognitiveMemory(memory_path or DATA_DIR / 'cognitive_memory.json')

    def add_phase(self, name, fn, optional=False):
        self.phases.append({'name': name, 'fn': fn, 'optional': optional})

    def reflect(self):
        """Check if we're in a stall — last 3 phases produced nothing."""
        if len(self.results) < 3:
            return 'ok'
        last3 = self.results[-3:]
        empty = sum(1 for r in last3 if not r.get('produced', False))
        if empty >= 2:
            return 'stall'
        return 'ok'

    def run(self):
        """Run the full cycle with memory, adaptation, reflection, learning."""
        ts = datetime.now()
        print(f"\n{'='*60}")
        print(f"COGNITIVE CYCLE — {ts.strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")

        # 1. Load memory
        if self.memory.direction:
            print(f"\n  Direction: {self.memory.direction[:80]}")
        if self.memory.open_question:
            print(f"  Open question: {self.memory.open_question[:80]}")

        recent = self.memory.data.get('learnings', [])[-1:]
        if recent:
            print(f"  Last learning: {recent[0].get('what', '?')[:60]}")

        # 2. Run phases
        for phase in self.phases:
            name = phase['name']

            # Adaptation: skip ineffective optional phases
            if phase['optional'] and self.memory.should_skip(name):
                print(f"\n  [{name}] SKIP (ineffective last cycle)")
                self.results.append({
                    'phase': name, 'produced': False, 'summary': 'skipped (adaptation)'
                })
                continue

            print(f"\n  [{name}]")
            try:
                result = phase['fn']()
                if not isinstance(result, dict):
                    result = {'produced': True, 'summary': str(result)[:100]}
                result['phase'] = name
                self.results.append(result)

                produced = result.get('produced', False)
                summary = result.get('summary', '')[:60]
                tag = '✓' if produced else '·'
                print(f"  [{name}] {tag} {summary}")

            except Exception as e:
                print(f"  [{name}] ERROR: {e}")
                self.results.append({
                    'phase': name, 'produced': False, 'summary': f'error: {e}'
                })

            # Reflection between phases
            state = self.reflect()
            if state == 'stall':
                print(f"\n  [REFLECT] Stall detected — consider changing direction")

        # 3. Learn
        duration = (datetime.now() - ts).total_seconds() / 60
        produced_phases = [r for r in self.results if r.get('produced')]
        empty_phases = [r for r in self.results if not r.get('produced')]

        learning = {
            'timestamp': datetime.now().isoformat(),
            'duration_min': round(duration, 1),
            'phases_total': len(self.results),
            'phases_produced': len(produced_phases),
            'phases_empty': len(empty_phases),
            'what': '; '.join(r.get('summary', '')[:40] for r in produced_phases[:3]) or 'nothing new',
            'effective': [r['phase'] for r in produced_phases],
            'ineffective': [r['phase'] for r in empty_phases],
        }

        self.memory.add_learning(learning)
        self.memory.data['effective_tools'] = learning['effective']
        self.memory.data['ineffective_tools'] = learning['ineffective']

        # 4. Summary
        print(f"\n{'='*60}")
        print(f"RESULT: {len(produced_phases)}/{len(self.results)} phases produced | {duration:.1f}min")
        if learning['what'] != 'nothing new':
            print(f"  Learned: {learning['what'][:80]}")

        n_empty = len(empty_phases)
        n_total = len(self.results)
        if n_empty > n_total * 0.5:
            print(f"  WARNING: {n_empty}/{n_total} phases empty — cycle is spinning")

        # 5. Save memory
        self.memory.save()
        print(f"  Memory saved ({len(self.memory.data['learnings'])} learnings)")

        return learning

    def status(self):
        """Show memory state."""
        print(f"\n{'='*60}")
        print(f"COGNITIVE MEMORY STATUS")
        print(f"{'='*60}")
        print(f"\n  Last cycle: {self.memory.data.get('last_cycle', 'never')}")
        print(f"  Direction: {self.memory.direction[:80] or 'none'}")
        print(f"  Open question: {self.memory.open_question[:80] or 'none'}")
        print(f"  Effective: {self.memory.data.get('effective_tools', [])}")
        print(f"  Ineffective: {self.memory.data.get('ineffective_tools', [])}")
        print(f"  Learnings: {len(self.memory.data.get('learnings', []))}")
        for l in self.memory.data.get('learnings', [])[-3:]:
            print(f"    [{l.get('timestamp', '?')[:10]}] {l.get('what', '?')[:60]}")


# === CLI ===

if __name__ == '__main__':
    cycle = CognitiveCycle(DATA_DIR / 'cognitive_memory.json')

    if '--status' in sys.argv:
        cycle.status()
    elif '--reset' in sys.argv:
        cycle.memory.data = {
            'version': 1, 'last_cycle': None, 'learnings': [],
            'current_direction': '', 'effective_tools': [],
            'ineffective_tools': [], 'open_question': '',
        }
        cycle.memory.save()
        print("Memory reset.")
    else:
        # Example: register some phases
        def example_phase():
            return {'produced': True, 'summary': 'example ran'}

        cycle.add_phase('example', example_phase)
        cycle.run()
