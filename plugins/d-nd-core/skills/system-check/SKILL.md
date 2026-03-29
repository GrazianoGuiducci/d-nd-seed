---
name: system-check
description: "Check system status — repos, services, containers, APIs. Use when you need to verify system health or diagnose issues."
---

# System Check — Status Diagnostics

Run diagnostics on your system components. Adapt the commands to your infrastructure.

## Quick checks

### API health
```bash
curl -s --max-time 5 "http://${DND_VPS_IP:-localhost}:${DND_VPS_PORT:-3002}/api/status" \
  -H "X-Auth-Token: ${DND_API_TOKEN}"
```

### Service status
```bash
# Check if your main service is running
systemctl is-active ${DND_SERVICE_NAME:-my-service} 2>/dev/null || echo "Service not found"
```

### Container health (if using Docker)
```bash
docker ps --filter "name=${DND_CONTAINER_NAME:-my-container}" --format "{{.Names}}: {{.Status}}"
```

### Container logs
```bash
docker logs ${DND_CONTAINER_NAME:-my-container} --tail 20 2>&1
```

## Interpreting results
- **status: online** — API responding
- **Up X minutes (healthy)** — container running with health check passing
- **EACCES** — file ownership issue (docker cp creates root-owned files)

## Environment variables
Configure these in your `.env` or shell profile:
- `DND_VPS_IP` — your server IP (default: localhost)
- `DND_VPS_PORT` — API port (default: 3002)
- `DND_API_TOKEN` — authentication token
- `DND_CONTAINER_NAME` — Docker container name
- `DND_SERVICE_NAME` — systemd service name

$ARGUMENTS

## Eval

## Trigger Tests
# "check system health" -> activates
# "is the server running" -> activates
# "diagnose API issues" -> activates
# "deploy new version" -> does NOT activate

## Fidelity Tests
# Given healthy system: reports all services online
# Given API down: reports unreachable with suggestion
# Given missing env vars: uses defaults, warns about configuration
