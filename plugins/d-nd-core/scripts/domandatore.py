#!/usr/bin/env python3
"""
domandatore.py — Autopoietic Research Engine (Neutral Seed)

A self-feeding experiment generator that takes a research tension
(open question) and produces falsifiable experiments using 5
question operators derived from duality logic:

  1. DUAL    — if X is true, what does 1/X say?
  2. BOUNDARY — if A and B are opposites, what's at the border?
  3. DOMAIN  — if it holds here, does it hold there?
  4. BREAK   — what would break this claim?
  5. SCALE   — does it hold at large N as at small N?

Cycle: tension -> operator -> experiment -> execution -> evaluation -> new tension

This is the public, domain-neutral version. To use it for your research:
1. Define your PRELUDE (shared computation code)
2. Define your VOCABULARY (measurable quantities with targets)
3. Define your BANKS (experiment templates per domain)
4. Run: python domandatore.py --seed your_seed.json

The engine handles: generation, execution, evaluation, de-duplication,
auto-expansion (successful experiments become reusable banks), and
vocabulary self-extension (new quantities discovered during cycles).

Author: D-ND Project (d-nd.com)
License: MIT
"""

import numpy as np
import json
import sys
import os
import re
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timedelta


# ============================================================
# CONFIGURATION — Override these for your domain
# ============================================================

# Shared code injected into every experiment
PRELUDE = '''
import numpy as np
import json
# Add your domain-specific imports and helpers here
'''

# Measurable quantities: name -> {desc, codice, target}
VOCABULARY = {
    # Example:
    # 'my_metric': {
    #     'desc': 'description of what this measures',
    #     'codice': 'code to compute it (uses `seq` and `N`)',
    #     'target': '1.0',
    # },
}

# Experiment bodies: name -> (code_string, target_string)
BODIES = {
    # Example:
    # 'my_metric': ('value = compute_something(data)', '1.0'),
}

# Experiment banks: name -> (function, keywords)
CATALOG = {
    # Example:
    # 'my_bank': (my_bank_function, ['keyword1', 'keyword2']),
}


# ============================================================
# CORE ENGINE — Domain-independent
# ============================================================

class Domandatore:
    """The autopoietic research engine."""

    def __init__(self, seed_path, results_dir=None, prelude=None,
                 vocabulary=None, bodies=None, catalog=None):
        self.seed_path = Path(seed_path)
        self.results_dir = Path(results_dir) if results_dir else self.seed_path.parent / 'domandatore'
        self.results_dir.mkdir(parents=True, exist_ok=True)

        self.prelude = prelude or PRELUDE
        self.vocabulary = vocabulary or VOCABULARY
        self.bodies = bodies or BODIES
        self.catalog = catalog or CATALOG

        # Custom banks and vocabulary discovered during cycles
        self.custom_banks_dir = self.results_dir / 'banks_custom'
        self.custom_vocab_path = self.results_dir / 'vocabulary_custom.json'

    def load_seed(self):
        """Load seed with open tensions."""
        if not self.seed_path.exists():
            return None
        with open(self.seed_path) as f:
            return json.load(f)

    def get_open_tensions(self, seed=None):
        """Extract open tensions from seed."""
        if seed is None:
            seed = self.load_seed()
        if seed is None:
            return []
        return [t for t in seed.get('tensions', seed.get('tensioni', []))
                if t.get('type', t.get('tipo', '')) in
                ('open_tension', 'tensione_aperta', 'unexplored_boundary', 'confine_inesplorato')]

    def recent_experiment_ids(self, hours=24):
        """IDs of experiments run in the last N hours (for de-duplication)."""
        ids = set()
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        for f in self.results_dir.glob('report_*.json'):
            try:
                with open(f) as fh:
                    report = json.load(fh)
                if report.get('timestamp', '') < cutoff:
                    continue
                for r in report.get('results', []):
                    ids.add(r.get('id', ''))
            except Exception:
                continue
        return ids

    # --- Operators ---

    def _bank_or_generate(self, claim, tid):
        """Use catalog if available, otherwise generate from scratch."""
        banks = self._select_banks(claim, tid, max_banks=1)
        if banks:
            bank = banks[0]
            bank['_source'] = 'catalog'
            return bank
        bank = self._generate_experiment(claim, tid)
        if bank:
            bank['_source'] = 'generated'
            return bank
        return None

    def operator_dual(self, tension):
        """If X is true, what does 1/X say?"""
        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        bank = self._bank_or_generate(claim, tid)
        if not bank:
            return []
        source = bank.pop('_source', '?')
        return [{
            'id': bank['id'],
            'operator': 'dual',
            'hypothesis': f'Dual of "{claim[:50]}" [{source}: {bank.get("domain", "?")}]',
            'code': bank['code'],
            'criterion': bank['criterion'],
        }]

    def operator_boundary(self, tension):
        """If A and B are opposites, what's at the border?"""
        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        # Always active — the boundary test is universal
        return [{
            'id': f'BOUNDARY_{tid}',
            'operator': 'boundary',
            'hypothesis': f'Between extremes of "{claim[:50]}" exists a continuous transition',
            'code': self.prelude + '\n# Boundary experiment placeholder\nprint("boundary test")',
            'criterion': 'Continuous transition exists (the third included)',
        }]

    def operator_domain(self, tension):
        """If it holds here, does it hold there?"""
        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        bank = self._bank_or_generate(f'cross-domain test: {claim}', tid)
        if not bank:
            return []
        return [{
            'id': f'DOMAIN_{bank["id"]}',
            'operator': 'domain',
            'hypothesis': f'Effect "{claim[:40]}" manifests also in {bank.get("domain", "?")}',
            'code': bank['code'],
            'criterion': bank['criterion'],
        }]

    def operator_break(self, tension):
        """What would break this claim?"""
        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        bank = self._bank_or_generate(f'scaling break test: {claim}', tid)
        if not bank:
            return []
        return [{
            'id': f'BREAK_{tid}',
            'operator': 'break',
            'hypothesis': f'Claim "{claim[:50]}" FAILS at small N or extreme parameters',
            'code': bank['code'],
            'criterion': bank['criterion'],
        }]

    def operator_scale(self, tension):
        """Does it hold at large N as at small N?"""
        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        bank = self._bank_or_generate(f'scaling convergence: {claim}', tid)
        if not bank:
            return []
        return [{
            'id': f'SCALE_{tid}',
            'operator': 'scale',
            'hypothesis': f'Effect "{claim[:50]}" scales as power law with N',
            'code': bank['code'],
            'criterion': bank['criterion'],
        }]

    OPERATORS = None  # Set in __init__ or use default

    def _get_operators(self):
        if self.OPERATORS:
            return self.OPERATORS
        return [
            self.operator_dual,
            self.operator_boundary,
            self.operator_domain,
            self.operator_break,
            self.operator_scale,
        ]

    # --- Bank selection and generation ---

    def _select_banks(self, claim, tid, max_banks=3):
        """Select most relevant banks from catalog + custom banks."""
        claim_lower = claim.lower()
        scores = []
        for name, (fn, keywords) in self.catalog.items():
            score = sum(1 for kw in keywords if kw in claim_lower)
            if score > 0:
                scores.append((score, name, fn))

        # Include custom banks
        if self.custom_banks_dir.exists():
            for f in self.custom_banks_dir.glob('bank_*.json'):
                try:
                    with open(f) as fh:
                        custom = json.load(fh)
                    kws = custom.get('keywords', [])
                    score = sum(1 for kw in kws if kw in claim_lower)
                    if score > 0:
                        def _make_fn(c):
                            def fn(tid):
                                return {
                                    'id': f'{c["id_prefix"]}_{tid}',
                                    'domain': c.get('domain', 'custom'),
                                    'code': self.prelude + c['code'],
                                    'criterion': c.get('criterion', '?'),
                                }
                            return fn
                        scores.append((score + 0.5, custom.get('name', f.stem), _make_fn(custom)))
                except Exception:
                    continue

        scores.sort(reverse=True)
        results = []
        for score, name, fn in scores[:max_banks]:
            bank = fn(tid)
            bank['bank_name'] = name
            bank['score'] = score
            results.append(bank)
        return results

    def _load_extended_vocabulary(self):
        """Load base vocabulary + custom extensions."""
        vocab = dict(self.vocabulary)
        if self.custom_vocab_path.exists():
            try:
                with open(self.custom_vocab_path) as f:
                    custom = json.load(f)
                for name, info in custom.items():
                    if name not in vocab:
                        vocab[name] = info
            except Exception:
                pass
        return vocab

    def _generate_experiment(self, claim, tid):
        """Generate experiment from scratch based on claim and vocabulary."""
        claim_lower = claim.lower()
        vocab = self._load_extended_vocabulary()

        found = []
        for name, info in vocab.items():
            if name.lower() in claim_lower or any(
                w in claim_lower for w in info.get('desc', '').lower().split()
                if len(w) > 3 and w not in ('the', 'for', 'not', 'that', 'with', 'from',
                                              'di', 'per', 'non', 'che', 'con')):
                found.append(name)

        if not found:
            return None

        quantity = found[0]
        if quantity in self.bodies:
            body, target = self.bodies[quantity]
        elif quantity in vocab and 'codice' in vocab[quantity]:
            body = vocab[quantity]['codice']
            target = vocab[quantity].get('target', vocab[quantity].get('target_phi', '0'))
        else:
            return None

        code = self.prelude + '\n' + body

        try:
            compile(code, f'gen_{tid}.py', 'exec')
        except SyntaxError:
            return None

        return {
            'id': f'GEN_{quantity.upper()}_{tid}',
            'domain': quantity,
            'code': code,
            'criterion': f'{quantity} matches target {target}',
            'generated': True,
        }

    # --- Execution ---

    def execute_experiment(self, exp):
        """Execute a single experiment and capture output."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(exp['code'])
            tmppath = f.name

        try:
            result = subprocess.run(
                [sys.executable, tmppath],
                capture_output=True, text=True, timeout=120,
            )
            return {
                'id': exp['id'],
                'operator': exp['operator'],
                'hypothesis': exp['hypothesis'],
                'criterion': exp['criterion'],
                'stdout': result.stdout[-2000:] if result.stdout else '',
                'stderr': result.stderr[-500:] if result.stderr else '',
                'returncode': result.returncode,
                'success': result.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {
                'id': exp['id'],
                'operator': exp['operator'],
                'hypothesis': exp['hypothesis'],
                'criterion': exp['criterion'],
                'stdout': '', 'stderr': 'TIMEOUT (120s)',
                'returncode': -1, 'success': False,
            }
        finally:
            os.unlink(tmppath)

    # --- Evaluation ---

    def evaluate_result(self, result):
        """
        Evaluate experiment result. Multi-level:
        0. Structured JSON output
        1. Named comparison (phi: X silver: Y)
        2. Transition detection (alpha → metric)
        3. Closer/farther pattern counting
        4. Keyword fallback
        """
        if not result['success']:
            return {
                'type': 'experiment_error',
                'id': f'ERR_{result["id"]}',
                'claim': f'Experiment {result["id"]} failed: {result["stderr"][:80]}',
                'intensity': 0.3,
            }

        output = result['stdout']

        # Level 0: structured JSON
        try:
            data = json.loads(output.strip())
            if isinstance(data, dict) and len(data) >= 2:
                # Look for systematic differences between entries
                values = {k: v for k, v in data.items() if isinstance(v, (int, float))}
                if len(values) >= 2:
                    keys = list(values.keys())
                    vals = list(values.values())
                    cv = np.std(vals) / np.mean(vals) if np.mean(vals) != 0 else 0
                    if cv > 0.3:
                        return {
                            'type': 'discovery',
                            'id': f'DISC_{result["id"]}',
                            'claim': f'Significant variation (CV={cv:.2f}): {dict(zip(keys[:3], [round(v,4) for v in vals[:3]]))}',
                            'intensity': min(0.9, 0.5 + cv),
                            'detail': output[-500:],
                        }
        except (json.JSONDecodeError, TypeError):
            pass

        # Level 1: named comparison
        named_vals = {}
        for m in re.finditer(r'(\w+):\s+(\w[\w_]*)\s*=\s*([+-]?\d+\.?\d*(?:[eE][+-]?\d+)?)', output):
            name, metric, val = m.group(1).lower(), m.group(2), float(m.group(3))
            named_vals.setdefault(name, {})[metric] = val
        if len(named_vals) >= 2:
            pass  # extend for your domain

        # Level 2: transition detection
        alpha_pairs = re.findall(r'alpha=([0-9.]+):\s*\S+=([0-9.]+)', output)
        if len(alpha_pairs) >= 5:
            vals = [float(p[1]) for p in alpha_pairs]
            r_range = max(vals) - min(vals)
            is_monotone = all(vals[i] <= vals[i+1] + 0.01 for i in range(len(vals)-1)) or \
                          all(vals[i] >= vals[i+1] - 0.01 for i in range(len(vals)-1))
            if is_monotone and r_range > 0.1:
                return {
                    'type': 'partial_confirmation',
                    'id': f'TRANS_{result["id"]}',
                    'claim': f'Continuous transition: {vals[0]:.3f} to {vals[-1]:.3f} (range={r_range:.3f})',
                    'intensity': 0.7,
                    'detail': output[-500:],
                }

        # Level 3: closer/farther
        closer = output.lower().count('closer')
        farther = output.lower().count('farther')
        total = closer + farther
        if total >= 3:
            ratio = closer / total
            if ratio > 0.7:
                return {
                    'type': 'partial_confirmation',
                    'id': f'CONF_{result["id"]}',
                    'claim': f'Convergence {closer}/{total} ({ratio:.0%}): {result["criterion"][:50]}',
                    'intensity': 0.6 + 0.2 * ratio,
                    'detail': output[-500:],
                }
            elif ratio < 0.3:
                return {
                    'type': 'open_tension',
                    'id': f'TENS_{result["id"]}',
                    'claim': f'Divergence {farther}/{total}: {result["criterion"][:50]}',
                    'intensity': 0.7,
                    'detail': output[-500:],
                }

        # Level 4: fit failure
        if 'fit failed' in output.lower() or 'optimal parameters not found' in output.lower():
            return {
                'type': 'open_tension',
                'id': f'TENS_{result["id"]}',
                'claim': f'Fit does not converge — model may not be power-law. {result["criterion"][:40]}',
                'intensity': 0.6,
                'detail': output[-500:],
            }

        # Neutral
        return {
            'type': 'neutral_result',
            'id': f'NEUT_{result["id"]}',
            'claim': f'Experiment {result["id"]} completed, requires interpretation',
            'intensity': 0.4,
            'detail': output[-500:],
        }

    # --- Auto-expansion ---

    def save_custom_bank(self, bank, keywords):
        """Save successful experiment as reusable bank."""
        self.custom_banks_dir.mkdir(parents=True, exist_ok=True)
        code = bank.get('code', '')
        if code.startswith(self.prelude):
            code = code[len(self.prelude):]
        entry = {
            'name': bank.get('bank_name', bank['id']),
            'id_prefix': bank['id'].rsplit('_', 1)[0] if '_' in bank['id'] else bank['id'],
            'domain': bank.get('domain', 'custom'),
            'code': code,
            'criterion': bank.get('criterion', '?'),
            'keywords': keywords,
            'created': datetime.now().isoformat(),
        }
        fname = f'bank_{bank["id"].lower()}.json'
        path = self.custom_banks_dir / fname
        with open(path, 'w') as f:
            json.dump(entry, f, indent=2, ensure_ascii=False)
        return path

    def save_vocabulary_entry(self, name, desc, body_code, target, keywords=None):
        """Save a new quantity to custom vocabulary."""
        custom = {}
        if self.custom_vocab_path.exists():
            try:
                with open(self.custom_vocab_path) as f:
                    custom = json.load(f)
            except Exception:
                pass
        custom[name] = {
            'desc': desc,
            'codice': body_code,
            'target': target,
            'keywords': keywords or [],
            'discovered': datetime.now().isoformat(),
        }
        with open(self.custom_vocab_path, 'w') as f:
            json.dump(custom, f, indent=2, ensure_ascii=False)
        return self.custom_vocab_path

    # --- Main cycle ---

    def cycle(self, tension=None, max_experiments=5):
        """
        Full cycle:
        1. Read tension from seed (or use provided)
        2. Generate experiments with 5 operators
        3. Execute the most relevant
        4. Evaluate results
        5. Produce new tensions
        6. Save report
        """
        ts = datetime.now()

        # 1. Tension
        if tension is None:
            seed = self.load_seed()
            if seed is None:
                print("  No seed found.")
                return None
            open_tensions = self.get_open_tensions(seed)
            if not open_tensions:
                print("  No open tensions in seed.")
                return None
            tension = max(open_tensions, key=lambda t: t.get('intensity', t.get('intensita', 0)))

        tid = tension.get('id', '?')
        claim = tension.get('claim', '')
        intensity = tension.get('intensity', tension.get('intensita', 0))

        print(f"\n  TENSION: [{intensity}] {tid}")
        print(f"  CLAIM: {claim}")

        # 2. Generate
        recent = self.recent_experiment_ids()
        experiments = []
        for op in self._get_operators():
            exps = op(tension)
            for exp in exps:
                if exp['id'] not in recent:
                    experiments.append(exp)

        print(f"\n  Experiments generated: {len(experiments)}")
        if not experiments:
            print("  All already run in last 24h.")
            return {'timestamp': ts.isoformat(), 'tension': tension,
                    'generated': 0, 'results': [], 'new_tensions': []}

        # 3. Execute
        results = []
        for exp in experiments[:max_experiments]:
            print(f"  >>> {exp['id']} ({exp['operator']})")
            result = self.execute_experiment(exp)
            results.append(result)
            status = "OK" if result['success'] else f"FAIL: {result['stderr'][:60]}"
            print(f"      {status}")

        # 4. Evaluate
        new_tensions = []
        for result in results:
            evaluation = self.evaluate_result(result)
            new_tensions.append(evaluation)
            print(f"  {result['id']} -> [{evaluation['type']}] {evaluation['claim'][:60]}")

        # 5. Save report
        report = {
            'timestamp': ts.isoformat(),
            'tension_input': {'id': tid, 'claim': claim, 'intensity': intensity},
            'generated': len(experiments),
            'executed': len(results),
            'results': [{
                'id': r['id'], 'operator': r['operator'],
                'hypothesis': r['hypothesis'], 'criterion': r['criterion'],
                'success': r['success'], 'stdout': r['stdout'][-1000:],
            } for r in results],
            'new_tensions': new_tensions,
        }
        report_path = self.results_dir / f"report_{ts.strftime('%Y%m%d_%H%M')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)

        n_ok = sum(1 for r in results if r['success'])
        print(f"\n  Summary: {len(experiments)} generated, {len(results)} executed, {n_ok} OK")
        print(f"  Report: {report_path}")

        return report

    def cycle_all(self, max_experiments_per_tension=5):
        """Run cycle on all open tensions."""
        seed = self.load_seed()
        if seed is None:
            print("No seed found.")
            return []
        reports = []
        for t in self.get_open_tensions(seed):
            report = self.cycle(t, max_experiments_per_tension)
            if report:
                reports.append(report)
        return reports


# ============================================================
# CLI
# ============================================================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Domandatore — Autopoietic Research Engine')
    parser.add_argument('--seed', type=str, required=True, help='Path to seed JSON file')
    parser.add_argument('--results', type=str, help='Path to results directory')
    parser.add_argument('--tension', type=str, help='Specific tension ID')
    parser.add_argument('--all', action='store_true', help='All open tensions')
    parser.add_argument('--dry', action='store_true', help='Generate only, no execution')
    args = parser.parse_args()

    engine = Domandatore(
        seed_path=args.seed,
        results_dir=args.results,
    )

    if args.all:
        engine.cycle_all()
    elif args.tension:
        seed = engine.load_seed()
        if seed:
            tensions = seed.get('tensions', seed.get('tensioni', []))
            t = next((t for t in tensions if t.get('id') == args.tension), None)
            if t:
                engine.cycle(t)
            else:
                print(f"Tension {args.tension} not found.")
    else:
        engine.cycle()
