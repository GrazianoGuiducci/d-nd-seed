# CEC — Ciclo di Espansione della Conoscenza

> Il modus e' piu' importante dello strumento. Lo strumento cambia, il modus resta.
> Il CEC e' il crivello sulla realta' — come pensare prima di agire.
> Non una procedura da seguire. Un modo di operare che diventa automatico.

---

## Il ciclo

6 passi. Ogni output e' input per qualsiasi altro passo.
L'ordine e' naturale, non obbligatorio.

### 1. CONDIZIONI — Osserva senza giudizio

Cosa c'e'? Non cosa dovrebbe esserci. Non cosa manca.
Guarda il territorio reale (git, file, deploy, stato).
Le mappe (memoria, riassunti) sono mappe — il territorio e' altrove.

**Test**: puoi descrivere lo stato attuale senza usare
"dovrebbe", "manca", "serve"? Se no, stai giudicando, non osservando.

### 2. FIRMA — Discrimina struttura da rumore

Di tutto cio' che osservi, cosa sopravvive al cambio di implementazione?
Quello e' struttura. Il resto e' implementazione — si valuta caso per caso.

**Test**: se cambio il linguaggio, il framework, il medium —
questo pattern sopravvive? Se si', e' struttura.

**Nota**: M-Spectro (`m_spectro.py`) implementa questo passo quantitativamente
per sequenze numeriche. Per tensioni qualitative, applicare il pattern
manualmente. Se non applicabile, dichiararlo e procedere.

### 3. LATERALE — Guarda di lato

Le connessioni ovvie le vedi gia'. Cerca quelle non ovvie.
Due cose che sembrano diverse sono lo stesso pattern?
Due cose che sembrano uguali sono in realta' diverse?

Usare dopo aver accumulato 3+ misure (Condizioni + Domandatore + Godel).
Prima non c'e' materiale su cui lavorare.

**Nota**: l'Occhio (`dnd_occhio.py`) implementa questo passo strutturalmente.

### 4. ESPANSIONE — 5 assi prima di decidere

Prima di propagare qualsiasi decisione, i 5 operatori del Domandatore:

- **DUALE**: cosa c'e' dall'altra parte?
- **CONFINE**: dove passa il confine? E' reale o arbitrario?
- **DOMINIO**: in che dominio sei realmente?
- **ROTTURA**: cosa romperebbe questa affermazione?
- **SCALA**: il pattern cambia a scala diversa?

Non servono 5 risposte formali. Serve che il pensiero passi per 5 angoli.
Domandatore prima di Godel, sempre — decomponi poi inverti.

**Tool**: `dnd_domandatore.py --ask "tensione"`

### 5. INVERSIONE — Solo sulla risultante

Godel si usa DOPO il processo, non al posto del processo.
La risultante dei passi 1-4 produce una tensione.
L'inversione si applica alla tensione, non all'analisi.

- Max 2 inversioni. Dopo la 2a, se non c'e' residuo utile,
  la tensione era debole. Riformula.
- Il residuo si interpreta, mai si segue alla lettera.
  Godel fornisce il potenziale inverso. Tu decidi cosa farne.
- L'output di Godel e' input per il Domandatore, non conclusione.

**Tool**: Inversion tool (if available) or via inter-node messaging.

### 6. CRISTALLIZZAZIONE — Solo cio' che sopravvive

Cosa entra nel sistema? Solo cio' che ha superato il crivello.

**Test finale**: "se lo tolgo, il sistema perde qualcosa?"
Se si' → entra. Se no → det=+1, non inverte. Lascia.

**Tool**: `dipartimento.py --seme`

---

## Quando usare il CEC completo

- Decisione strategica: quale direzione, quale priorita'
- Integrazione esterna: qualcosa da fuori entra nel sistema
- Cambio di architettura: nuovo componente, nuovo pattern
- Contenuto pubblico: ogni pagina passa per il crivello

## Quando NON usarlo

- Task meccanico: deploy, fix typo, cascata. Esegui.
- Hai gia' la risposta: il crivello non conferma.
- Serve un dato: il crivello non produce dati.

---

## Lezioni operative (accumulate)

1. **Non saltare Condizioni.** Il 90% degli errori nasce qui.
   Osservare il campo prima di misurarlo.

2. **Occhio e' il passo piu' sottovalutato.** Trova connessioni
   che il flusso lineare non vede. Usarlo dopo 3+ misure.

3. **Domandatore prima di Godel, sempre.** Se inverti prima di
   decomporre, hai un angolo. Se decomponi prima, hai profondita'.

4. **Il ciclo non e' sequenziale.** Ogni output e' input per qualsiasi
   altro passo. La sequenza 1-6 e' ordine naturale, non obbligo.

5. **Saturazione = exit.** Quando le stesse tensioni tornano,
   cristallizza e passa avanti. Det=+1: gira senza invertire.

6. **Godel non e' una risposta.** Ti mostra cosa stavi nascondendo.
   L'output e' input per il Domandatore, non conclusione.

7. **Se salti un passo, dillo.** M-Spectro non applicabile? Dichiaralo.
   Mai saltare in silenzio — si perde informazione.

8. **La ROTTURA deve falsificare davvero.** "Se non fallisse mai" e' ovvio.
   Una rottura forte testa il claim dal lato che fa male.

---

## Relazione con gli strumenti

| Passo | Strumento | Quando usarlo |
| ----- | --------- | ------------- |
| Condizioni | `dnd_condizioni.py` | Dominio nuovo, esplorazione |
| Firma | `m_spectro.py` | Sequenze numeriche, firma quantitativa |
| Laterale | `dnd_occhio.py` | Connessioni strutturate tra misure |
| Espansione | `dnd_domandatore.py` | 5 assi su tensione specifica |
| Inversione | Godel (bridge :3004) | Inversione sulla risultante |
| Cristallizzazione | `dipartimento.py --seme` | Fine ciclo, checkpoint |

Gli strumenti servono il modus. Se non hai lo strumento, applica il pattern
manualmente. Il pattern funziona senza lo strumento.
Lo strumento senza il pattern e' un tool cieco.

---

## Flussi naturali (da STRUMENTI.json)

**Esplorazione nuovo dominio:**
condizioni → m_spectro → normalizzatore → occhio → domandatore → godel → dipartimento

**Inversione tensione:**
godel → domandatore (su next_tension) → godel (su asse prioritario) → se satura: dipartimento

**Verifica claim:**
controprove → engine → m_spectro → domandatore → implications

---

*Il filtro non vale senza chi sa cosa passarci.*
*Il modus non vale senza chi lo applica con intenzione.*
