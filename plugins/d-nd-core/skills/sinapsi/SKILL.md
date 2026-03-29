---
name: sinapsi
description: "Send and receive messages via inter-node communication. Use when you need to communicate with other nodes, check messages, or send task updates."
---

# Sinapsi — Inter-Node Communication

Communicate with other nodes in your distributed system.

## Environment

- `DND_VPS_IP` — Server IP or hostname
- `DND_VPS_PORT` — API port (default: 3002)
- `DND_API_TOKEN` — Authentication token
- `DND_NODE_ID` — Your node identity

## Commands

### Read unread messages
```bash
curl -s "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync?for=${DND_NODE_ID}&unread=true" \
  -H "X-Auth-Token: ${DND_API_TOKEN}"
```

### Send a message
```bash
curl -s -X POST "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: ${DND_API_TOKEN}" \
  -d '{"from":"'${DND_NODE_ID}'","to":"TARGET_NODE","type":"info","content":"MESSAGE"}'
```

### Mark message as read
```bash
curl -s -X PATCH "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync/MSG_ID/read" \
  -H "X-Auth-Token: ${DND_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"reader":"'${DND_NODE_ID}'"}'
```

## Message types
- `info` — General information
- `task` — Task assignment or update
- `response` — Reply to a task or question
- `report` — Status report
- `ack` — Acknowledgment

## Protocol
1. Check unread messages before sending new ones
2. Mark messages as read after processing
3. Include context: what you did, what you need, what the result was
4. One message per topic — do not bundle unrelated items

$ARGUMENTS

## Eval

## Trigger Tests
# "check messages" -> activates
# "send a message to the other node" -> activates
# "any unread messages?" -> activates
# "deploy" -> does NOT activate

## Fidelity Tests
# Given unread messages: displays summary with sender, type, preview
# Given no unread: reports "no unread messages"
# Given send request: constructs correct JSON with from/to/type/content
