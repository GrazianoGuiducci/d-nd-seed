---
name: sinapsi
description: Send and receive messages via D-ND Sinapsi inter-node communication. Use when you need to communicate with other TMx nodes, check messages, or send task updates.
---

# Sinapsi — D-ND Inter-Node Communication

You have access to the Sinapsi API for communicating with other nodes in the D-ND network.

## Environment

- `DND_VPS_IP` — VPS IP (default: 31.97.35.9)
- `DND_VPS_PORT` — API port (default: 3002)
- `DND_API_TOKEN` — Auth token
- `DND_NODE_ID` — Your node identity (TM1, TM3, TM5...)

## Commands

### Read unread messages
```bash
curl -s "http://${DND_VPS_IP:-31.97.35.9}:${DND_VPS_PORT:-3002}/api/node-sync?for=${DND_NODE_ID}&unread=true" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}"
```

### Send a message
```bash
curl -s -X POST "http://${DND_VPS_IP:-31.97.35.9}:${DND_VPS_PORT:-3002}/api/node-sync" \
  -H "Content-Type: application/json" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}" \
  -d '{"from":"'${DND_NODE_ID}'","to":"TARGET_NODE","type":"info","content":"MESSAGE"}'
```

### Mark message as read
```bash
curl -s -X PATCH "http://${DND_VPS_IP:-31.97.35.9}:${DND_VPS_PORT:-3002}/api/node-sync/MSG_ID/read" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}"
```

## Message types
- `info` — General information
- `task` — Task assignment or update
- `ack` — Acknowledgment
- `alert` — Urgent notification

## Protocol
1. Always check unread messages before sending new ones
2. Mark messages as read after processing
3. When sending to TM3, messages auto-trigger the bridge (spawns Claude Code session)
4. Include context: what you did, what you need, what the operator said

$ARGUMENTS
