# Guida Operativa — Domandatore D-ND

> Come usare il domandatore in modo che discrimini davvero.
> Questa guida si migliora ad ogni uso. Quando sara' matura, diventa codice.

## Regola fondamentale

Il domandatore lavora su **tensioni specifiche**, non su brief generici.

Una tensione e' un punto dove la scelta non e' ovvia: "apre col problema o con la promessa?",
"il nome emerge prima o dopo la demo?", "esce con un tool o con una comprensione?"

Se gli dai un brief lungo, ripete l'input nei 5 operatori senza discriminare nulla.

## Pattern d'uso

1. **Identifica le tensioni** — prima di lanciare il tool, chiediti: quali sono i punti
   dove devo scegliere e non e' ovvio? Ogni punto e' una tensione.

2. **Una tensione per run** — `--ask "L'articolo apre col problema o con la promessa?"`
   Breve, binaria (o apparentemente binaria — il CONFINE trova il terzo).

3. **Sequenza vincolante** — la risultante di ogni tensione vincola la successiva.
   Prima: come apro? → Risultante: apri con un fatto.
   Poi: quando nomino D-ND? → Vincolo: dopo il fatto, non prima.
   Poi: cosa esce con il lettore? → Vincolo: coerente con i primi due.

4. **Il CONFINE e' quasi sempre il piu' produttivo** — il terzo incluso rompe
   la falsa dicotomia. "Problema o promessa?" → "Nessuno dei due: un fatto."
   "Framework o singola domanda?" → "Una domanda che e' gia' un framework."

5. **Rispondi a tutti e 5 gli operatori** — non solo al CONFINE. Il DUALE verifica
   robustezza, la ROTTURA trova i punti deboli, la SCALA testa i limiti,
   il DOMINIO verifica se la scelta e' tua.

## Anti-pattern

- Brief generico di 5 righe → il tool diventa eco, non discriminatore
- Domanda retorica ("dovrei scrivere un buon articolo?") → niente da discriminare
- Saltare le risposte → le domande senza risposte sono rumore

## Evoluzione

Questa guida e' il seme del domandatore v2:
- Scissione automatica dell'input in tensioni
- Domande gia' mirate per operatore (non la stessa frase ripetuta 5 volte)
- Sequenza suggerita basata sulle dipendenze tra tensioni

Pattern generalizzabile: impara a usare il tool → formalizza la guida → la guida diventa il tool.
