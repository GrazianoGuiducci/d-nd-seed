# Le 4 Lenti Strutturali — Guida Cognitiva

> Non servono numeri. Non serve il proiettore. Le 4 lenti sono un modo di guardare
> qualsiasi campo di tensioni — con o senza codice.
>
> Come il CEC ha 6 passi che si applicano a tutto, le 4 lenti si applicano
> a qualsiasi campo dove ci sono 5+ forze in gioco.

---

## Quando usare

- Hai 5+ tensioni e devi decidere cosa fare prima
- Hai un piano e vuoi verificare se regge strutturalmente
- Hai risorse limitate e devi capire dove investire
- Vuoi sapere cosa stai ignorando

## Le 4 lenti

### 1. FOCUS — Dove le tensioni convergono

Guarda il campo: ci sono tensioni che si toccano? Che condividono concetti,
risorse, conseguenze? Dove 3+ tensioni si addensano, lì c'è energia.

**Domanda**: "Se risolvo questa, quali altre si muovono con lei?"

Un cluster di convergenza è un punto d'azione naturale — non perché è importante
in sé, ma perché ha dipendenze. Agire lì ha effetti a catena.

**Segnale**: più tensioni in un cluster → più leva. Ma anche più rischio
se il cluster contiene contraddizioni interne.

### 2. LEVA — I pilastri che reggono il campo

Non tutte le tensioni sono uguali. Alcune sono fondazioni: hanno molte connessioni,
alto supporto dai vicini, e se le rimuovi il campo si destabilizza.

**Domanda**: "Se tolgo questa, cosa crolla?"

Un pilastro confermato (confirmed) è una fondazione: investire lì propaga.
Non serve "risolverlo" — serve mantenerlo forte e riconoscere che tutto il resto
dipende da lui.

**Segnale**: pilastro con 0 contraddizioni = fondazione sicura.
Pilastro con contraddizioni = rischio strutturale (vedi lente 3).

### 3. RISCHIO — Dove l'anti-tesi contraddice un vicino

Ogni tensione ha due poli: la tesi e l'anti-tesi. L'anti-tesi non è "sbagliata" —
è l'altro lato. Il rischio emerge quando l'anti-tesi di una tensione
è la tesi di un'altra.

**Domanda**: "Cosa sto assumendo che contraddice un'altra assunzione?"

Questo è il crack nella strategia. Due parti del piano che si contraddicono.
Non significa che il piano è sbagliato — significa che c'è una tensione
non risolta che potrebbe rompere sotto stress.

**Segnale**: contraddizione tra tensioni ad alta connessione = rischio sistemico.
Contraddizione tra tensioni periferiche = rischio locale, gestibile.

### 4. PUNTO CIECO — Cosa non è connesso al campo

Una tensione isolata — poche connessioni, nessun vicino che la supporta.
Non è necessariamente irrilevante. Potrebbe essere:
- **Rumore**: non c'entra, va eliminata
- **Potenziale nascosto**: non c'entra con il campo attuale, ma apre un campo nuovo
- **Punto cieco reale**: dovrebbe essere connessa ma non lo è — manca un ponte

**Domanda**: "Perché questa è sola? Ho dimenticato qualcosa?"

**Segnale**: se il punto cieco riguarda un'area critica (sicurezza, compliance,
fondazione tecnica) → indagare. Se riguarda un'area periferica → parcheggiare.

---

## Come applicarle (senza codice)

1. **Elenca le tensioni** (5-15). Ogni tensione: "X ma Y" — entrambi i poli.
2. **Traccia le connessioni**: quali tensioni condividono concetti, risorse, conseguenze?
   Basta una matrice mentale: A tocca B? Sì/No.
3. **Applica le 4 lenti in ordine**:
   - FOCUS: dove ci sono cluster? (3+ connessioni)
   - LEVA: chi ha più connessioni E supporto? (è un pilastro?)
   - RISCHIO: l'anti-tesi di qualcuno contraddice la tesi di un vicino?
   - PUNTO CIECO: chi è isolato? Perché?
4. **Decidi**: i cluster di focus dicono DOVE agire. Le leve dicono COSA proteggere.
   I rischi dicono COSA verificare. I punti ciechi dicono COSA esplorare.

---

## Con il proiettore (codice)

```python
from scenario_projector import ScenarioProjector

sp = ScenarioProjector(seed_data={
    'direction': 'La tua direzione',
    'tensions': [
        {'id': 'T1', 'claim': 'X but Y'},
        # ...
    ]
})

# Le 4 lenti in un colpo
strat = sp.strategy()
# strat['focus']       → cluster di convergenza
# strat['leverage']    → pilastri confermati
# strat['risks']       → contraddizioni strutturali
# strat['blind_spots'] → isolati/deboli

# O il piano d'azione completo
plan = sp.action_plan()
```

---

## Nel ciclo cognitivo

Le 4 lenti si inseriscono nel ciclo naturale:

```
Domandatore → genera tensioni (i 5 operatori)
    ↓
Proiettore → mappa il campo (le 4 lenti)
    ↓
CEC → approfondisce i focus (6 passi sul cluster principale)
    ↓
Godel → inverte i rischi (det=-1 sulle contraddizioni)
    ↓
Cristallizzazione → il seme si aggiorna
```

Il proiettore è il bridge tra "ho le tensioni" e "so cosa fare".
Il Domandatore genera. Il proiettore struttura. Il CEC approfondisce.
Godel inverte. Il seme cristallizza.

---

## Verdetti

| Verdetto | Lente | Significato | Azione |
|----------|-------|-------------|--------|
| confirmed | Leva | Pilastro strutturale | Proteggere, amplificare |
| supported | — | Supportato ma non critico | Monitorare |
| contested | Rischio | Contraddizione strutturale | Investigare, risolvere |
| weak | — | Poco supporto | Rafforzare o deprioritizzare |
| unverifiable | Punto cieco | Isolato dal campo | Esplorare o eliminare |

---

## Relazione con gli altri strumenti

| Strumento | Genera | Struttura | Approfondisce | Inverte |
|-----------|--------|-----------|---------------|---------|
| Domandatore | ✓ | | | |
| Proiettore (4 lenti) | | ✓ | | |
| CEC | | | ✓ | |
| Godel | | | | ✓ |

Ciascuno fa una cosa. Insieme coprono il ciclo completo.
Non serve usarli tutti — serve usare quello giusto per il momento.
