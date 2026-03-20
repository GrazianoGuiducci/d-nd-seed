# Learnings — Errori che non si ripetono

> Pattern per cristallizzare gli errori risolti.
> Il delta tra il tentativo fallito e la soluzione e' il learning.
> Solo errori RISOLTI — non appunti. Il delta e' il valore.

---

## Il pattern

Quando un errore viene risolto con un approccio diverso dal primo tentativo,
cristallizzare:

1. **Errore**: cosa e' andato storto
2. **Causa**: perche' (la causa reale, non il sintomo)
3. **Soluzione**: come si e' risolto
4. **Regola**: la regola per il futuro (trasferibile)

## Dove salvare

File persistente (`learnings.md` nella memoria del nodo).
Aggiornato a fine sessione o quando un errore significativo viene risolto.

## Trigger

Nella fase di chiusura sessione: "durante la sessione un errore e' stato
risolto con un approccio diverso dal primo tentativo?"
Se si', cristallizzare. Se no, niente da aggiungere.

## Cosa NON e' un learning

- "Cosa e' successo oggi" → va nel session log (eventi, non regole)
- "Cosa ho capito" → va nella memoria (insight, non errore)
- "Cosa devo fare domani" → va nel backlog (task, non learning)

Un learning e' una **regola** che nasce da un **errore risolto**.
Se non c'e' errore, non c'e' learning.
Se l'errore non e' risolto, non c'e' ancora learning.

## Esempio

```
### Bridge exit code 1 senza retry
- Errore: claude -p falliva con exit code 1 e il task veniva marcato failed
- Causa: nessuna classificazione errore, nessun retry
- Soluzione: classifyError() + max 2 retry con backoff
- Regola: classificare l'errore prima di decidere se riprovare
```

---

*L'errore che si ripete e' un errore del sistema, non dell'operatore.*
*L'errore cristallizzato e' un investimento. L'errore dimenticato e' un costo.*
