#!/usr/bin/env python3
"""
scenario_projector.py — Proiettore di scenari D-ND (universale)

Legge un seme (tensioni + direzione) e proietta scenari usando
la struttura proiettiva del modello D-ND: dipoli, assonanze, lagrangiana.

Non usa numeri per vincolare concetti. Le decisioni sono strutturali:
- Dipolo: D(claim, anti-claim) — ogni tensione ha due poli
- Assonanza: A(Di, Dj) in {0, 1} — risuonano o no
- Potenziale: alto/medio/basso/isolato/saturo — qualitativo
- Lagrangiana: il percorso naturale attraverso i dipoli a massimo potenziale

Usage:
    python scenario_projector.py                          # proiezione dal seme locale
    python scenario_projector.py --seed path/to/seme.json # seme specifico
    python scenario_projector.py --explore                # esplorazione autonoma
    python scenario_projector.py --json                   # output strutturato

As library:
    from scenario_projector import ScenarioProjector
    sp = ScenarioProjector(seed_path='path/to/seed.json')
    trajectory = sp.lagrangian_trajectory()
    passages = sp.explore()

No external dependencies (no numpy). Pure Python.

Author: TM3 + Operatore (D-ND system)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
# STOPWORDS per estrazione concetti (IT + EN)
# ═══════════════════════════════════════════════════════════════════

_STOPWORDS = {
    'della', 'delle', 'dello', 'degli', 'nella', 'nelle', 'nello',
    'come', 'cosa', 'sono', 'deve', 'essere', 'questo', 'questa',
    'quello', 'quella', 'molto', 'anche', 'altro', 'altra', 'altri',
    'altre', 'ogni', 'tutto', 'tutti', 'tutte', 'tutta', 'quale',
    'quali', 'hanno', 'fatto', 'prima', 'dopo', 'senza', 'ancora',
    'circa', 'sopra', 'sotto', 'verso', 'lungo',
    'the', 'that', 'this', 'with', 'from', 'have', 'been', 'which',
    'their', 'there', 'about', 'would', 'could', 'should', 'between',
}


class ScenarioProjector:
    """
    Proietta scenari da un seme usando la struttura proiettiva D-ND.

    Il principio: la struttura contiene già la risposta.
    Non interporre numeri tra la struttura e la decisione.
    """

    def __init__(self, seed_path=None, seed_data=None):
        """
        Args:
            seed_path: percorso al file seme JSON
            seed_data: dizionario seme (alternativa a seed_path)
        """
        if seed_data:
            self.seed = seed_data
        elif seed_path:
            self.seed = json.loads(Path(seed_path).read_text())
        else:
            # Cerca seme nella directory corrente o in data/
            for candidate in ['seed.json', 'seme.json', 'data/seed.json', 'data/seme.json']:
                p = Path(candidate)
                if p.exists():
                    self.seed = json.loads(p.read_text())
                    break
            else:
                self.seed = {'tensions': [], 'direction': ''}

        # Normalizza: supporta sia 'tensions' che 'tensioni'
        self.tensions = (self.seed.get('tensions') or
                         self.seed.get('tensioni', []))

    # ═══════════════════════════════════════════════════════════════
    # ESTRAZIONE CONCETTI
    # ═══════════════════════════════════════════════════════════════

    def _extract_concepts(self, text, include_id=''):
        """Estrai concetti strutturali (parole + radici)."""
        full_text = text
        if include_id:
            full_text = f'{include_id.lower().replace("_", " ")} {text}'

        words = set(w.lower() for w in re.findall(r'\b\w{4,}\b', full_text))
        words -= _STOPWORDS

        # Radici (troncamento suffissi comuni IT+EN)
        stems = set()
        for w in words:
            stem = re.sub(r'(zione|mente|ità|ness|tion|ment|able|ible|ando|endo)$', '', w)
            if len(stem) >= 4:
                stems.add(stem)

        return words | stems

    def _resonance_threshold(self):
        """Soglia adattiva: 1 per claim corti, 2 per claim lunghi."""
        if not self.tensions:
            return 2
        avg_len = sum(len(t.get('claim', '')) for t in self.tensions) / len(self.tensions)
        return 1 if avg_len < 150 else 2

    # ═══════════════════════════════════════════════════════════════
    # DIPOLI
    # ═══════════════════════════════════════════════════════════════

    def _invert_claim(self, claim):
        """
        L'anti-claim: il polo opposto del dipolo.

        3 livelli:
        1. Dipolo esplicito nel claim ("X vs Y") → i due poli
        2. Pattern strutturale (deve→non deve) → inversione
        3. Fallback strutturale
        """
        cl = claim.strip()

        # 1. Dipolo esplicito
        dipole_patterns = [
            r'[Tt]ensione?\s+tra\s+(.+?)\s+e\s+(.+?)[\.\,]',
            r'(.+?)\s+vs\.?\s+(.+)',
            r'(.+?)\s+ma\s+(.+?)[\.\,]',
            r'(.+?)\s+per[oò]\s+(.+?)[\.\,]',
            r'(.+?)\s+but\s+(.+?)[\.\,]',
            r'(.+?)\s+however\s+(.+?)[\.\,]',
        ]
        for pat in dipole_patterns:
            m = re.search(pat, cl)
            if m:
                return f'{m.group(2).strip()} (non {m.group(1).strip()[:50]})'

        # 2. Pattern strutturali universali
        inversions = [
            (r'\bdeve\b', lambda m: cl.replace('deve', 'non deve', 1)),
            (r'\bmust\b', lambda m: cl.replace('must', 'need not', 1)),
            (r'\brichiede\b', lambda m: cl.replace('richiede', 'non richiede', 1)),
            (r'\brequires?\b', lambda m: cl.replace(m.group(), f'does not {m.group()}', 1)),
            (r'\brischia\b', lambda m: f"Non c'è rischio — {cl[m.end():].strip()[:80]}"),
            (r'\bnon è\b', lambda m: cl.replace('non è', 'è', 1)),
            (r'\bis not\b', lambda m: cl.replace('is not', 'is', 1)),
            (r'\bnon\s+\w+\b', lambda m: cl.replace(m.group(), m.group().replace('non ', ''), 1)),
            (r"\bcan'?t\b", lambda m: cl.replace(m.group(), 'can', 1)),
            (r'\bunic[oa]\b', 'non unico — altri sistemi hanno la stessa proprietà'),
            (r'\bunique\b', 'not unique — other systems share this property'),
            (r'\bsolo\b', 'non solo — altri fattori contribuiscono'),
            (r'\bonly\b', 'not only — other factors contribute'),
            (r'\bsempre\b', 'non sempre — ci sono eccezioni strutturali'),
            (r'\balways\b', 'not always — structural exceptions exist'),
            (r'\bconverg', 'non converge — il pattern è locale, non globale'),
            (r'\bdiverg', 'non diverge — il sistema si stabilizza'),
            (r'\bcresc', 'decresce — il segnale si indebolisce'),
            (r'\bdecresc', 'cresce — il segnale si rafforza'),
            (r'\bincreas', 'decreases — the signal weakens'),
            (r'\bdecreas', 'increases — the signal strengthens'),
        ]

        for pattern, inversion in inversions:
            m = re.search(pattern, cl, re.IGNORECASE)
            if m:
                if callable(inversion):
                    return inversion(m)[:150]
                return inversion

        # 3. Fallback
        return f'Il contrario: {cl[:80]}... non è necessariamente vero'

    def _count_resonances(self, tid, claim):
        """Quante altre tensioni risuonano con questa?"""
        concepts = self._extract_concepts(claim, include_id=tid)
        threshold = self._resonance_threshold()
        count = 0
        for t in self.tensions:
            other_id = t.get('id', '')
            if other_id == tid:
                continue
            other = self._extract_concepts(t.get('claim', ''), include_id=other_id)
            if len(concepts & other) >= threshold:
                count += 1
        return count

    def _potentiality(self, tension):
        """
        Qualità strutturale del potenziale:
        - alto: dipolo interno o molte connessioni
        - medio: alcune connessioni
        - basso: poche connessioni
        - isolato: nessuna connessione
        - saturo: risolto
        """
        tid = tension.get('id', '')
        claim = tension.get('claim', '')
        connections = self._count_resonances(tid, claim)
        porta = tension.get('porta', tension.get('gate', ''))
        stato = tension.get('stato', tension.get('status', ''))

        if porta in ('confermata', 'falsificata', 'confirmed', 'falsified') or stato == 'saturo':
            return 'saturo'

        has_dipole = bool(re.search(
            r'(?:vs\.?|tensione?\s+tra|ma\s|per[oò]\s|but\s|however\s|non\s+\w+\s+ma)',
            claim, re.IGNORECASE))

        if has_dipole or connections >= 4:
            return 'alto'
        elif connections >= 2:
            return 'medio'
        elif connections >= 1:
            return 'basso'
        else:
            return 'isolato'

    # ═══════════════════════════════════════════════════════════════
    # CAMPO E MATRICE
    # ═══════════════════════════════════════════════════════════════

    def dipole_field(self):
        """Il campo come sistema di dipoli."""
        dipoles = []
        for t in self.tensions:
            tid = t.get('id', '?')
            claim = t.get('claim', '')
            anti = self._invert_claim(claim)
            connections = self._count_resonances(tid, claim)

            dipoles.append({
                'id': tid,
                'claim': claim[:150],
                'anti_claim': anti[:150],
                'connections': connections,
                'potentiality': self._potentiality(t),
            })
        return dipoles

    def assonance_matrix(self):
        """Matrice di assonanza binaria. Pure Python (no numpy)."""
        n = len(self.tensions)
        matrix = [[0] * n for _ in range(n)]
        ids = [t.get('id', '?') for t in self.tensions]

        concepts = [self._extract_concepts(t.get('claim', ''), include_id=t.get('id', ''))
                    for t in self.tensions]
        threshold = self._resonance_threshold()

        for i in range(n):
            for j in range(i + 1, n):
                if len(concepts[i] & concepts[j]) >= threshold:
                    matrix[i][j] = 1
                    matrix[j][i] = 1

        return ids, matrix

    # ═══════════════════════════════════════════════════════════════
    # TRAIETTORIA LAGRANGIANA
    # ═══════════════════════════════════════════════════════════════

    def lagrangian_trajectory(self):
        """
        Il percorso naturale attraverso i dipoli a massimo potenziale.
        Segue le assonanze convergenti. delta_V = angolo del passo.
        """
        dipoles = self.dipole_field()
        ids, A = self.assonance_matrix()

        pot_rank = {'alto': 4, 'medio': 3, 'basso': 2, 'isolato': 1, 'saturo': 0}
        trajectory = []
        visited = set()
        remaining = list(range(len(dipoles)))

        while remaining:
            best_idx = max(remaining, key=lambda i: (
                pot_rank.get(dipoles[i]['potentiality'], 0),
                dipoles[i]['connections'],
            ))

            d = dipoles[best_idx]
            visited.add(best_idx)
            remaining.remove(best_idx)

            resonance_with_path = sum(A[best_idx][j] for j in visited if j != best_idx)

            if resonance_with_path > 0 and d['potentiality'] in ('alto', 'medio'):
                delta_v = 'acuto'
            elif d['potentiality'] == 'isolato':
                delta_v = 'piatto'
            else:
                delta_v = 'tangente'

            trajectory.append({
                'step': len(trajectory) + 1,
                'id': d['id'],
                'potentiality': d['potentiality'],
                'connections': d['connections'],
                'resonance_with_path': resonance_with_path,
                'delta_v': delta_v,
                'anti_claim': d['anti_claim'],
            })

            if len(trajectory) >= 3 and all(
                    t['delta_v'] == 'piatto' for t in trajectory[-3:]):
                break

        return trajectory

    # ═══════════════════════════════════════════════════════════════
    # ESPLORAZIONE
    # ═══════════════════════════════════════════════════════════════

    def explore(self, verbose=True):
        """
        Esplorazione autonoma via lagrangiana.
        Trova passaggi: cluster di convergenza, nuove connessioni, saturazione.
        """
        trajectory = self.lagrangian_trajectory()
        ids, A = self.assonance_matrix()
        dipoles = self.dipole_field()

        passages = []
        clusters_seen = set()

        for step in trajectory:
            idx = next(i for i, d in enumerate(dipoles) if d['id'] == step['id'])
            neighbors = {ids[j] for j in range(len(ids)) if A[idx][j] == 1}
            cluster_key = frozenset(neighbors | {step['id']})

            if len(neighbors) >= 2 and cluster_key not in clusters_seen:
                clusters_seen.add(cluster_key)
                passages.append({
                    'type': 'convergence',
                    'step': step['step'],
                    'dipoles': sorted(neighbors | {step['id']}),
                    'size': len(neighbors) + 1,
                })

        # Stats
        n_assonances = sum(sum(row) for row in A) // 2
        n_alto = sum(1 for d in dipoles if d['potentiality'] in ('alto', 'medio'))
        n_saturo = sum(1 for d in dipoles if d['potentiality'] == 'saturo')

        if verbose:
            self._print_exploration(trajectory, passages, dipoles, n_assonances, n_alto, n_saturo)

        return {
            'trajectory': trajectory,
            'passages': passages,
            'field': {
                'dipoles': len(dipoles),
                'assonances': n_assonances,
                'high_potential': n_alto,
                'saturated': n_saturo,
            },
        }

    def _print_exploration(self, trajectory, passages, dipoles, n_ass, n_alto, n_sat):
        """Output leggibile dell'esplorazione."""
        sym = {'acuto': '◆', 'tangente': '·', 'piatto': '○'}

        print("\n--- TRAIETTORIA LAGRANGIANA ---")
        for t in trajectory:
            s = sym.get(t['delta_v'], '?')
            line = f"  {s} {t['step']:2d}. {t['id']:<45s} pot={t['potentiality']:<8s} conn={t['connections']:<3d} reson={t['resonance_with_path']:<3d} δV={t['delta_v']}"
            print(line)
            if t['delta_v'] == 'acuto':
                print(f"       anti: {t['anti_claim'][:80]}")

        print("\n--- PASSAGGI ---")
        if passages:
            for p in passages:
                names = ', '.join(p['dipoles'][:3])
                if len(p['dipoles']) > 3:
                    names += '...'
                print(f"  [{p['type']}] step {p['step']}: {p['size']} dipoli risuonano: {names}")
        else:
            print("  Nessun passaggio — il campo è uniforme")

        print(f"\n--- CAMPO ---")
        print(f"  Dipoli: {len(dipoles)}  Assonanze: {n_ass}")
        print(f"  Alto potenziale: {n_alto}  Saturi: {n_sat}")
        print(f"  Saturazione piano: {n_sat}/{len(dipoles)}")


# ═══════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description='D-ND Scenario Projector')
    parser.add_argument('--seed', type=str, help='Path to seed JSON file')
    parser.add_argument('--explore', action='store_true', help='Autonomous exploration')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--field', action='store_true', help='Show dipole field')
    args = parser.parse_args()

    sp = ScenarioProjector(seed_path=args.seed)

    if not sp.tensions:
        print("Nessuna tensione nel seme. Usa --seed path/to/seed.json")
        sys.exit(1)

    if args.json:
        result = sp.explore(verbose=False)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    elif args.field:
        dipoles = sp.dipole_field()
        for d in dipoles:
            print(f"  D({d['id']})")
            print(f"    + {d['claim'][:80]}")
            print(f"    - {d['anti_claim'][:80]}")
            print(f"    pot={d['potentiality']}  conn={d['connections']}")
            print()
    elif args.explore:
        direction = sp.seed.get('direction', sp.seed.get('direzione', ''))
        print(f"Direzione: {direction[:80]}")
        print(f"Tensioni: {len(sp.tensions)}")
        sp.explore(verbose=True)
    else:
        # Default: trajectory
        trajectory = sp.lagrangian_trajectory()
        for t in trajectory[:10]:
            sym = {'acuto': '◆', 'tangente': '·', 'piatto': '○'}.get(t['delta_v'], '?')
            print(f"  {sym} {t['id']:<40s} pot={t['potentiality']:<8s} δV={t['delta_v']}")


if __name__ == '__main__':
    main()
