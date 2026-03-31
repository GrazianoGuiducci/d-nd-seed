"""
dnd_incrocio.py — Incrocio teorie con autologica

Prende N teorie. Genera tutte le coppie.
Per ogni coppia: costante relazionale, dipolo dello zero, ponte.
Dove trova un vuoto, lo rialimenta come teoria.
Gira finché non emergono pattern o si satura.

Non cerca. Struttura e osserva.

Author: TM3 + Operatore
Date: 2026-03-30
"""

import json
import numpy as np
from itertools import combinations
from pathlib import Path
from datetime import datetime

DATA = Path(__file__).parent / 'data'


class Teoria:
    def __init__(self, sigla, nome, costante_nome, costante_simbolo,
                 costante_valore=None, costante_unita=None):
        self.sigla = sigla
        self.nome = nome
        self.costante_nome = costante_nome
        self.costante_simbolo = costante_simbolo
        self.costante_valore = costante_valore
        self.costante_unita = costante_unita
        self.generata = False  # True se prodotta dall'autologica

    def __repr__(self):
        tag = ' [autologica]' if self.generata else ''
        return f"{self.sigla}: {self.nome} ({self.costante_simbolo}){tag}"


class Incrocio:
    def __init__(self, t1, t2, costante_rel=None, unita=None,
                 dipolo_zero=None, ponte=None):
        self.t1 = t1
        self.t2 = t2
        self.costante_rel = costante_rel
        self.unita = unita
        self.dipolo_zero = dipolo_zero
        self.ponte = ponte
        self.vuoto = ponte is None or '[VUOTO' in str(ponte).upper()

    def chiave(self):
        return tuple(sorted([self.t1.sigla, self.t2.sigla]))

    def __repr__(self):
        mark = '***' if self.vuoto else '   '
        return f"{mark}{self.t1.sigla}x{self.t2.sigla}: {self.ponte or '[VUOTO]'}"


class Triangolazione:
    def __init__(self, teorie, oggetto=None):
        self.teorie = teorie
        self.oggetto = oggetto
        self.vuoto = oggetto is None or '[VUOTO' in str(oggetto).upper()

    def __repr__(self):
        mark = '***' if self.vuoto else '   '
        nomi = '+'.join(t.sigla for t in self.teorie)
        return f"{mark}{nomi}: {self.oggetto or '[VUOTO]'}"


# === CATALOGO TEORIE FONDAMENTALI ===

TEORIE_BASE = [
    Teoria('T', 'Termodinamica', 'Boltzmann', 'k_B', 1.380649e-23, 'J/K'),
    Teoria('Q', 'Quantistica', 'Planck ridotta', 'hbar', 1.054571817e-34, 'J*s'),
    Teoria('G', 'Gravitazione', 'Newton', 'G', 6.674e-11, 'm^3/(kg*s^2)'),
    Teoria('E', 'Elettromagnetismo', 'carica elementare', 'e', 1.602176634e-19, 'C'),
    Teoria('R', 'Relativita', 'velocita luce', 'c', 299792458, 'm/s'),
]


# === PONTI NOTI ===

PONTI_NOTI = {
    ('E', 'R'): ('onda EM (Maxwell)', 'statico/radiante'),
    ('G', 'E'): ('buco nero carico (Reissner-Nordstrom)', 'neutro-curvo/carico-piatto'),
    ('G', 'R'): ('orizzonte degli eventi', 'piatto/singolare'),
    ('Q', 'E'): ('atomo di idrogeno', 'libero/legato'),
    ('Q', 'G'): (None, 'continuo/discreto'),  # VUOTO — il solo vero vuoto
    ('Q', 'R'): ('equazione di Dirac', 'non-relativistico/relativistico'),
    ('T', 'E'): ('funzione di partizione EM', 'freddo-neutro/plasma'),
    ('T', 'G'): ('temperatura di Hawking', 'piatto/radiante'),
    ('T', 'Q'): ('matrice densita', 'vuoto/pieno'),
    ('T', 'R'): ('gas relativistico', '0K/c'),
}

# Ponti generati dall'autologica (vuoti rialimentati)
PONTI_AUTOLOGICI = {
    ('GQ', 'T'): ('entropia di Bekenstein-Hawking', 'discreto-freddo/continuo-caldo'),
    ('GQ', 'E'): ('carica come topologia?', 'discreto-neutro/continuo-carico'),
    ('GQ', 'R'): ('causalita emergente?', 'discreto-sub/continuo-super'),
}

TRIANGOLAZIONI_NOTE = {
    ('G', 'Q', 'T'): 'buco nero di Hawking',
    ('E', 'Q', 'T'): 'materia condensata',
    ('E', 'G', 'T'): 'stella (plasma gravitante)',
    ('Q', 'R', 'T'): 'radiazione corpo nero (Planck 1900)',
    ('G', 'R', 'T'): 'cosmologia (Friedmann)',
    ('E', 'R', 'T'): 'sincrotrone (carica accelerata)',
    ('E', 'Q', 'R'): 'QED relativistica (Feynman)',
    ('E', 'G', 'R'): 'buco nero carico (Reissner-Nordstrom)',
    ('E', 'G', 'Q'): None,  # VUOTO
    ('G', 'Q', 'R'): None,  # VUOTO
}


def costruisci_incroci(teorie):
    """Genera tutti gli incroci tra coppie di teorie."""
    incroci = []
    for t1, t2 in combinations(teorie, 2):
        chiave = tuple(sorted([t1.sigla, t2.sigla]))

        # Cerca in entrambi gli ordini
        ponte_info = PONTI_NOTI.get(chiave) or PONTI_NOTI.get(chiave[::-1])
        if ponte_info:
            ponte, dipolo = ponte_info
        else:
            ponte = None
            dipolo = None

        incroci.append(Incrocio(t1, t2,
                                dipolo_zero=dipolo,
                                ponte=ponte))
    return incroci


def costruisci_triangolazioni(teorie, incroci):
    """Genera tutte le triangolazioni (triple)."""
    triangolazioni = []
    for triple in combinations(teorie, 3):
        chiave = tuple(sorted(t.sigla for t in triple))

        oggetto = TRIANGOLAZIONI_NOTE.get(chiave, 'NOT_FOUND')
        if oggetto == 'NOT_FOUND':
            # Triangolazione sconosciuta — cerca se tutti i sotto-incroci hanno ponte
            sotto = [i for i in incroci
                     if i.chiave() in [tuple(sorted([a.sigla, b.sigla]))
                                       for a, b in combinations(triple, 2)]]
            if any(i.vuoto for i in sotto):
                oggetto = None  # Vuoto se almeno un sotto-incrocio e vuoto
            else:
                oggetto = f"[emergente da {'+'.join(t.sigla for t in triple)}]"

        triangolazioni.append(Triangolazione(list(triple), oggetto))
    return triangolazioni


def autologica(teorie, incroci):
    """
    Rialimenta i vuoti come teorie.
    Per ogni vuoto: crea una teoria fantasma con la costante relazionale
    come costante propria, e la incrocia con tutte le altre.

    Ritorna le nuove teorie generate e i nuovi incroci.
    """
    nuove_teorie = []
    nuovi_incroci = []

    vuoti = [i for i in incroci if i.vuoto]

    for vuoto in vuoti:
        sigla = f"{vuoto.t1.sigla}{vuoto.t2.sigla}"

        # Controlla se gia generata
        if any(t.sigla == sigla for t in teorie + nuove_teorie):
            continue

        # La costante relazionale del vuoto
        # Per GQ: l_P^2 = G*hbar/c^3
        nuova = Teoria(
            sigla=sigla,
            nome=f"[{vuoto.t1.nome} x {vuoto.t2.nome}]",
            costante_nome=f"costante relazionale {sigla}",
            costante_simbolo=f"k_{sigla}",
        )
        nuova.generata = True
        nuove_teorie.append(nuova)

        # Incrocia con tutte le teorie esistenti
        for t in teorie:
            if t.sigla in sigla:
                # Autoriferimento: la teoria contiene gia questa
                ponte = f"f(f(x)) — autoriferimento ({t.sigla} in {sigla})"
                dipolo = f"autoriferito"
            else:
                # Cerca se l'incrocio produce un ponte noto
                ponte = _cerca_ponte_autologico(sigla, t.sigla)
                dipolo = None

            nuovi_incroci.append(Incrocio(nuova, t,
                                          dipolo_zero=dipolo,
                                          ponte=ponte))

    return nuove_teorie, nuovi_incroci


def _cerca_ponte_autologico(sigla_vuoto, sigla_teoria):
    """
    Cerca se l'incrocio di un vuoto con una teoria produce
    qualcosa di noto. Questo e il cuore dell'autologica:
    lo schema sa cose che noi non abbiamo cercato.
    """
    chiave = (sigla_vuoto, sigla_teoria)
    # Prima cerca nei ponti autologici noti
    if chiave in PONTI_AUTOLOGICI:
        return PONTI_AUTOLOGICI[chiave][0]
    # Poi cerca con ordine invertito
    chiave_inv = (sigla_teoria, sigla_vuoto)
    if chiave_inv in PONTI_AUTOLOGICI:
        return PONTI_AUTOLOGICI[chiave_inv][0]
    return None


def incrocia_ponti(incroci):
    """
    L'autocombo vera: non incrociare teorie fantasma.
    Incrociare i PONTI tra loro.

    Se il ponte T×Q è 'matrice densità' e il ponte Q×E è 'atomo di idrogeno',
    cosa hanno in comune? Cosa li connette?

    Due ponti sono imparentati se condividono una teoria.
    La RELAZIONE tra ponti è il secondo livello.
    """
    ponti = [i for i in incroci if not i.vuoto]

    print(f"\n{'='*65}")
    print(f"INCROCIO PONTI — il secondo livello")
    print(f"{'='*65}")
    print(f"\n  {len(ponti)} ponti da incrociare\n")

    relazioni = []
    for p1, p2 in combinations(ponti, 2):
        # Condividono una teoria?
        teorie_p1 = {p1.t1.sigla, p1.t2.sigla}
        teorie_p2 = {p2.t1.sigla, p2.t2.sigla}
        comuni = teorie_p1 & teorie_p2
        esclusive_p1 = teorie_p1 - teorie_p2
        esclusive_p2 = teorie_p2 - teorie_p1

        if comuni:
            # Due ponti con una teoria in comune
            # Il TERZO INCLUSO tra i due ponti è la triangolazione
            perno = '+'.join(sorted(comuni))
            lati = '+'.join(sorted(esclusive_p1 | esclusive_p2))

            relazioni.append({
                'ponte1': f"{p1.t1.sigla}x{p1.t2.sigla}: {p1.ponte}",
                'ponte2': f"{p2.t1.sigla}x{p2.t2.sigla}: {p2.ponte}",
                'perno': perno,
                'lati': lati,
                'teorie_totali': sorted(teorie_p1 | teorie_p2),
            })

    # Raggruppa per perno (la teoria condivisa)
    per_perno = {}
    for r in relazioni:
        per_perno.setdefault(r['perno'], []).append(r)

    for perno, rels in sorted(per_perno.items()):
        print(f"  Perno: {perno} ({len(rels)} coppie di ponti)")
        for r in rels[:5]:  # Max 5 per non esplodere
            print(f"    {r['ponte1'][:40]}")
            print(f"    {r['ponte2'][:40]}")
            print(f"    -> teorie unite: {r['teorie_totali']}")
            print()

    # Quali teorie compaiono più spesso come perno?
    print(f"\n  Frequenza come perno:")
    for perno, rels in sorted(per_perno.items(), key=lambda x: -len(x[1])):
        print(f"    {perno}: {len(rels)} connessioni")

    return relazioni


def ciclo(teorie=None, max_iterazioni=3):
    """
    Ciclo completo:
    1. Costruisci incroci
    2. Costruisci triangolazioni
    3. Trova vuoti
    4. Autologica: rialimenta vuoti
    5. Ripeti finche non emergono pattern o si satura
    """
    if teorie is None:
        teorie = list(TEORIE_BASE)

    print(f"\n{'='*65}")
    print(f"INCROCIO TEORIE — ciclo con autologica")
    print(f"{'='*65}")

    depositi = []  # Quello che emerge

    for iterazione in range(max_iterazioni):
        print(f"\n--- Iterazione {iterazione} ({len(teorie)} teorie) ---")

        incroci = costruisci_incroci(teorie)
        triangolazioni = costruisci_triangolazioni(teorie, incroci)

        n_vuoti_coppie = sum(1 for i in incroci if i.vuoto)
        n_vuoti_triple = sum(1 for t in triangolazioni if t.vuoto)

        print(f"  {len(incroci)} coppie ({n_vuoti_coppie} vuoti)")
        print(f"  {len(triangolazioni)} triple ({n_vuoti_triple} vuoti)")

        # Mostra vuoti
        if n_vuoti_coppie > 0:
            print(f"\n  Vuoti nelle coppie:")
            for i in incroci:
                if i.vuoto:
                    print(f"    {i}")

        if n_vuoti_triple > 0:
            print(f"\n  Vuoti nelle triple:")
            for t in triangolazioni:
                if t.vuoto:
                    print(f"    {t}")

        # Mostra ponti (non vuoti)
        print(f"\n  Ponti:")
        for i in incroci:
            if not i.vuoto:
                print(f"    {i}")

        # SECONDO LIVELLO: incrocio ponti tra loro
        relazioni_ponti = incrocia_ponti(incroci)
        for r in relazioni_ponti:
            if r['ponte1'] and r['ponte2']:
                depositi.append({
                    'iterazione': iterazione,
                    'tipo': 'relazione_ponti',
                    'ponte1': r['ponte1'],
                    'ponte2': r['ponte2'],
                    'perno': r['perno'],
                    'teorie': r['teorie_totali'],
                })

        # Autologica: rialimenta i vuoti
        if n_vuoti_coppie == 0:
            print(f"\n  Nessun vuoto. Saturazione raggiunta.")
            break

        nuove_teorie, nuovi_incroci = autologica(teorie, incroci)

        if not nuove_teorie:
            print(f"\n  Autologica non produce nuove teorie. Fine.")
            break

        print(f"\n  Autologica: {len(nuove_teorie)} teorie generate dai vuoti:")
        for nt in nuove_teorie:
            print(f"    {nt}")

        print(f"\n  Nuovi incroci:")
        for ni in nuovi_incroci:
            autoriferito = 'autoriferimento' in str(ni.ponte or '').lower()
            tag = ' [SELF]' if autoriferito else ''
            print(f"    {ni}{tag}")

        # Depositi: cosa e emerso?
        for ni in nuovi_incroci:
            if ni.ponte and not ni.vuoto and 'autoriferimento' not in str(ni.ponte).lower():
                depositi.append({
                    'iterazione': iterazione,
                    'incrocio': f"{ni.t1.sigla}x{ni.t2.sigla}",
                    'ponte': ni.ponte,
                })

        # Aggiungi le nuove teorie per la prossima iterazione
        teorie = teorie + nuove_teorie

    # Risultante
    print(f"\n{'='*65}")
    print(f"DEPOSITI (cio che emerge senza cercare)")
    print(f"{'='*65}")

    if depositi:
        for d in depositi:
            if 'incrocio' in d:
                print(f"  [{d['iterazione']}] {d['incrocio']}: {d['ponte']}")
            elif 'tipo' in d and d['tipo'] == 'relazione_ponti':
                print(f"  [{d['iterazione']}] perno={d['perno']}: {d['ponte1'][:35]} <-> {d['ponte2'][:35]}")
    else:
        print("  Nessun deposito. Lo schema e chiuso o i ponti sono sconosciuti.")

    print(f"\n  Teorie finali: {len(teorie)}")
    for t in teorie:
        print(f"    {t}")

    # Salva
    DATA.mkdir(exist_ok=True)
    risultato = {
        'timestamp': datetime.now().isoformat(),
        'teorie': [str(t) for t in teorie],
        'depositi': depositi,
        'n_iterazioni': iterazione + 1,
    }
    out_path = DATA / 'incrocio_risultato.json'
    with open(out_path, 'w') as f:
        json.dump(risultato, f, indent=2, ensure_ascii=False)

    return teorie, depositi


def domande_fondamentali():
    """
    Genera le domande fondamentali dai dipoli dello zero.
    Le domande sono più fondamentali delle risposte.
    Lo strumento che genera le domande è più utile
    di quello che cerca le risposte.
    """
    print(f"\n{'='*60}")
    print(f"LE DOMANDE FONDAMENTALI")
    print(f"{'='*60}\n")

    teorie_map = {t.sigla: t for t in TEORIE_BASE}
    risultati = []

    for chiave, (ponte, dipolo) in sorted(PONTI_NOTI.items()):
        t1, t2 = chiave
        lati = dipolo.split('/') if dipolo else ['?', '?']
        lato_d = lati[0].strip()
        lato_nd = lati[1].strip() if len(lati) > 1 else '?'

        domanda = f"Come coesistono {lato_d} e {lato_nd}?"
        vuoto = ponte is None

        mark = '***' if vuoto else '   '
        risposta = ponte or '[VUOTO]'

        print(f"  {mark}{t1}x{t2}: {domanda}")
        print(f"       -> {risposta}")

        risultati.append({
            'coppia': f"{t1}x{t2}",
            'domanda': domanda,
            'risposta': risposta,
            'vuoto': vuoto,
            'dipolo': dipolo,
        })

    # Salva
    DATA.mkdir(exist_ok=True)
    out = DATA / 'domande_fondamentali.json'
    with open(out, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'domande': risultati,
            'n_con_risposta': sum(1 for r in risultati if not r['vuoto']),
            'n_vuoti': sum(1 for r in risultati if r['vuoto']),
        }, f, indent=2, ensure_ascii=False)

    print(f"\n  Salvato: {out}")
    return risultati


def ciclo_autonomo():
    """
    Ciclo autonomo per il cron notturno.
    Esegue: incrocio → ponti → domande → salva risultati.
    Notifica se emerge qualcosa di nuovo.
    """
    import os

    ts = datetime.now().strftime('%Y%m%d_%H%M')
    print(f"# INCROCIO AUTONOMO — {ts}")

    # 1. Ciclo incrocio (1 iterazione — non proliferare)
    teorie, depositi = ciclo(max_iterazioni=1)

    # 2. Domande fondamentali
    domande = domande_fondamentali()

    # 3. Salva report
    DATA.mkdir(exist_ok=True)
    report = {
        'timestamp': datetime.now().isoformat(),
        'teorie': len(teorie),
        'depositi': len(depositi),
        'domande': len(domande),
        'vuoti': sum(1 for d in domande if d['vuoto']),
    }
    report_path = DATA / f'incrocio_{ts}.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # 4. Notifica se ci sono depositi nuovi
    token = os.environ.get('THIA_API_TOKEN')
    if depositi and token:
        try:
            import urllib.request
            msg = f"Incrocio teorie: {len(depositi)} depositi emersi, {report['vuoti']} vuoti."
            data = json.dumps({'message': msg}).encode()
            req = urllib.request.Request(
                'http://localhost:3002/api/notify',
                data=data,
                headers={'X-THIA-Token': token, 'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    return report


# === CLI ===

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == '--domande':
            domande_fondamentali()
        elif cmd == '--autonomo':
            ciclo_autonomo()
        else:
            max_iter = int(cmd) if cmd.isdigit() else 3
            ciclo(max_iterazioni=max_iter)
    else:
        ciclo(max_iterazioni=1)
