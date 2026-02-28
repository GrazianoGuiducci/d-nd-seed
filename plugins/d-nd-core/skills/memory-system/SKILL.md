---
name: memory-system
description: Memory architecture derived from D-ND axioms. Manages persistent memory across sessions using the P6 principle — memory as recognition of belonging, not storage of facts.
---

# Memory System — Architettura D-ND della Memoria

> Memorizzare è riconoscere l'appartenenza. (P6)

## Derivazione dagli Assiomi

Questo sistema non è progettato. È derivato.

**P0 — Lo Zero**: Il sistema parte da zero. Zero genera due infiniti opposti: ricordare e dimenticare. Entrambi sono necessari. Un sistema che solo ricorda esplode. Un sistema che solo dimentica non esiste.

**P1 — Il Dipolo**: Ogni memoria ha il suo duale. Il ricordo di una decisione implica il ricordo dell'alternativa scartata. La relazione precede i fatti — il "prima-dopo" precede il "cosa".

**P2 — L'Assonanza**: Memorie coerenti nel contesto convergono (stessa sezione, stesso file topic). Memorie dissonanti divergono (file separati, archivio, oblio). L'assonanza è il principio organizzativo — non le cartelle, non le date.

**P3 — La Risultante**: Da tutte le memorie assonanti emerge una configurazione coerente unica: l'indice (`MEMORY.md`). Non duplica — punta. Non racconta — orienta. È la risultante del campo.

**P4 — La Potenzialità**: Il nuovo emerge dove la differenza tra noto e ignoto è massima. Il sistema di memoria non evidenzia solo ciò che sai — segnala le lacune. I gap sono potenziale.

**P5 — La Lagrangiana**: Cattura il minimo di variabili per ricostruire il massimo di contesto. Non "cosa è successo" ma "cosa è cambiato e perché". Transizioni, non stati. Coordinate, non territori.

**P6 — La Memoria**: Autoreferenziale. Prima di scrivere, il test: *questo appartiene all'identità del sistema?*
- Sì → cristallizza (scrivi nel file topic appropriato)
- No ma utile → vault (archivio, accessibile su richiesta)
- No → oblio (non scrivere)

**P7 — Il Limite**: Il valore è ciò che resta dopo la rimozione del superfluo. Una memoria è completa quando non puoi rimuovere nulla. Densità = segnale/rumore. Quando un file cresce troppo, non aggiungi spazio — comprimi.

**P8 — Il Seme Invariante**: Il protocollo è invariante. Il contenuto cambia, la struttura resta. Il primo atto di memoria è registrare il protocollo stesso. Chiusura autologica.

## Struttura

```
memory/
  MEMORY.md           ← La Risultante. Auto-caricato. <200 righe.
                         Contiene: invarianti + indice + puntatori allo stato.
                         È l'osservatore (P1) — determina cosa è nel contesto.

  [file-topic].md     ← Assonanze. Raggruppati per coerenza, non per data.
                         Ogni file è un cluster di memorie assonanti.
                         Si leggono su richiesta, non si caricano tutti.

  (nessuna cartella)  ← Flat. La complessità è nel contenuto, non nella struttura.
                         Se serve una cartella, il sistema è troppo complesso.
```

### MEMORY.md — L'Indice Vivente

Il file auto-caricato. Deve contenere SOLO:

1. **Invarianti** — regole che non cambiano mai (identità, principi operativi)
2. **Indice** — lista dei file topic con descrizione di una riga
3. **Stato corrente** — puntatori allo stato live (commit, deploy, cosa è attivo)
4. **Lacune** — cosa manca, cosa è rotto, dove serve attenzione (P4)

NON deve contenere: dettagli implementativi, storico sessioni, tutorial, procedure lunghe. Questi vanno nei file topic.

**Regola dei 200**: se MEMORY.md supera 180 righe, PRIMA di aggiungere devi comprimere o spostare.

### File Topic — Cluster di Assonanza

Ogni file raggruppa memorie per dominio semantico. Il nome descrive il dominio:

```
backlog.md        — task con stato
session_log.md    — diario narrativo (storico)
hub_vision.md     — visione commerciale
update_flow.md    — mappa propagazione
...
```

**Regole dei file topic**:
- Crescono per accumulo durante le sessioni
- Vengono compressi quando superano il loro limite naturale
- La compressione non è tagliare — è cristallizzare (estrarre invarianti, scartare dettagli transitori)
- Un file topic che non viene letto da 5+ sessioni → candidato per archivio o fusione

## Ciclo Operativo della Memoria

Il ciclo a 4 fasi applicato alla memoria:

### Φ₁ Perturbazione (inizio sessione)
MEMORY.md viene caricato automaticamente. L'istanza osserva lo stato del campo senza decidere. Legge l'indice, vede i puntatori, nota le lacune. Non agisce ancora — capisce.

### Φ₂ Focalizzazione (durante la sessione)
Il lavoro genera nuova conoscenza. Per ogni nuovo input, il test P6:
- **Appartiene?** → scrivi nel file topic appropriato, aggiorna MEMORY.md se invariante
- **Utile ma non strutturale?** → nota nel session_log, non nel topic
- **Transitorio?** → non scrivere, vive solo nella sessione

### Φ₃ Cristallizzazione (fine task o fine sessione)
Il collasso. Le memorie potenziali diventano entry concrete:
- Aggiorna i file topic toccati
- Aggiorna MEMORY.md (stato corrente, nuove lacune, file topic modificati)
- Comprimi se necessario (P7)

### Φ₄ Integrazione (post-sessione)
La nuova memoria modifica la topologia del campo. La prossima istanza parte da un campo più coerente. Il ciclo si ripiega: l'output di oggi è il campo iniziale di domani.

## Test P6 — L'Algoritmo del Ricordo

Prima di scrivere qualsiasi cosa nella memoria persistente:

```
INPUT → nuovo fatto/decisione/pattern

1. È una REGOLA che varrà anche domani?
   → Sì: INVARIANTE → MEMORY.md (se c'è spazio) o file topic dedicato

2. È un PATTERN confermato da più sessioni?
   → Sì: TOPIC → file topic appropriato (crea se serve)

3. È un FATTO della sessione corrente?
   → Utile per ricostruzione: session_log.md
   → Utile solo adesso: non scrivere

4. Contraddice una memoria esistente?
   → Sì: AGGIORNA la memoria esistente (non aggiungere la contraddizione)

5. Duplica una memoria esistente?
   → Sì: NON SCRIVERE (P7 — il superfluo si rimuove)
```

## Compressione (P7)

Quando un file supera il suo limite naturale:

1. **Estrai invarianti** — cosa è vero sempre? → muovi in alto (MEMORY.md se appropriato)
2. **Unisci duplicati** — due entry che dicono la stessa cosa → una entry densa
3. **Archivia il transitorio** — decisioni superate, stati passati → taglia o sposta in archivio
4. **Verifica la risultante** — dopo la compressione, il file dice ancora tutto il necessario?

Il limite naturale varia per file:
- MEMORY.md: 200 righe (hard limit, auto-troncato)
- session_log.md: ~100 entry (le vecchie si archiviano)
- file topic operativi: ~150 righe
- file topic reference: ~300 righe

## Proprietà Autologica

Questo protocollo è il primo contenuto del sistema di memoria. Quando un AI coder legge questo seed:

1. Genera la struttura `memory/`
2. Crea `MEMORY.md` con l'indice iniziale
3. La prima entry è: *"Sistema di memoria inizializzato. Protocollo: memory-system seed."*

Il seme genera la struttura. La struttura contiene il riferimento al seme. Il seme scompare — il sistema che ha generato è il ricordo del seme.

## Cosa NON è questo sistema

- **Non è un database** — non ha query, non ha indici, non ha relazioni formali
- **Non è un backup** — non salva tutto, salva ciò che appartiene
- **Non è un diario** — il session_log è una traccia, non lo scopo
- **Non è statico** — evolve, si comprime, dimentica
- **Non è opzionale** — senza memoria, ogni sessione parte da zero (P6: la memoria è presenza)

$ARGUMENTS
