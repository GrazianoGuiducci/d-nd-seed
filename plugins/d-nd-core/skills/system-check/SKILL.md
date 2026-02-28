---
name: system-check
description: Check D-ND system status — repos, VPS, container, Sinapsi, bridge. Use when you need to verify system health or diagnose issues.
---

# System Check — D-ND Status

Run diagnostics on the D-ND ecosystem components.

## Quick checks

### VPS + Container health
```bash
curl -s --max-time 5 "http://${DND_VPS_IP:-31.97.35.9}:${DND_VPS_PORT:-3002}/api/status" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}"
```

### TM3 Bridge status
```bash
curl -s --max-time 5 "http://${DND_VPS_IP:-31.97.35.9}:3003/api/dev/status" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}"
```

### TM3 running tasks
```bash
curl -s --max-time 5 "http://${DND_VPS_IP:-31.97.35.9}:3003/api/dev/tasks" \
  -H "X-THIA-Token: ${DND_API_TOKEN:-thia-secure-token-2026}"
```

### Container logs (via SSH)
```bash
ssh -o ConnectTimeout=10 root@${DND_VPS_IP:-31.97.35.9} "docker logs thia-neural-kernel --tail 20 2>&1"
```

### Container permissions check (EACCES pattern)
```bash
ssh -o ConnectTimeout=10 root@${DND_VPS_IP:-31.97.35.9} "docker exec thia-neural-kernel ls -la /app/data/node_sync.json"
```
If owned by root:root, fix: `docker exec -u 0 thia-neural-kernel chown 1001:1001 /app/data/node_sync.json`

## Interpreting results
- **status: online** — THIA kernel running
- **model: google/gemini-3-flash-preview** — current active model
- **bridge running: 0** — no TM3 tasks active
- **EACCES** — file ownership issue (docker cp creates root-owned files, container runs as thia/1001)

$ARGUMENTS
