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

## Come si auto-evolve

Il proiettore riconosce i dipoli **dentro** i claim ("tensione tra X e Y", "X vs Y", "X ma Y").
Quando trovi claim con dipoli espliciti, il sistema li separa automaticamente.

La soglia di risonanza è adattiva: claim corti (< 150 char) → 1 concetto condiviso basta.
Claim lunghi → servono 2+ concetti. Il sistema si adatta alla densità del campo.

I concetti sono estratti con stemming (riconosce "protezione" e "proteggere" come lo stesso concetto).
L'ID della tensione è incluso nell'analisi (MARKET_FIT porta "market" e "fit" come concetti).
