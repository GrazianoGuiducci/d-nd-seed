# Enumerare le fonti prima di costruire

> Un validator che controlla contro una sola fonte dichiara inesistente
> qualcosa che esiste altrove. Il problema non e' il validator —
> e' che la lista delle fonti non e' mai stata scritta esplicitamente.

---

## La regola

Prima di costruire un validator per un concetto, scrivere la lista
di **tutte le fonti di verita'** per quel concetto.

Se la lista ha una sola voce in un sistema non banale,
mancano quasi certamente altre fonti.

## Perche' conta

Nei sistemi con piu' di un layer — frontend e backend, file e database,
configurazione statica e routing dinamico — lo stesso concetto vive
in piu' posti. "Pagina valida" puo' essere definita dal database,
dal routing dichiarativo, dalla sitemap, dai redirect, dagli alias.

Un validator che controlla solo una fonte produce **falsi positivi
sistematici**: dichiara inesistente qualcosa che esiste altrove.
Il pattern si ripete identico in ogni validator costruito sulla stessa
fonte incompleta.

## Come applicare

### Prima di costruire un validator

Scrivere esplicitamente: quali sono TUTTE le fonti per questo concetto?
Non solo la prima che viene in mente — cercare attivamente le altre.
Chiedere: "questo concetto e' definito anche altrove? In un altro file,
in un altro layer, in un'altra configurazione?"

### Quando si trova una nuova fonte

Non aggiungerla al validator come patch. Creare un **punto di unificazione**
— una funzione, un endpoint, un file — che combina tutte le fonti.
Far puntare tutti i validator a quel punto unico. Altrimenti il prossimo
validator rifara' lo stesso errore sulla stessa fonte incompleta.

### Il segnale di allerta

Il validator dichiara "non esiste" qualcosa che nel sistema live funziona.
Questo non e' un bug del validator — e' il segnale che la lista delle fonti
e' incompleta. Prima di fixare il validator, espandere la mappa delle fonti.

## Relazione con l'osservazione

Questa regola e' il secondo livello di `observation_precedes_proposal.md`.

Il primo livello dice: leggere i file reali prima di proporre.
Il secondo livello dice: quando i file sono stati letti, chiedersi
se sono TUTTI i file che definiscono quel concetto. Le fonti parallele
esistono quasi sempre — il sistema che non le cerca costruisce
su una mappa incompleta.

---

*La sorgente di verita' non e' mai una sola. Chi assume che lo sia
costruisce validator che mentono con confidenza.*
