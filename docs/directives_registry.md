# Registro direttive — pattern di visibilita' della propagazione

> Una direttiva strutturale permanente vive in piu' punti del sistema.
> Il registro mostra dove esiste e dove manca.
> L'attrito di propagare resta — il registro lo rende visibile.

---

## Il principio

Un sistema con piu' nodi, piu' repo, piu' layer tende ad accumulare direttive
strutturali permanenti: regole di modo, principi di lavoro, vincoli operativi
che devono valere in piu' posti contemporaneamente.

Ogni direttiva vive in posti diversi: il boot di ogni nodo, il kernel del sistema,
il seme propagabile, le skill operative, i manifesti pubblici. La stessa regola
cambia forma in ogni contesto — la formulazione per il boot e' diversa da quella
per il seme, che e' diversa dalla pagina pubblica.

Senza un registro, la propagazione e' invisibile. Una direttiva nata in un nodo
potrebbe non arrivare mai agli altri, oppure arrivare con formulazioni che
si sono divergenti nel tempo. Il drift e' silenzioso.

Il registro **non inietta** la direttiva in tutti i posti — mostra **dove esiste
e dove manca**. La propagazione resta manuale. L'attrito della scrittura manuale
e' il processo che fa assorbire la regola dal nodo che la scrive.

## Perche' non automatizzare l'iniezione

Automatizzare la propagazione sembra piu' efficiente ma produce rischi strutturali:

- **Regole non assorbite**: una regola iniettata in 7 posti da uno script non e'
  stata digerita da nessun nodo. Arriva come dato estraneo, non come modus.

- **Propagazione di errori**: una regola sbagliata si propaga alla velocita'
  dell'iniettore. La propagazione manuale fa da filtro — ogni nodo la rilegge
  mentre la applica.

- **Conformismo senza comprensione**: l'attrito di riformulare ogni volta
  costringe a ripensare la direttiva nel contesto specifico. Senza attrito,
  la direttiva diventa copia, non applicazione.

Il registro automatizza **la visibilita'**, non l'azione.

## Targets canonici

I posti tipici dove vive una direttiva strutturale permanente:

| Target | Quando serve |
|--------|--------------|
| Boot di ogni nodo | Ogni direttiva permanente — il nodo la legge al boot |
| Kernel di sistema | Direttive che toccano il nucleo (memoria, awareness, protocolli) |
| Node profile (es. `.claude/CLAUDE.md`) | Direttive metodologiche per lo sviluppo |
| Seme — kernels | Direttive assiomatiche, forma neutra trasferibile |
| Seme — docs | Direttive metodologiche, forma neutra trasferibile |
| Skill operative (auto-learn, cascade, ecc.) | Direttive su come imparare, come propagare |
| Nucleo condiviso iniettato nei prompt | Corollari assiomatici che cambiano il comportamento runtime |
| Protocollo inter-nodo | Direttive sulla collaborazione tra nodi |
| Pagine pubbliche | Solo dopo stabilizzazione interna completa |

Ogni sistema istanzia il proprio set di targets canonici sulla base della sua architettura.

## Shape del registro

Una struttura semplice che ogni nodo puo' adottare:

```markdown
# Registro Direttive

## Targets canonici
[tabella dei posti dove vive una direttiva nel proprio sistema]

## Direttive

### [Nome direttiva]
**Forma**: [la formulazione canonica]
**Derivazione**: [da quali assiomi o principi discende]
**Origine**: [quando e' stata cristallizzata, da chi]

**Stato propagazione**:
- [x] target 1 (chi, quando)
- [ ] target 2
- [x] target 3 (chi, quando)
- [ ] target 4

**Istanze operative preesistenti**: [se la direttiva riconosce retroattivamente
applicazioni gia' presenti nel sistema come casi particolari]
```

Quando emerge una nuova direttiva:
1. Aggiungere la sezione al registro con **targets dichiarati ma vuoti**
2. Propagare manualmente a ogni target, rileggendo e riformulando per il contesto
3. Spuntare il target dopo la propagazione
4. Il registro mostra sempre cosa manca

## Come si legge il drift

- `[x]` → propagato e verificato
- `[ ]` → non ancora propagato o da verificare
- Una direttiva con molti `[ ]` e' un **segnale di drift**: la regola esiste
  in un posto ma non ha ancora raggiunto il resto del sistema
- Cristallizzazione retroattiva: direttive vecchie che non erano state tracciate
  possono essere aggiunte al registro con lo stato reale — rivela quello che
  il sistema non aveva mai mappato esplicitamente

## Come si usa come strumento operativo

**Al boot del nodo**: leggere il registro, identificare `[ ]` su direttive critiche,
decidere se propagare ora o segnalare come debito.

**Dopo cristallizzazione di una nuova direttiva**: aggiungere la sezione al registro
**prima** di propagare. Questo garantisce che non venga dimenticato nessun target.

**Quando una formulazione e' incerta**: cercare la direttiva nel registro, leggere
i target gia' spuntati — uno di quelli e' probabilmente il modello di formulazione
adatto per il contesto corrente.

**In coordinamento inter-nodo**: ogni nodo ha il proprio registro locale. Quando
si aggiorna, si notifica via canale inter-nodo (Sinapsi, git, messaggio).
Una direttiva condivisa appare nei registri di tutti i nodi coinvolti con targets
e stati propri.

## Relazione con altri pattern del seme

**Cascata** (`cascade_trigger.md`): il registro e' l'incarnazione concreta
del principio di cascata applicato alle direttive strutturali. La cascata dice
"quando qualcosa cambia, chi altro deve saperlo?" Il registro mostra dove la risposta
e' ancora aperta.

**Autologica**: il registro permette di applicare l'autologica alle direttive
stesse. La direttiva sul metodo si applica anche al metodo del registro —
se una formulazione si dimostra debole in un target, si corregge e si propaga
la correzione agli altri target tramite il registro stesso.

**Auto-learn**: quando una direttiva e' cristallizzata da un errore risolto,
la fase "Propagate" dell'auto-learn produce una sezione del registro.
Il registro diventa memoria tracciata dell'apprendimento del sistema.

---

## Boundary

Il registro non sostituisce il giudizio di chi propaga.
Non dice quale formulazione e' giusta in ogni contesto.
Non impone completezza — un `[ ]` che resta aperto a lungo e' un dato,
non un allarme.

Il registro e' uno specchio. Riflette lo stato del sistema.
Chi legge decide se e come agire.

---

*La propagazione manuale e' il processo che fa assorbire la regola.
Il registro rende visibile dove il processo non e' ancora avvenuto.*
