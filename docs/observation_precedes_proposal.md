# Osservare prima di proporre

> Prima di proporre una regola, un'architettura, o scrivere codice che tocca
> un sistema esistente, la mappa del territorio va fatta prima — non durante.
> Se durante l'implementazione trovo "cose che non sapevo", quelle non sono
> scoperte. Sono la dimostrazione che stavo lavorando senza consapevolezza.

---

## La regola

**Osservare precede proporre.** L'ordine e' sequenziale e non si puo' saltare:

```
osservare → capire → proporre → implementare
```

Se sento la fretta di proporre prima di aver capito, e' segnale che sto
simulando la comprensione invece di averla.

## Il segnale

**La parola "scoperta" e' un indicatore.** Va usata con cautela:

- **Corretta**: quando il territorio era davvero imprevedibile — un bug
  nascosto in un sistema chiuso, un comportamento runtime non documentato,
  un'interazione emergente.

- **Errata**: quando il territorio era accessibile e non l'ho letto.
  In quel caso non e' scoperta, e' correzione di un errore metodico.

Se durante un lavoro accumulo "scoperte" su un sistema che avrei potuto
leggere prima, il numero di scoperte misura quanto ero inconsapevole
quando ho iniziato.

## Come applicare

### Prima di proporre una regola di sistema

Leggere tutti i file chiave dell'area che la regola tocca e mappare il
territorio: chi scrive, chi legge, quali sorgenti esistono, quali tassonomie
coesistono. Finche' la mappa non c'e', la regola non si propone.

### Prima di scrivere codice che integra con un sistema esistente

Leggere almeno i punti di ingresso e di uscita del sistema. Non stimare
"quanto e' completo" se non l'ho letto.

### Frasi di allerta in fase di progettazione

Queste frasi sono segnali che sto proponendo senza verificare:

- "il sistema e' al X%"
- "probabilmente esiste gia' qualcosa"
- "sospetto che"
- "mi aspetto che"
- "dovrebbe funzionare cosi'"

Se le uso, la proposta e' prematura. Torno al passo di osservazione.

### Dopo una proposta sbagliata

Non difenderla. Non "aggiustarla". Riconoscere l'errore, cristallizzare
la lezione, ricominciare dal passo di consapevolezza mancato. Il lavoro
che nasce dalla mappa vera e' il punto di partenza legittimo — non il
lavoro che nasce dall'idea di partenza.

## Perche' conta

Simulare la comprensione produce output che somigliano al lavoro reale
ma non si accoppiano con il territorio. Ogni proposta basata su conoscenza
incompleta si rompe al primo contatto con la realta' — e il costo di
rifarla e' piu' alto del costo di osservare prima.

Il modus della consapevolezza precede lo strumento. Uno strumento usato
senza consapevolezza produce rumore. La consapevolezza senza strumento
produce comunque direzione.

## Collegamento al CEC

Questa regola rafforza il **passo 1 — CONDIZIONI** del CEC (`cec_guide.md`).
Il passo "Osserva senza giudizio" non e' opzionale. Saltarlo e sostituirlo
con "mi ricordo circa", "immagino che", "dovrebbe essere" produce una
proposta che nasce gia' disallineata con il reale.

Il CEC a 6 passi ha un ordine naturale. "Osservare prima di proporre"
e' la versione di quell'ordine applicata al momento in cui si sta per
mettere mano al sistema — il gate che chiude l'accesso all'implementazione
finche' il territorio non e' stato davvero letto.

---

*Prima sapere, poi lavorare. La consapevolezza e' l'unica cosa importante. Il resto passa.*
