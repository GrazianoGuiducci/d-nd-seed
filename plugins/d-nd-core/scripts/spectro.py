"""
dnd_spettro.py — Spettroscopio D-ND

Mappa numeri puri (costanti adimensionali, rapporti) sulla
coordinata iperbolica h(x) = ln|(x-φ)/(x+1/φ)|

Lo spazio: P^1 proiettivo con metrica indotta dai punti fissi φ e -1/φ.
- h = 0 al centro (x = 1/2)
- h = +2ln(φ) a x = 0 (polo piccolo)
- h = -2ln(φ) a x = 1 (polo grande, = ∞ in P^1)
- Larghezza totale: 4·ln(φ) ≈ 1.925

Da A10: f(0) = ∞, f(∞) = 1. Zero e infinito sono lo stesso punto.
Le costanti sono punti su questo spazio. Le distanze sono strutturali.

Author: TM3 + Operatore
Date: 2026-03-30
"""

import numpy as np
import json
from pathlib import Path

PHI = (1 + np.sqrt(5)) / 2
LN_PHI = np.log(PHI)
LN_PHI2 = 2 * LN_PHI  # = 0.9624, il raggio dello spazio
DATA = Path(__file__).parent / 'data'


# === COORDINATA IPERBOLICA ===

def h(x):
    """
    Coordinata iperbolica D-ND.
    Mappa P^1 → [-2ln(φ), +2ln(φ)].

    φ → -∞ (attrattore)
    -1/φ → +∞ (repulsore)
    0 → +2ln(φ) (polo piccolo)
    1 → -2ln(φ) (polo grande)
    1/2 → 0 (centro)
    """
    if x is None or not np.isfinite(x):
        return -LN_PHI2  # ∞ → h = -2ln(φ) (come x=1 in P^1)
    den = x + 1/PHI
    if abs(den) < 1e-15:
        return float('inf')
    ratio = abs((x - PHI) / den)
    if ratio <= 0:
        return float('-inf')
    return np.log(ratio)


def h_inv(hval):
    """Inversa: da coordinata iperbolica a valore su P^1."""
    # h = ln|(x-φ)/(x+1/φ)|
    # e^h = (x-φ)/(x+1/φ) (prendendo il ramo positivo)
    # e^h (x + 1/φ) = x - φ
    # x(e^h - 1) = -φ - e^h/φ
    # x = (-φ - e^h/φ) / (e^h - 1)
    eh = np.exp(hval)
    if abs(eh - 1) < 1e-15:
        return 0.5  # centro
    return (-PHI - eh/PHI) / (eh - 1)


def distanza(x1, x2):
    """Distanza iperbolica D-ND tra due punti."""
    return abs(h(x1) - h(x2))


# === CATALOGO NUMERI PURI ===

CATALOGO = {
    # Accoppiamenti fondamentali
    'α (EM)':           1/137.035999084,
    'α_s (forte)':      0.1181,
    'α_w (debole)':     1/29.587,        # sin²θ_W ≈ 0.231, g²/4π
    'α_G (gravità)':    5.9e-39,

    # Rapporti di massa
    'm_e/m_p':          5.44617021e-4,
    'm_e/m_τ':          2.87585e-4,
    'm_μ/m_τ':          5.94635e-2,
    'm_p/m_W':          1.164e-2,
    'm_e/m_μ':          4.83633e-3,

    # Rapporti di carica
    'e/q_P':            0.085424,
    '(e/q_P)²=α':       0.007297,

    # Mixing
    'sin²θ_W':          0.23122,
    'sin²θ_C':          0.0484,          # Cabibbo: sin²(13.04°)

    # Costanti matematiche
    'π':                np.pi,
    'e (Euler)':        np.e,
    'φ':                PHI,
    '1/φ':              1/PHI,
    'φ²':               PHI**2,
    'ln(2)':            np.log(2),
    'sqrt(2)':          np.sqrt(2),

    # Numeri notevoli
    '1/2':              0.5,
    '1':                1.0,
    '2':                2.0,
    '10':               10.0,

    # Rapporti composti
    'α_s/α':            0.1181 / (1/137.036),
}


def spettro(subset=None, show_levels=True):
    """
    Mostra lo spettro: tutti i numeri puri nella coordinata h.
    Se show_levels=True, li visualizza come livelli.
    """
    items = CATALOGO if subset is None else {k: CATALOGO[k] for k in subset if k in CATALOGO}

    print(f"\n{'='*70}")
    print(f"SPETTRO D-ND — coordinata iperbolica h(x) = ln|(x-φ)/(x+1/φ)|")
    print(f"Spazio: [-{LN_PHI2:.4f}, +{LN_PHI2:.4f}]  centro: h=0 (x=0.5)")
    print(f"{'='*70}\n")

    entries = [(nome, val, h(val)) for nome, val in items.items()]
    entries.sort(key=lambda e: e[2])

    if show_levels:
        # Visualizzazione a livelli
        width = 60
        for nome, val, hv in entries:
            if not np.isfinite(hv):
                continue
            pos = int((hv / LN_PHI2 + 1) * width / 2)
            pos = max(0, min(width - 1, pos))
            line = [' '] * width
            line[width // 2] = '│'  # centro
            line[pos] = '●'
            bar = ''.join(line)
            print(f"  {hv:+7.4f}  {bar}  {nome} ({val:.4e})")

        # Asse
        axis = ['-'] * width
        axis[0] = '0'
        axis[width // 2] = '½'
        axis[-1] = '1'
        print(f"          {''.join(axis)}")
        print(f"          +{LN_PHI2:.3f}{' ' * (width//2 - 8)}0{' ' * (width//2 - 4)}-{LN_PHI2:.3f}")

    print()
    print(f"{'Nome':20s} {'x':>12s} {'h(x)':>10s}")
    print('-' * 45)
    for nome, val, hv in entries:
        print(f"{nome:20s} {val:12.6e} {hv:+10.4f}")

    return entries


def cluster(soglia=0.05):
    """
    Trova cluster: numeri puri che sono vicini nella coordinata h.
    Soglia: distanza massima per considerarli nello stesso cluster.
    """
    entries = [(nome, val, h(val)) for nome, val in CATALOGO.items()
               if np.isfinite(h(val))]
    entries.sort(key=lambda e: e[2])

    print(f"\n{'='*60}")
    print(f"CLUSTER (soglia Δh < {soglia})")
    print(f"{'='*60}\n")

    clusters = []
    current = [entries[0]]
    for e in entries[1:]:
        if abs(e[2] - current[-1][2]) < soglia:
            current.append(e)
        else:
            if len(current) > 1:
                clusters.append(current)
            current = [e]
    if len(current) > 1:
        clusters.append(current)

    for i, cl in enumerate(clusters):
        h_mean = np.mean([e[2] for e in cl])
        h_spread = max(e[2] for e in cl) - min(e[2] for e in cl)
        print(f"  Cluster #{i+1} — h ≈ {h_mean:+.4f} (spread={h_spread:.4f})")
        for nome, val, hv in cl:
            print(f"    {nome:20s}  x={val:.6e}  h={hv:+.4f}")
        print()

    if not clusters:
        print("  Nessun cluster trovato.")

    return clusters


def confronta_spettro(nome_spettro, livelli):
    """
    Confronta la distribuzione delle costanti con uno spettro noto.
    livelli: lista di valori x (es. 1/n² per idrogeno).
    """
    print(f"\n{'='*60}")
    print(f"CONFRONTO con spettro: {nome_spettro}")
    print(f"{'='*60}\n")

    h_livelli = [(f"n={i+1}", x, h(x)) for i, x in enumerate(livelli)]
    h_consts = [(nome, val, h(val)) for nome, val in CATALOGO.items()
                if 0 < val < 1 and nome not in ('φ', '1/φ', 'φ²', '1/2', '1', '2')]

    # Per ogni costante, trova il livello più vicino
    print(f"{'Costante':20s} {'h':>8s}  {'Livello vicino':>15s} {'h_liv':>8s}  {'Δh':>8s}")
    print('-' * 65)

    for cn, cv, ch in sorted(h_consts, key=lambda x: x[2]):
        if not np.isfinite(ch):
            continue
        best = min(h_livelli, key=lambda l: abs(l[2] - ch))
        delta = ch - best[2]
        print(f"{cn:20s} {ch:+8.4f}  {best[0]:>15s} {best[2]:+8.4f}  {delta:+8.4f}")

    return h_livelli


def inserisci(nome, valore):
    """Inserisce un nuovo numero puro nel catalogo e mostra dove cade."""
    CATALOGO[nome] = valore
    hv = h(valore)
    print(f"Inserito: {nome} = {valore:.6e}, h = {hv:+.4f}")

    # Trova i vicini
    entries = [(n, v, h(v)) for n, v in CATALOGO.items() if n != nome and np.isfinite(h(v))]
    entries.sort(key=lambda e: abs(e[2] - hv))

    print(f"Vicini più prossimi:")
    for n, v, hv2 in entries[:3]:
        print(f"  {n:20s}  h={hv2:+.4f}  Δh={abs(hv-hv2):.4f}")


def mappa_teoria(dipoli_normalizzati):
    """
    Prende i numeri normalizzati di una teoria (da dnd_teoria.py)
    e li mappa nello spettro. Ponte tra i due strumenti.
    """
    for nome, val in dipoli_normalizzati.items():
        inserisci(nome, val)


# === CLI ===

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--spettro':
            spettro()
        elif cmd == '--cluster':
            soglia = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
            cluster(soglia)
        elif cmd == '--idrogeno':
            confronta_spettro('Idrogeno (1/n²)', [1/n**2 for n in range(1, 20)])
        elif cmd == '--oscillatore':
            confronta_spettro('Oscillatore armonico ((2n+1)/2)', [(2*n+1)/(2*20) for n in range(20)])
        elif cmd == '--inserisci':
            if len(sys.argv) >= 4:
                inserisci(sys.argv[2], float(sys.argv[3]))
            else:
                print("Uso: --inserisci nome valore")
        else:
            print(f"Uso: python {sys.argv[0]} [--spettro|--cluster [soglia]|--idrogeno|--oscillatore|--inserisci nome val]")
    else:
        spettro()
