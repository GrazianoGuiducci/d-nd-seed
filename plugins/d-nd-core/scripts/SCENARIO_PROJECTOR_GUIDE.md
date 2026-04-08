# Scenario Projector — Guida

Proietta scenari da un seme usando la struttura proiettiva D-ND.
Nessuna dipendenza esterna (no numpy). Pure Python.

## Principio

**La struttura contiene già la risposta.**
Non interporre numeri tra la struttura e la decisione.

Ogni tensione è un dipolo D(claim, anti-claim). I dipoli risuonano (assonanza binaria: sì/no).
La traiettoria lagrangiana segue i dipoli a massimo potenziale. I passaggi emergono
dove i cluster di assonanze convergono.

## Uso CLI

```bash
# Traiettoria dal seme locale (cerca seed.json o seme.json)
python scenario_projector.py

# Seme specifico
python scenario_projector.py --seed path/to/seed.json

# Esplorazione autonoma (traiettoria + passaggi + campo)
python scenario_projector.py --explore

# Output strutturato
python scenario_projector.py --json

# Campo dipolare (claim + anti-claim per ogni tensione)
python scenario_projector.py --field

# Cross-check — verifica strutturale del campo
python scenario_projector.py --cross-check

# Cross-check su una singola tensione
python scenario_projector.py --cross-check --tension TENSION_ID

# Strategia — dove concentrare lo sforzo
python scenario_projector.py --strategy

# Piano d'azione — azioni prioritizzate
python scenario_projector.py --action-plan
```

## Uso come libreria

```python
from scenario_projector import ScenarioProjector

# Da file
sp = ScenarioProjector(seed_path='seed.json')

# Da dati
sp = ScenarioProjector(seed_data={
    'direction': 'Esplorare X',
    'tensions': [
        {'id': 'T1', 'claim': 'A implica B'},
        {'id': 'T2', 'claim': 'B ma non C'},
    ]
})

# Esplorazione
result = sp.explore(verbose=False)
# result['trajectory'] — lista passi lagrangiani
# result['passages'] — cluster di convergenza
# result['field'] — stato del campo (dipoli, assonanze, potenziale)

# Componenti singoli
dipoles = sp.dipole_field()
ids, matrix = sp.assonance_matrix()
trajectory = sp.lagrangian_trajectory()

# Cross-check — verifica da più angoli
checks = sp.cross_check()               # tutto il campo
checks = sp.cross_check('TENSION_ID')    # singola tensione
# checks[i] → {id, verdict, is_pillar, support_ratio, contradictions, ...}

# Strategia — dove concentrare lo sforzo
strat = sp.strategy()
# strat['focus'] — cluster di convergenza (dove concentrarsi)
# strat['blind_spots'] — isolati/deboli (cosa potresti perdere)
# strat['risks'] — anti-claim delle tensioni più connesse
# strat['leverage'] — pilastri confermati (dove investire)
# strat['completed'] — saturi (fatto)

# Piano d'azione — azioni prioritizzate
plan = sp.action_plan()
# plan['actions'] — lista di azioni con type/what/why/risk/priority
# plan['summary'] — conteggi per tipo
```

## Formato seme

```json
{
  "direction": "La direzione corrente",
  "tensions": [
    {
      "id": "TENSION_ID",
      "claim": "L'asserzione — può contenere dipoli espliciti (X vs Y, X ma Y)",
      "porta": "novità|confermata|falsificata"
    }
  ]
}
```

Supporta sia chiavi inglesi (`tensions`, `direction`, `gate`, `status`)
che italiane (`tensioni`, `direzione`, `porta`, `stato`).

## Legenda output

| Simbolo | δV | Significato |
|---------|-----|-------------|
| ◆ | acuto | Rilascia potenziale — passo produttivo |
| · | tangente | Neutro — nessuna risonanza nuova |
| ○ | piatto | Dispersione — il dipolo è isolato |

| Potenziale | Significato |
|-----------|-------------|
| alto | Dipolo interno o molte connessioni |
| medio | Alcune connessioni |
| basso | Poche connessioni |
| isolato | Nessuna connessione |
| saturo | Risolto (confermato/falsificato) |

## Cross-check — verifica strutturale

Il cross-check verifica ogni tensione da 4 angoli:

1. **Vicinato**: chi risuona con questo dipolo?
2. **Rimozione**: se tolgo questa tensione, quanto scende la connettività?
3. **Supporto**: quanti vicini sono ad alto potenziale?
4. **Contraddizione**: l'anti-claim risuona con il claim di qualche vicino?

**Verdetti**:

| Verdetto | Significato |
|----------|-------------|
| `confirmed` | Pilastro strutturale con alto supporto |
| `supported` | Supportato dai vicini ma non è un pilastro |
| `contested` | L'anti-claim contraddice almeno un vicino |
| `weak` | Poco supporto, non isolato |
| `unverifiable` | Isolato — nessun vicino per verificare |

Un pilastro (`is_pillar=true`) ha 4+ connessioni e 3+ vicini.
Se lo rimuovi, il campo perde struttura.

## Strategia — dove concentrare lo sforzo

La strategia estrae 5 categorie di insight:

- **Focus**: cluster di convergenza ordinati per densità. Dove le tensioni si addensano c'è energia.
- **Leva**: pilastri confermati. Investire qui propaga nel campo (cascata).
- **Rischi**: anti-claim delle tensioni più connesse. Se cadono queste, il campo si ristruttura.
- **Punti ciechi**: isolati o deboli. Potrebbero nascondere qualcosa di non esplorato.
- **Completati**: saturi. Fatto — liberano potenziale per altro.

## Piano d'azione — dalla proiezione alle azioni

Il piano traduce la strategia in azioni concrete, ciascuna con:

- **what**: cosa fare
- **why**: perché (dalla struttura del campo)
- **risk**: cosa potrebbe andare storto (dall'anti-claim)
- **priority**: dalla posizione nella traiettoria
- **ids**: tensioni coinvolte

4 tipi di azione:

| Tipo | Simbolo | Da dove viene |
|------|---------|---------------|
| `focus` | ▶ | Cluster di convergenza |
| `risk` | ✗ | Contraddizioni strutturali |
| `blind_spot` | ? | Tensioni isolate |
| `leverage` | ✓ | Pilastri confermati |

## Come si auto-evolve

Il proiettore riconosce i dipoli **dentro** i claim ("tensione tra X e Y", "X vs Y", "X ma Y").
Quando trovi claim con dipoli espliciti, il sistema li separa automaticamente.

La soglia di risonanza è adattiva: claim corti (< 150 char) → 1 concetto condiviso basta.
Claim lunghi → servono 2+ concetti. Il sistema si adatta alla densità del campo.

I concetti sono estratti con stemming (riconosce "protezione" e "proteggere" come lo stesso concetto).
L'ID della tensione è incluso nell'analisi (MARKET_FIT porta "market" e "fit" come concetti).
