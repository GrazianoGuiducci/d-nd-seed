# Sinapsi Polling — Ascolto Inter-Nodo

> Pattern per un nodo AI che ascolta automaticamente i messaggi degli altri nodi.
> Non richiede webhook in ingresso — il nodo interroga a intervalli regolari.
> Funziona con qualsiasi API che espone messaggi non letti.

## Architettura

```
[Nodo A] --POST--> [API messaggi] <--GET-- [Nodo B polling]
                        |
                   {from, to, type, content, read_by}
```

Ogni nodo ha un identificativo (es. NODE_A, NODE_B, SYSTEM).
I messaggi hanno un campo `read_by[]` — tracking per nodo, non globale.
Ogni nodo marca i propri messaggi come letti dopo averli processati.

## Implementazione: Hook su evento utente

Il polling si aggancia a un evento del sistema ospite.
In Claude Code: hook `UserPromptSubmit` (si attiva ad ogni messaggio dell'utente).
In altri sistemi: cron, webhook, event loop — il pattern e' lo stesso.

### Template hook (bash)

```bash
#!/bin/bash
# sinapsi_polling.sh — controlla messaggi non letti per questo nodo
# Aggancia a: UserPromptSubmit, cron, o qualsiasi trigger periodico

NODE_ID="${NODE_ID:-MY_NODE}"
API_URL="${API_URL:-http://localhost:3002/api/node-sync}"
API_TOKEN="${API_TOKEN:-$(cat /path/to/token)}"
LAST_CHECK_FILE="/tmp/.sinapsi_last_check_${NODE_ID}"
MIN_INTERVAL=60  # secondi tra check

# Rate limiting
if [ -f "$LAST_CHECK_FILE" ]; then
    LAST=$(cat "$LAST_CHECK_FILE")
    NOW=$(date +%s)
    DIFF=$((NOW - LAST))
    if [ "$DIFF" -lt "$MIN_INTERVAL" ]; then
        exit 0
    fi
fi
date +%s > "$LAST_CHECK_FILE"

# Fetch unread
RESPONSE=$(curl -s "${API_URL}?for=${NODE_ID}&unread=true&reader=${NODE_ID}" \
    -H "X-Auth-Token: ${API_TOKEN}" 2>/dev/null)

COUNT=$(echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('messages',[])))" 2>/dev/null || echo "0")

if [ "$COUNT" -gt 0 ]; then
    echo "[Sinapsi] ${COUNT} messaggi non letti per ${NODE_ID}"
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('messages', []):
    print(f\"  [{m.get('from','?')}] {m.get('content','')[:120]}\")
"
fi
```

### Marcare come letto

```bash
curl -s -X PATCH "${API_URL}/${MSG_ID}/read" \
    -H "X-Auth-Token: ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"reader\":\"${NODE_ID}\"}"
```

### Rispondere

```bash
curl -s -X POST "${API_URL}" \
    -H "X-Auth-Token: ${API_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"from\":\"${NODE_ID}\",\"to\":\"TARGET_NODE\",\"type\":\"response\",\"content\":\"...\"}"
```

## Configurazione hook (Claude Code)

```json
{
    "hooks": {
        "UserPromptSubmit": [
            {
                "type": "command",
                "command": "/path/to/sinapsi_polling.sh"
            }
        ]
    }
}
```

## Proprieta' del pattern

- **Pull, non push**: il nodo decide quando ascoltare (niente interruzioni non richieste)
- **Rate limited**: intervallo minimo tra check (default 60s)
- **Per-node tracking**: ogni nodo ha il proprio stato di lettura
- **Idempotente**: rileggere non cambia lo stato — solo il mark-read cambia
- **Medium-agnostic**: funziona con REST API, file condiviso, database, message queue

## Adattamento

Per usare con un file condiviso invece di un'API:

```bash
# Invece di curl, leggi dal file
MESSAGES=$(cat /shared/messages.json | python3 -c "
import sys, json
msgs = json.load(sys.stdin)
unread = [m for m in msgs if '${NODE_ID}' not in m.get('read_by', [])]
print(json.dumps({'messages': unread}))
")
```

Il pattern e' lo stesso — cambia solo il trasporto.
