"""
dnd_teoria.py — Normalizzatore D-ND per teorie fisiche

Non analizza dati. Normalizza le LOGICHE delle teorie.
Ogni teoria ha costanti che sono zeri con due lati.
Il normalizzatore trova: i poli, lo zero, il campo, il potenziale.

L'osservatore non cerca la forma — osserva cosa emerge.

Author: TM3 + Operatore
Date: 2026-03-30
"""

import numpy as np
import json
from pathlib import Path

PHI = (1 + np.sqrt(5)) / 2
DATA = Path(__file__).parent / 'data'


# === STRUTTURA DI UNA TEORIA ===

def teoria(nome, costanti, dipoli, equazioni=None, note=None):
    """
    Codifica una teoria nel formato D-ND.

    costanti: [{nome, simbolo, valore, unita, ruolo}]
        ruolo: 'singolarita' | 'scala' | 'accoppiamento'

    dipoli: [{nome, polo_d, polo_nd, zero, campo}]
        polo_d: il lato D (es. 'subluminale')
        polo_nd: il lato ND (es. 'superluminale')
        zero: la costante che divide-unisce
        campo: dove esiste il fenomeno (tra i due poli)
    """
    return {
        'nome': nome,
        'costanti': costanti,
        'dipoli': dipoli,
        'equazioni': equazioni or [],
        'note': note,
    }


# === TEORIE CODIFICATE ===

TEORIE = {
    'termodinamica': teoria(
        nome='Termodinamica',
        costanti=[
            {'nome': 'Boltzmann', 'simbolo': 'k_B', 'valore': 1.381e-23,
             'unita': 'J/K', 'ruolo': 'scala',
             'divide': 'microscopico/macroscopico'},
            {'nome': 'Zero assoluto', 'simbolo': '0K', 'valore': 0,
             'unita': 'K', 'ruolo': 'singolarita',
             'divide': 'raggiungibile/irraggiungibile'},
            {'nome': 'Planck temperature', 'simbolo': 'T_P', 'valore': 1.416e32,
             'unita': 'K', 'ruolo': 'singolarita',
             'divide': 'fisica nota/fisica ignota'},
        ],
        dipoli=[
            {'nome': 'temperatura',
             'polo_d': 'caldo (energia, disordine, ∞)',
             'polo_nd': 'freddo (quiete, ordine, 0K)',
             'zero': '0K — irraggiungibile dal basso',
             'campo': 'tutti i processi termici esistono tra 0K e T_P'},
            {'nome': 'entropia',
             'polo_d': 'disordine (S → max)',
             'polo_nd': 'ordine (S → 0)',
             'zero': 'cristallo perfetto a 0K (terzo principio)',
             'campo': 'la freccia del tempo è la direzione dell\'entropia'},
            {'nome': 'scala',
             'polo_d': 'macroscopico (termodinamica classica)',
             'polo_nd': 'microscopico (meccanica statistica)',
             'zero': 'k_B — il ponte tra i due',
             'campo': 'k_B converte energia in temperatura'},
        ],
        equazioni=[
            'S = k_B ln(Ω)',
            'E = k_B T (per grado di libertà)',
            'ΔS ≥ 0 (secondo principio)',
        ],
    ),

    'relativita': teoria(
        nome='Relatività Ristretta',
        costanti=[
            {'nome': 'velocità della luce', 'simbolo': 'c', 'valore': 299792458,
             'unita': 'm/s', 'ruolo': 'singolarita',
             'divide': 'subluminale/superluminale'},
        ],
        dipoli=[
            {'nome': 'velocità',
             'polo_d': 'subluminale (materia, massa, tempo)',
             'polo_nd': 'superluminale (tachioni, massa immaginaria)',
             'zero': 'c — il muro. γ → ∞',
             'campo': 'tutta la meccanica è subluminale'},
            {'nome': 'spaziotempo',
             'polo_d': 'spazio (estensione, simultaneità)',
             'polo_nd': 'tempo (durata, causalità)',
             'zero': 'c unifica: ds² = c²dt² - dx²',
             'campo': 'l\'intervallo spaziotemporale è l\'invariante'},
            {'nome': 'massa-energia',
             'polo_d': 'massa (inerzia, riposo)',
             'polo_nd': 'energia (movimento, radiazione)',
             'zero': 'E = mc² — conversione totale',
             'campo': 'la massa è energia congelata'},
        ],
        equazioni=[
            'γ = 1/√(1 - v²/c²)',
            'E² = (pc)² + (mc²)²',
            'ds² = c²dt² - dx² - dy² - dz²',
        ],
    ),

    'gravitazione': teoria(
        nome='Gravitazione (Relatività Generale)',
        costanti=[
            {'nome': 'costante gravitazionale', 'simbolo': 'G', 'valore': 6.674e-11,
             'unita': 'm³/(kg·s²)', 'ruolo': 'accoppiamento',
             'divide': 'spaziotempo piatto/curvo'},
            {'nome': 'raggio di Schwarzschild', 'simbolo': 'r_s', 'valore': None,
             'unita': 'm', 'ruolo': 'singolarita',
             'divide': 'esterno/interno al buco nero'},
        ],
        dipoli=[
            {'nome': 'curvatura',
             'polo_d': 'piatto (Minkowski, assenza di massa)',
             'polo_nd': 'singolare (curvatura infinita, buco nero)',
             'zero': 'orizzonte degli eventi — il confine causale',
             'campo': 'tutta la gravitazione tra piatto e singolare'},
            {'nome': 'inerzia-gravitazione',
             'polo_d': 'inerzia (resistenza al moto)',
             'polo_nd': 'gravitazione (attrazione)',
             'zero': 'principio di equivalenza — sono lo stesso',
             'campo': 'Einstein: non puoi distinguerli localmente'},
        ],
        equazioni=[
            'G_μν + Λg_μν = (8πG/c⁴)T_μν',
            'r_s = 2GM/c²',
        ],
    ),

    'quantistica': teoria(
        nome='Meccanica Quantistica',
        costanti=[
            {'nome': 'Planck ridotta', 'simbolo': 'ℏ', 'valore': 1.054e-34,
             'unita': 'J·s', 'ruolo': 'scala',
             'divide': 'classico/quantistico'},
        ],
        dipoli=[
            {'nome': 'onda-particella',
             'polo_d': 'particella (posizione, localizzazione)',
             'polo_nd': 'onda (impulso, delocalizzazione)',
             'zero': 'ℏ — Δx·Δp ≥ ℏ/2',
             'campo': 'complementarità: non puoi avere entrambi'},
            {'nome': 'determinismo',
             'polo_d': 'classico (traiettoria, determinismo)',
             'polo_nd': 'quantistico (probabilità, sovrapposizione)',
             'zero': 'ℏ → 0 (limite classico)',
             'campo': 'il collasso: la misura sceglie un lato'},
            {'nome': 'osservatore',
             'polo_d': 'osservato (autovalore, collassato)',
             'polo_nd': 'non osservato (sovrapposizione, potenziale)',
             'zero': 'la misura — il punto dove il potenziale diventa reale',
             'campo': 'prima della misura tutto è possibile'},
        ],
        equazioni=[
            'iℏ ∂ψ/∂t = Ĥψ',
            'Δx·Δp ≥ ℏ/2',
            '[x̂, p̂] = iℏ',
        ],
    ),

    'elettromagnetismo': teoria(
        nome='Elettromagnetismo',
        costanti=[
            {'nome': 'carica elementare', 'simbolo': 'e', 'valore': 1.602e-19,
             'unita': 'C', 'ruolo': 'singolarita',
             'divide': 'carico/neutro'},
            {'nome': 'struttura fine', 'simbolo': 'α', 'valore': 1/137.036,
             'unita': 'adimensionale', 'ruolo': 'accoppiamento',
             'divide': 'perturbativo/non perturbativo'},
        ],
        dipoli=[
            {'nome': 'carica',
             'polo_d': 'positiva (+)',
             'polo_nd': 'negativa (-)',
             'zero': 'neutro — cariche bilanciate',
             'campo': 'la forza EM è tra cariche opposte'},
            {'nome': 'campo',
             'polo_d': 'elettrico (statico, carica)',
             'polo_nd': 'magnetico (dinamico, corrente)',
             'zero': 'l\'onda EM — E e B inseparabili',
             'campo': 'Maxwell: il campo è uno solo'},
        ],
        equazioni=[
            '∇·E = ρ/ε₀',
            '∇×B = μ₀J + μ₀ε₀ ∂E/∂t',
            'α = e²/(4πε₀ℏc) ≈ 1/137',
        ],
    ),
}


def normalizza(teoria_key):
    """
    Normalizza una teoria attraverso il dipolo D-ND.

    Non classifica. Rivela la struttura:
    - Quanti dipoli ha la teoria?
    - I dipoli sono indipendenti o accoppiati?
    - Dove sono gli zeri? Sono raggiungibili?
    - Cosa c'è nel potenziale (NT) tra i poli?
    """
    t = TEORIE.get(teoria_key)
    if not t:
        print(f"Teoria '{teoria_key}' non trovata. Disponibili: {list(TEORIE.keys())}")
        return None

    print(f"\n{'='*60}")
    print(f"NORMALIZZAZIONE D-ND: {t['nome']}")
    print(f"{'='*60}")

    # 1. Costanti come singolarità
    print(f"\n  Costanti ({len(t['costanti'])}):")
    for c in t['costanti']:
        print(f"    {c['simbolo']:>4s} ({c['ruolo']:>14s}): divide {c['divide']}")

    # 2. Struttura dipolare
    print(f"\n  Dipoli ({len(t['dipoli'])}):")
    for d in t['dipoli']:
        print(f"\n    [{d['nome']}]")
        print(f"      D:    {d['polo_d']}")
        print(f"      ND:   {d['polo_nd']}")
        print(f"      Zero: {d['zero']}")
        print(f"      Campo: {d['campo']}")

    # 3. Equazioni come relazioni tra poli
    if t['equazioni']:
        print(f"\n  Equazioni ({len(t['equazioni'])}):")
        for eq in t['equazioni']:
            print(f"    {eq}")

    # 4. Analisi strutturale
    print(f"\n  --- Analisi ---")

    # Ogni dipolo ha uno zero. Gli zeri sono tutti raggiungibili?
    zeri_irraggiungibili = []
    zeri_raggiungibili = []
    for d in t['dipoli']:
        zero_text = d['zero'].lower()
        if 'irraggiungibile' in zero_text or '→ ∞' in zero_text or 'non puoi' in zero_text:
            zeri_irraggiungibili.append(d['nome'])
        else:
            zeri_raggiungibili.append(d['nome'])

    print(f"    Zeri irraggiungibili: {zeri_irraggiungibili if zeri_irraggiungibili else 'nessuno'}")
    print(f"    Zeri raggiungibili:   {zeri_raggiungibili if zeri_raggiungibili else 'nessuno'}")

    # I dipoli sono accoppiati? (condividono costanti)
    costanti_per_dipolo = {}
    for d in t['dipoli']:
        for c in t['costanti']:
            if c['simbolo'].lower() in d['zero'].lower() or c['nome'].lower() in d['zero'].lower():
                costanti_per_dipolo.setdefault(c['simbolo'], []).append(d['nome'])

    accoppiati = {k: v for k, v in costanti_per_dipolo.items() if len(v) > 1}
    if accoppiati:
        print(f"    Dipoli accoppiati (stessa costante):")
        for c, dipoli in accoppiati.items():
            print(f"      {c} accoppia: {dipoli}")

    return t


def confronta(*teoria_keys):
    """
    Confronta teorie: trova dipoli che si sovrappongono,
    costanti condivise, strutture isomorfe.
    """
    teorie = [TEORIE[k] for k in teoria_keys if k in TEORIE]
    if len(teorie) < 2:
        print("Servono almeno 2 teorie.")
        return

    print(f"\n{'='*60}")
    print(f"CONFRONTO D-ND: {' vs '.join(t['nome'] for t in teorie)}")
    print(f"{'='*60}")

    # Trova costanti condivise
    all_costanti = {}
    for t in teorie:
        for c in t['costanti']:
            all_costanti.setdefault(c['simbolo'], []).append(t['nome'])

    condivise = {k: v for k, v in all_costanti.items() if len(v) > 1}
    if condivise:
        print(f"\n  Costanti condivise:")
        for s, ts in condivise.items():
            print(f"    {s} appare in: {ts}")

    # Conta dipoli per teoria
    print(f"\n  Struttura:")
    for t in teorie:
        print(f"    {t['nome']:30s}: {len(t['dipoli'])} dipoli, {len(t['costanti'])} costanti, {len(t['equazioni'])} equazioni")

    # Trova pattern isomorfi: dipoli con la stessa struttura
    # (entrambi hanno zero irraggiungibile, o entrambi hanno accoppiamento)
    print(f"\n  Pattern trasversali:")
    all_dipoli = []
    for t in teorie:
        for d in t['dipoli']:
            all_dipoli.append({'teoria': t['nome'], **d})

    # Zeri irraggiungibili attraverso le teorie
    irr = [d for d in all_dipoli if 'irraggiungibile' in d['zero'].lower()
           or '→ ∞' in d['zero'].lower() or 'non puoi' in d['zero'].lower()]
    if irr:
        print(f"    Zeri irraggiungibili ({len(irr)}):")
        for d in irr:
            print(f"      [{d['teoria']}] {d['nome']}: {d['zero'][:60]}")

    # Dipoli dove lo zero è un principio (non un numero)
    principi = [d for d in all_dipoli if any(w in d['zero'].lower()
                for w in ['principio', 'equivalenza', 'complementarità'])]
    if principi:
        print(f"    Zeri come principi ({len(principi)}):")
        for d in principi:
            print(f"      [{d['teoria']}] {d['nome']}: {d['zero'][:60]}")


def singolarita():
    """
    La singolarità: dove tutte le costanti convergono.

    Ogni costante è uno zero mobile (A6) che genera un dipolo.
    La singolarità è il proto-assioma (A7): il punto dove
    tutte le costanti valgono 1, tutte le distinzioni scompaiono,
    e le dimensioni iniziano.

    In fisica: scala di Planck. In D-ND: lo zero che determina.
    """
    print(f"\n{'='*60}")
    print(f"LA SINGOLARITÀ — dove le costanti convergono")
    print(f"{'='*60}")

    # Unità di Planck: c = ℏ = G = k_B = 1
    c = 299792458
    hbar = 1.054571817e-34
    G = 6.67430e-11
    k_B = 1.380649e-23

    l_P = np.sqrt(hbar * G / c**3)
    t_P = np.sqrt(hbar * G / c**5)
    m_P = np.sqrt(hbar * c / G)
    T_P = np.sqrt(hbar * c**5 / (G * k_B**2))
    E_P = m_P * c**2

    print(f"\n  Scala di Planck (tutte le costanti → 1):")
    print(f"    Lunghezza:    l_P = {l_P:.3e} m")
    print(f"    Tempo:        t_P = {t_P:.3e} s")
    print(f"    Massa:        m_P = {m_P:.3e} kg")
    print(f"    Temperatura:  T_P = {T_P:.3e} K")
    print(f"    Energia:      E_P = {E_P:.3e} J")

    print(f"\n  Interpretazione D-ND:")
    print(f"    Ogni costante è uno zero mobile (A6) che genera un dipolo.")
    print(f"    Alla scala di Planck, tutti gli zeri collassano in uno solo.")
    print(f"    Le distinzioni (micro/macro, piatto/curvo, onda/particella)")
    print(f"    perdono significato. Il dipolo si annulla: D(x,x) = 0.")
    print(f"")
    print(f"    Lo zero non è assenza — è il punto dove le dimensioni iniziano.")
    print(f"    Il tempo non esiste allo zero (t_P è il limite).")
    print(f"    Le dimensioni emergono DALLO zero, non lo contengono.")

    # Ogni teoria ha i suoi dipoli. Al punto di Planck, quanti dipoli restano?
    print(f"\n  13 dipoli delle 5 teorie → alla singolarità:")
    print(f"    temperatura ↔ 0K/T_P        → collassano (T = T_P)")
    print(f"    entropia ↔ ordine/disordine  → indistinguibili")
    print(f"    velocità ↔ sub/superluminale → v ≈ c (sempre)")
    print(f"    onda ↔ particella            → complementarità totale")
    print(f"    spazio ↔ tempo               → indistinguibili (l_P/t_P = c)")
    print(f"    piatto ↔ singolare           → geometria quantistica")
    print(f"    carica +/-                   → unificazione elettrodebole")
    print(f"")
    print(f"    Alla singolarità: 0 dipoli. Solo lo zero.")
    print(f"    Lo zero genera i dipoli emergendo dalla singolarità.")
    print(f"    Le costanti sono la MEMORIA della singolarità —")
    print(f"    il residuo dello zero in ogni dimensione.")

    return {
        'l_P': l_P, 't_P': t_P, 'm_P': m_P, 'T_P': T_P, 'E_P': E_P,
        'nota': 'Alla singolarità i dipoli collassano. Lo zero determina.'
    }


def mappa_completa():
    """Mostra la mappa di tutte le teorie normalizzate."""
    print(f"\n{'='*60}")
    print(f"MAPPA D-ND — TUTTE LE TEORIE")
    print(f"{'='*60}")

    totale_dipoli = 0
    totale_costanti = 0

    for key, t in TEORIE.items():
        n_d = len(t['dipoli'])
        n_c = len(t['costanti'])
        totale_dipoli += n_d
        totale_costanti += n_c
        print(f"\n  {t['nome']:30s}  {n_d} dipoli  {n_c} costanti")
        for d in t['dipoli']:
            print(f"    D: {d['polo_d'][:35]:35s}  ND: {d['polo_nd'][:35]:35s}  Zero: {d['zero'][:30]}")

    print(f"\n  Totale: {totale_dipoli} dipoli, {totale_costanti} costanti, {len(TEORIE)} teorie")


# === CRIVELLO — il meccanismo che attraversa le teorie ===

def _dipolo_firma(dipolo):
    """
    Estrae la firma strutturale di un dipolo.
    La firma è indipendente dal dominio — è la FORMA del dipolo.

    Proprietà strutturali:
    - zero_raggiungibile: il confine si può toccare?
    - zero_tipo: 'numero' | 'principio' | 'operazione'
    - simmetria: i due poli sono simmetrici o uno domina?
    - collasso: lo zero annulla la distinzione o la mantiene?
    """
    zero = dipolo['zero'].lower()

    # Tipo dello zero
    if any(w in zero for w in ['principio', 'equivalenza']):
        zero_tipo = 'principio'
    elif any(w in zero for w in ['=', 'conversione', 'unifica']):
        zero_tipo = 'operazione'
    else:
        zero_tipo = 'numero'

    # Raggiungibilità
    raggiungibile = not any(w in zero for w in [
        'irraggiungibile', '→ ∞', 'non puoi', 'limite'
    ])

    # Collasso: lo zero annulla i poli o li connette?
    collasso = any(w in zero for w in [
        'sono lo stesso', 'inseparabili', 'conversione totale',
        'coincidono', 'complementarità'
    ])

    # Potenziale: il campo descrive qualcosa che esiste SOLO tra i poli?
    campo = dipolo.get('campo', '').lower()
    emergente = any(w in campo for w in [
        'tra', 'tutti', 'tutta', 'esiste', 'possibile'
    ])

    return {
        'nome': dipolo['nome'],
        'zero_tipo': zero_tipo,
        'zero_raggiungibile': raggiungibile,
        'collasso': collasso,
        'emergente': emergente,
    }


def isomorfie():
    """
    Trova dipoli strutturalmente isomorfi tra teorie diverse.

    Non confronta i CONTENUTI (temperatura ≠ velocità)
    ma le FORME (entrambi hanno zero irraggiungibile?
    entrambi hanno collasso? entrambi sono emergenti?).

    Le isomorfie sono le identità nascoste nel potenziale.
    """
    print(f"\n{'='*60}")
    print(f"ISOMORFIE — dipoli con la stessa forma tra teorie diverse")
    print(f"{'='*60}")

    # Calcola firma per ogni dipolo
    tutti = []
    for key, t in TEORIE.items():
        for d in t['dipoli']:
            firma = _dipolo_firma(d)
            firma['teoria'] = t['nome']
            firma['polo_d'] = d['polo_d']
            firma['polo_nd'] = d['polo_nd']
            firma['zero'] = d['zero']
            tutti.append(firma)

    # Raggruppa per firma strutturale
    # La firma = (zero_tipo, raggiungibile, collasso, emergente)
    gruppi = {}
    for f in tutti:
        chiave = (f['zero_tipo'], f['zero_raggiungibile'], f['collasso'], f['emergente'])
        gruppi.setdefault(chiave, []).append(f)

    # Mostra isomorfie (gruppi con dipoli da teorie diverse)
    n_iso = 0
    for chiave, membri in sorted(gruppi.items(), key=lambda x: -len(x[1])):
        teorie_nel_gruppo = set(m['teoria'] for m in membri)
        if len(teorie_nel_gruppo) < 2:
            continue  # stesso tipo ma stessa teoria — non è isomorfismo

        n_iso += 1
        zt, zr, col, em = chiave
        print(f"\n  Isomorfismo #{n_iso}: zero={zt}, raggiungibile={zr}, collasso={col}, emergente={em}")
        print(f"  ({len(membri)} dipoli, {len(teorie_nel_gruppo)} teorie)")
        for m in membri:
            print(f"    [{m['teoria']}] {m['nome']}")
            print(f"      D: {m['polo_d'][:50]}")
            print(f"      ND: {m['polo_nd'][:50]}")
            print(f"      Zero: {m['zero'][:60]}")

    if n_iso == 0:
        print("\n  Nessuna isomorfismo trovato.")

    # Dipoli isolati (forma unica)
    isolati = [g[0] for g in gruppi.values() if len(set(m['teoria'] for m in g)) == 1]
    if isolati:
        print(f"\n  Dipoli con forma unica ({len(isolati)}):")
        for f in isolati:
            print(f"    [{f['teoria']}] {f['nome']} — zero: {f['zero_tipo']}, "
                  f"raggiungi: {f['zero_raggiungibile']}, collasso: {f['collasso']}")

    return gruppi


def attraversa(teoria_key):
    """
    Attraversa una teoria col crivello D-ND completo.

    Per ogni dipolo della teoria:
    1. Firma strutturale
    2. I 5 operatori del domandatore (come tensioni)
    3. Isomorfie con altre teorie
    4. La domanda che emerge

    Non produce risposte — produce domande.
    Le domande sono il potenziale.
    """
    t = TEORIE.get(teoria_key)
    if not t:
        print(f"Teoria '{teoria_key}' non trovata.")
        return

    print(f"\n{'='*60}")
    print(f"ATTRAVERSAMENTO D-ND: {t['nome']}")
    print(f"{'='*60}")

    risultati = []

    for dipolo in t['dipoli']:
        firma = _dipolo_firma(dipolo)

        print(f"\n  --- Dipolo: {dipolo['nome']} ---")
        print(f"  D:    {dipolo['polo_d']}")
        print(f"  ND:   {dipolo['polo_nd']}")
        print(f"  Zero: {dipolo['zero']}")
        print(f"  Firma: tipo={firma['zero_tipo']}, raggiungi={firma['zero_raggiungibile']}, "
              f"collasso={firma['collasso']}, emergente={firma['emergente']}")

        # I 5 operatori come tensioni sul dipolo
        print(f"\n  5 tensioni:")

        tensioni = []

        # DUALE: se D è vero, cosa dice ND?
        t_duale = (f"Se '{dipolo['polo_d']}' è il regime dominante, "
                   f"cosa dice '{dipolo['polo_nd']}' su di esso?")
        tensioni.append(('DUALE', t_duale))

        # CONFINE: cosa c'è allo zero?
        t_confine = (f"Lo zero '{dipolo['zero']}' — è un muro o un passaggio? "
                     f"Cosa esiste ESATTAMENTE al confine?")
        tensioni.append(('CONFINE', t_confine))

        # DOMINIO: questo dipolo esiste in un'altra teoria?
        # Cerca isomorfie
        iso_trovate = []
        for key2, t2 in TEORIE.items():
            if key2 == teoria_key:
                continue
            for d2 in t2['dipoli']:
                f2 = _dipolo_firma(d2)
                if (f2['zero_tipo'] == firma['zero_tipo'] and
                    f2['collasso'] == firma['collasso']):
                    iso_trovate.append(f"[{t2['nome']}] {d2['nome']}")

        if iso_trovate:
            t_dominio = f"Questo dipolo ha la stessa forma di: {', '.join(iso_trovate)}. Sono lo stesso?"
        else:
            t_dominio = f"Questo dipolo non ha isomorfi nelle altre teorie. Perché è unico?"
        tensioni.append(('DOMINIO', t_dominio))

        # ROTTURA: cosa romperebbe questo dipolo?
        if firma['zero_raggiungibile']:
            t_rottura = f"Lo zero è raggiungibile. Cosa succede quando ci arrivi? Il dipolo sopravvive?"
        else:
            t_rottura = f"Lo zero è irraggiungibile. Cosa succederebbe se lo raggiungessi? Il dipolo sopravvive?"
        tensioni.append(('ROTTURA', t_rottura))

        # SCALA: il dipolo vale a tutte le scale?
        t_scala = (f"Questo dipolo ({dipolo['polo_d']} / {dipolo['polo_nd']}) "
                   f"vale alla scala di Planck? Vale a scala cosmologica?")
        tensioni.append(('SCALA', t_scala))

        for nome, tensione in tensioni:
            print(f"    [{nome:8s}] {tensione}")

        risultati.append({
            'dipolo': dipolo['nome'],
            'firma': firma,
            'tensioni': tensioni,
            'isomorfie': iso_trovate,
        })

    # Risultante: la domanda che emerge dalla teoria intera
    print(f"\n  === RISULTANTE ===")
    n_collasso = sum(1 for r in risultati if r['firma']['collasso'])
    n_irragg = sum(1 for r in risultati if not r['firma']['zero_raggiungibile'])
    n_iso = sum(1 for r in risultati if r['isomorfie'])

    print(f"  {len(risultati)} dipoli analizzati")
    print(f"  {n_collasso} con collasso (lo zero annulla la distinzione)")
    print(f"  {n_irragg} con zero irraggiungibile")
    print(f"  {n_iso} con isomorfie in altre teorie")

    if n_collasso > 0 and n_irragg > 0:
        print(f"\n  Tensione: la teoria ha dipoli dove lo zero annulla la distinzione")
        print(f"  E dipoli dove lo zero è irraggiungibile.")
        print(f"  Queste due classi coesistono — perché?")

    return risultati


# === CLI ===

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--mappa':
            mappa_completa()
        elif cmd == '--confronta':
            confronta(*sys.argv[2:])
        elif cmd == '--singolarita':
            singolarita()
        elif cmd == '--isomorfie':
            isomorfie()
        elif cmd == '--attraversa':
            if len(sys.argv) > 2:
                attraversa(sys.argv[2])
            else:
                for key in TEORIE:
                    attraversa(key)
        elif cmd in TEORIE:
            normalizza(cmd)
        else:
            print(f"Uso: python {sys.argv[0]} [teoria|--mappa|--confronta|--singolarita|--isomorfie|--attraversa]")
            print(f"Teorie: {list(TEORIE.keys())}")
    else:
        mappa_completa()
