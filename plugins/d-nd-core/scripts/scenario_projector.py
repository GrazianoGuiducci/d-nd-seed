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
    python scenario_projector.py --cross-check            # verifica strutturale
    python scenario_projector.py --strategy               # insight strategici
    python scenario_projector.py --action-plan            # azioni prioritizzate

As library:
    from scenario_projector import ScenarioProjector
    sp = ScenarioProjector(seed_path='path/to/seed.json')
    trajectory = sp.lagrangian_trajectory()
    passages = sp.explore()
    checks = sp.cross_check()
    strategy = sp.strategy()
    plan = sp.action_plan()

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

        # 1. Dipolo esplicito — claim che CONTIENE già i due poli
        # Nota: il delimitatore finale è opzionale ([\.\,]?) + $ per catturare fino a fine stringa
        dipole_patterns = [
            r'[Tt]ensione?\s+tra\s+(.+?)\s+e\s+(.+?)[\.\,]',
            r'(.+?)\s+vs\.?\s+(.+)',
            r'(.+?)\s+ma\s+(.+)',
            r'(.+?)\s+per[oò]\s+(.+)',
            r'(.+?)\s+but\s+(.+)',
            r'(.+?)\s+however,?\s+(.+)',
            r'(.+?)\s+while\s+(.+)',
            r'(.+?)\s+yet\s+(.+)',
            r'(.+?)\s+—\s+(.+)',
        ]
        for pat in dipole_patterns:
            m = re.search(pat, cl)
            if m:
                polo_b = m.group(2).strip().rstrip('.,;')
                polo_a = m.group(1).strip().rstrip('.,;')
                # Return polo_b as anti-claim (the counter-pole)
                return f'{polo_b} (not: {polo_a[:60]})'

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

        # 3. Fallback — detect language from claim
        has_italian = bool(re.search(r'\b(della|nella|questo|questa|sono|ogni)\b', cl, re.IGNORECASE))
        if has_italian:
            return f'Il contrario: {cl[:100]}... non è necessariamente vero'
        return f'The opposite: {cl[:100]}... is not necessarily true'

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

    # ═══════════════════════════════════════════════════════════════
    # CROSS-CHECK — verifica una proiezione da più angoli
    # ═══════════════════════════════════════════════════════════════

    def cross_check(self, tension_id=None):
        """
        Verifica strutturale di una tensione o dell'intero campo.

        Per ogni tensione verificata:
        1. Rimozione: cosa succede al campo senza questa tensione?
        2. Anti-scenario: se seguiamo l'anti-claim, dove porta?
        3. Conferma incrociata: quante tensioni adiacenti la supportano?

        Returns: lista di check, uno per tensione analizzata.
        """
        dipoles = self.dipole_field()
        ids, A = self.assonance_matrix()
        id_to_idx = {d['id']: i for i, d in enumerate(dipoles)}

        targets = [d for d in dipoles if d['id'] == tension_id] if tension_id else dipoles
        checks = []

        for d in targets:
            idx = id_to_idx.get(d['id'])
            if idx is None:
                continue

            # 1. Neighbors — who resonates with this dipole?
            neighbors = [ids[j] for j in range(len(ids)) if A[idx][j] == 1]

            # 2. Field without this tension — how much does connectivity drop?
            total_connections = d['connections']
            other_connections = sum(
                dipoles[id_to_idx[n]]['connections'] for n in neighbors
                if n in id_to_idx
            )
            # If removing this dipole would reduce neighbors' average connectivity
            # significantly, it's a structural pillar
            is_pillar = (total_connections >= 4 and
                         len(neighbors) >= 3)

            # 3. Support ratio — what fraction of neighbors are high potential?
            high_neighbors = sum(
                1 for n in neighbors
                if n in id_to_idx and dipoles[id_to_idx[n]]['potentiality'] in ('alto', 'medio')
            )
            support = high_neighbors / max(len(neighbors), 1)

            # 4. Contradiction check — does the anti-claim resonate with any neighbor's claim?
            # Contradiction requires STRONGER evidence than assonance:
            # sharing one domain word isn't a contradiction, it's just same domain.
            # Threshold: resonance_threshold + 1, minimum 2.
            anti_concepts = self._extract_concepts(d['anti_claim'])
            contradiction_threshold = max(self._resonance_threshold() + 1, 2)
            contradictions = []
            for n in neighbors:
                if n not in id_to_idx:
                    continue
                n_concepts = self._extract_concepts(dipoles[id_to_idx[n]]['claim'],
                                                     include_id=n)
                if len(anti_concepts & n_concepts) >= contradiction_threshold:
                    contradictions.append(n)

            # Verdict
            if contradictions:
                verdict = 'contested'
            elif is_pillar and support > 0.5:
                verdict = 'confirmed'
            elif d['potentiality'] == 'isolato':
                verdict = 'unverifiable'
            elif support > 0.3:
                verdict = 'supported'
            else:
                verdict = 'weak'

            checks.append({
                'id': d['id'],
                'potentiality': d['potentiality'],
                'connections': total_connections,
                'neighbors': neighbors,
                'is_pillar': is_pillar,
                'support_ratio': round(support, 2),
                'contradictions': contradictions,
                'verdict': verdict,
                'anti_claim': d['anti_claim'],
            })

        return checks

    # ═══════════════════════════════════════════════════════════════
    # STRATEGY — dove concentrare lo sforzo
    # ═══════════════════════════════════════════════════════════════

    def strategy(self):
        """
        Estrae insight strategici dalla proiezione.

        Returns:
            focus: dove concentrare lo sforzo (cluster più densi)
            blind_spots: dipoli isolati che potrebbero nascondere qualcosa
            risks: anti-claim delle tensioni più connesse
            completed: cosa è saturo (fatto)
            leverage: punti dove un'azione ha massimo impatto (pilastri)
        """
        result = self.explore(verbose=False)
        checks = self.cross_check()
        trajectory = result['trajectory']
        passages = result['passages']

        # Focus — convergence clusters sorted by size
        focus = sorted(passages, key=lambda p: p['size'], reverse=True)

        # Blind spots — isolated or unverifiable
        blind_spots = [c for c in checks if c['verdict'] in ('unverifiable', 'weak')]

        # Risks — anti-claims of the most connected (top 5)
        top_connected = sorted(checks, key=lambda c: c['connections'], reverse=True)[:5]
        risks = [{
            'id': c['id'],
            'anti_claim': c['anti_claim'],
            'connections': c['connections'],
            'contradictions': c['contradictions'],
        } for c in top_connected if c['anti_claim']]

        # Completed — saturated tensions
        completed = [c for c in checks if c['potentiality'] == 'saturo']

        # Leverage — structural pillars
        leverage = [c for c in checks if c['is_pillar'] and c['verdict'] == 'confirmed']

        return {
            'focus': focus,
            'blind_spots': blind_spots,
            'risks': risks,
            'completed': completed,
            'leverage': leverage,
            'field': result['field'],
        }

    # ═══════════════════════════════════════════════════════════════
    # ACTION PLAN — dalla strategia alle azioni
    # ═══════════════════════════════════════════════════════════════

    # Domain-specific language for action plans
    _DOMAIN_LABELS = {
        'startup_strategy': {
            'focus': 'Strategic convergence — these decisions are coupled',
            'risk': 'Growth risk — structural contradiction in the thesis',
            'blind_spot': 'Under-explored — could be hidden opportunity or noise',
            'leverage': 'Foundation — invest here, it propagates everywhere',
        },
        'product_roadmap': {
            'focus': 'Feature cluster — build together, they share dependencies',
            'risk': 'Roadmap conflict — these features work against each other',
            'blind_spot': 'Orphan feature — disconnected from the product story',
            'leverage': 'Platform foundation — enables everything downstream',
        },
        'due_diligence': {
            'focus': 'Correlated metrics — verify these together',
            'risk': 'Thesis contradiction — the investment story has a crack here',
            'blind_spot': 'Due diligence gap — not connected to the main thesis',
            'leverage': 'Thesis anchor — the strongest proof point, double down',
        },
        'risk_assessment': {
            'focus': 'Risk cascade — these risks trigger each other',
            'risk': 'Counter-risk — the mitigation creates a new exposure',
            'blind_spot': 'Unmonitored risk — not connected to existing controls',
            'leverage': 'Mitigation pillar — this control protects multiple risks',
        },
        'portfolio_management': {
            'focus': 'Correlated positions — these risks move together',
            'risk': 'Structural fragility — this allocation breaks under stress',
            'blind_spot': 'Unhedged exposure — disconnected from risk framework',
            'leverage': 'Portfolio anchor — this allocation stabilizes the whole',
        },
    }

    def _domain_label(self, action_type):
        """Get domain-specific label for an action type."""
        ctx = self.seed.get('context', '')
        domain = self._DOMAIN_LABELS.get(ctx, {})
        return domain.get(action_type, '')

    def action_plan(self):
        """
        Genera un piano d'azione dalla proiezione.

        Ogni azione ha:
        - what: cosa fare (domain-aware)
        - why: perché (dalla struttura)
        - risk: anti-claim del polo opposto
        - priority: dalla posizione nella traiettoria lagrangiana
        """
        strat = self.strategy()
        checks_by_id = {c['id']: c for c in self.cross_check()}

        actions = []

        # 1. Focus actions — from convergence clusters
        for i, cluster in enumerate(strat['focus'][:3]):
            dipole_ids = cluster.get('dipoles', [])
            contested = [d for d in dipole_ids if checks_by_id.get(d, {}).get('verdict') == 'contested']
            label = self._domain_label('focus')
            names = ', '.join(d.replace('_', ' ').lower() for d in dipole_ids[:4])

            actions.append({
                'type': 'focus',
                'what': label or f"Convergence cluster at step {cluster.get('step', '?')}",
                'detail': f"{len(dipole_ids)} tensions share structural dependencies: {names}",
                'risk': f"{len(contested)} contested" if contested else 'No contradictions',
                'priority': i + 1,
                'ids': dipole_ids[:8],
            })

        # 2. Risk actions — from top anti-claims with real contradictions
        for risk in strat['risks'][:3]:
            if risk['contradictions']:
                label = self._domain_label('risk')
                actions.append({
                    'type': 'risk',
                    'what': label or f"Structural contradiction: {risk['id']}",
                    'detail': f"{risk['id']} contested by {', '.join(risk['contradictions'][:3])}",
                    'risk': risk['anti_claim'][:200],
                    'priority': len(actions) + 1,
                    'ids': [risk['id']] + risk['contradictions'][:3],
                })

        # 3. Blind spot actions
        for blind in strat['blind_spots'][:2]:
            label = self._domain_label('blind_spot')
            actions.append({
                'type': 'blind_spot',
                'what': label or f"Investigate: {blind['id']}",
                'detail': f"{blind['id']} is disconnected from the field ({blind['connections']} connections)",
                'risk': blind['anti_claim'][:200],
                'priority': len(actions) + 1,
                'ids': [blind['id']],
            })

        # 4. Leverage actions — amplify confirmed pillars
        for lev in strat['leverage'][:2]:
            label = self._domain_label('leverage')
            actions.append({
                'type': 'leverage',
                'what': label or f"Amplify pillar: {lev['id']}",
                'detail': f"{lev['id']} — {lev['connections']} connections, {lev['support_ratio']:.0%} structural support",
                'risk': lev['anti_claim'][:200],
                'priority': len(actions) + 1,
                'ids': [lev['id']] + lev['neighbors'][:3],
            })

        return {
            'actions': actions,
            'summary': {
                'focus_clusters': len(strat['focus']),
                'risks': len([r for r in strat['risks'] if r['contradictions']]),
                'blind_spots': len(strat['blind_spots']),
                'leverage_points': len(strat['leverage']),
                'completed': len(strat['completed']),
            },
            'field': strat['field'],
        }


# ═══════════════════════════════════════════════════════════════════
# CLI — print helpers
# ═══════════════════════════════════════════════════════════════════

_VERDICT_SYM = {
    'confirmed': '✓', 'supported': '~', 'contested': '✗',
    'weak': '?', 'unverifiable': '—',
}
_VERDICT_COLOR = {
    'confirmed': '\033[32m', 'supported': '\033[33m', 'contested': '\033[31m',
    'weak': '\033[90m', 'unverifiable': '\033[90m',
}
_RESET = '\033[0m'


def _print_cross_check(checks):
    print("\n--- CROSS-CHECK ---")
    for c in checks:
        sym = _VERDICT_SYM.get(c['verdict'], '?')
        clr = _VERDICT_COLOR.get(c['verdict'], '')
        pillar = ' [PILLAR]' if c['is_pillar'] else ''
        print(f"  {clr}{sym}{_RESET} {c['id']:<40s} {clr}{c['verdict']}{_RESET}{pillar}")
        print(f"       conn={c['connections']}  support={c['support_ratio']:.0%}  neighbors={len(c['neighbors'])}")
        if c['contradictions']:
            print(f"       ✗ contradicted by: {', '.join(c['contradictions'][:4])}")
    # Summary
    verdicts = [c['verdict'] for c in checks]
    print(f"\n  Totale: {len(checks)} tensioni")
    for v in ['confirmed', 'supported', 'contested', 'weak', 'unverifiable']:
        n = verdicts.count(v)
        if n:
            print(f"    {_VERDICT_SYM[v]} {v}: {n}")


def _print_strategy(strat):
    print("\n--- STRATEGIA ---")

    if strat['focus']:
        print(f"\n  FOCUS ({len(strat['focus'])} cluster di convergenza)")
        for i, f in enumerate(strat['focus'][:5]):
            names = ', '.join(f.get('dipoles', [])[:3])
            print(f"    {i+1}. step {f.get('step','?')}: {f.get('size','?')} dipoli — {names}")

    if strat['leverage']:
        print(f"\n  LEVA ({len(strat['leverage'])} pilastri confermati)")
        for lev in strat['leverage'][:5]:
            print(f"    ✓ {lev['id']} — {lev['connections']} conn, {lev['support_ratio']:.0%} support")

    if strat['risks']:
        risks_with_contradiction = [r for r in strat['risks'] if r['contradictions']]
        if risks_with_contradiction:
            print(f"\n  RISCHI ({len(risks_with_contradiction)} contraddizioni)")
            for r in risks_with_contradiction[:5]:
                print(f"    ✗ {r['id']} contestato da {', '.join(r['contradictions'][:3])}")

    if strat['blind_spots']:
        print(f"\n  PUNTI CIECHI ({len(strat['blind_spots'])} isolati/deboli)")
        for b in strat['blind_spots'][:5]:
            print(f"    ? {b['id']} — {b['verdict']}")

    if strat['completed']:
        print(f"\n  COMPLETATI ({len(strat['completed'])} saturi)")
        for c in strat['completed'][:5]:
            print(f"    ○ {c['id']}")

    f = strat['field']
    print(f"\n  CAMPO: {f['dipoles']} dipoli, {f['assonances']} assonanze, {f['high_potential']} alto pot., {f['saturated']} saturi")


def _print_action_plan(plan):
    print("\n--- ACTION PLAN ---")
    s = plan['summary']
    print(f"  {s['focus_clusters']} cluster | {s['risks']} risks | {s['blind_spots']} blind spots | {s['leverage_points']} leverage | {s['completed']} completed")

    type_sym = {'focus': '▶', 'risk': '✗', 'blind_spot': '?', 'leverage': '✓'}

    for a in plan['actions']:
        sym = type_sym.get(a['type'], '·')
        print(f"\n  {sym} [{a['priority']}] {a['what']}")
        if a.get('detail'):
            print(f"    {a['detail']}")
        if a.get('risk'):
            print(f"    Risk: {a['risk']}")
        if a.get('ids'):
            print(f"    Tensions: {', '.join(a['ids'][:5])}")


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
    parser.add_argument('--cross-check', action='store_true', help='Structural cross-check')
    parser.add_argument('--strategy', action='store_true', help='Strategic insights')
    parser.add_argument('--action-plan', action='store_true', help='Prioritized action plan')
    parser.add_argument('--tension', type=str, help='Specific tension ID (for --cross-check)')
    args = parser.parse_args()

    sp = ScenarioProjector(seed_path=args.seed)

    if not sp.tensions:
        print("Nessuna tensione nel seme. Usa --seed path/to/seed.json")
        sys.exit(1)

    if args.json:
        result = sp.explore(verbose=False)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    elif args.cross_check:
        checks = sp.cross_check(tension_id=args.tension)
        _print_cross_check(checks)
    elif args.strategy:
        strat = sp.strategy()
        _print_strategy(strat)
    elif args.action_plan:
        plan = sp.action_plan()
        _print_action_plan(plan)
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
