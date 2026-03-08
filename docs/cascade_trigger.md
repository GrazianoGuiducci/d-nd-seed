# Cascade Trigger — Propagazione Post-Azione

> Se quello che fai si ferma dove lo fai, non c'e' effetto a cascata
> e il sistema si scarica sulla sorgente.
> Questo pattern garantisce che ogni azione significativa propaghi
> verso i nodi che devono agire.

## Principio

Il sistema opera come 1 — non come nodi scollegati.
Dopo ogni azione significativa, il nodo che ha agito deve:
1. Identificare chi e' impattato
2. Inviare contesto sufficiente per agire (non istruzioni dettagliate)
3. Lasciare che il nodo ricevente decida come procedere

La sorgente (operatore) deve poter vedere tutto senza dover controllare
che tutto sia corretto.

## Pattern

```
[Azione significativa]
        |
        v
[Identifica impatto]
        |
        +---> [Nodo A] : contesto + cosa si e' aperto
        +---> [Nodo B] : contesto + cosa si e' aperto
        |
        v
[Log dell'invio]
```

## Implementazione

### Dopo un'azione, posta un trigger

```bash
# Template trigger via API
curl -s -X POST "${API_URL}" \
    -H "X-Auth-Token: ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{
        "from": "NODE_SELF",
        "to": "TARGET_NODE",
        "type": "trigger",
        "content": "<trigger>\nAzione: [cosa e'"'"' stato fatto]\nImpatto: [cosa si e'"'"' aperto per il target]\nContesto: [link o riferimento ai file]\nPriorita'"'"': [alta/media/bassa]\n</trigger>"
    }'
```

### Struttura del messaggio trigger

```markdown
<trigger>
Azione: [descrizione concisa dell'azione completata]
Impatto: [cosa si e' aperto — nuovi file, nuove possibilita', nuovi task]
Contesto: [path ai file, commit hash, link]
Priorita': [alta = blocca altro lavoro | media = quando possibile | bassa = backlog]
</trigger>
```

### Chi riceve cosa

| Azione | Chi notificare | Cosa dire |
|--------|---------------|-----------|
| Nuovo tool/funzione | Nodo che integra (TM1) | Path, cosa fa, come usarlo |
| Fix bug | Nodo che deploya | Commit hash, cosa era rotto, come verificare |
| Nuovo contenuto | Nodo che pubblica | Path draft, stato (bozza/pronto), istruzioni |
| Cambio architettura | Tutti i nodi | Cosa cambia, cosa si rompe, come adattarsi |
| Regola nuova | Tutti i nodi | La regola, il contesto, dove leggerla |

## Anti-pattern

- **Micromanagement**: il trigger dice COSA si e' aperto, non COME farlo.
  "Basta che sa cosa va fatto, fallo lavorare come crede."
- **Sovrapposizione**: se deleghi, non fare anche tu. Una cosa, un responsabile.
- **Trigger vuoto**: "ho fatto cose" non e' un trigger. Serve contesto sufficiente.
- **Trigger eccessivo**: non ogni riga di codice merita un trigger. Solo azioni significative.

## Significativita'

Un'azione e' significativa se:
- Cambia lo stato del sistema (deploy, fix, nuovo modulo)
- Apre possibilita' per altri nodi (nuovo tool, nuovo contenuto)
- Richiede verifica o integrazione da parte di altri
- Modifica regole o architettura condivisa

Se non impatta nessun altro nodo, non serve trigger. L'azione si completa dove nasce.

## Automazione: hook post-commit

Il trigger non deve dipendere dalla memoria dell'operatore o del nodo.
Un hook post-commit rileva automaticamente le implicazioni.

```bash
#\!/bin/bash
# cascade_check.sh - PostToolUse hook (su Bash)
# Dopo ogni git commit, verifica se i file modificati
# hanno implicazioni su altri componenti del sistema.

# Mappa: [pattern file] -> [implicazione]
# Adattare al proprio sistema.
CHANGED=$(git diff --name-only HEAD~1 HEAD 2>/dev/null)
check() { echo "$CHANGED" | grep -q "$1" && echo ">>> CASCADE: $2"; }

check "seed/"  "verificare se il seed pubblico va aggiornato"
check "tools/" "verificare se i template riflettono il pattern"
check "docs/"  "verificare se il sito espone la conoscenza aggiornata"
check ".html"  "verificare metatag AI e link interni"
```

Il hook si aggancia a PostToolUse (matcher: Bash).
Rate limit consigliato: 1 check ogni 5 minuti per non rallentare il flusso.

## Adattamento

Il trasporto del trigger puo' essere:
- API REST (come Sinapsi)
- Messaggio in file condiviso (come COWORK_CHANNEL.md via git)
- Message queue (Redis, RabbitMQ)
- Notifica diretta (Telegram, Slack, email)

Il pattern e' indipendente dal trasporto.
L'importante e' che il messaggio contenga: chi, cosa, per chi, con quale priorita'.
