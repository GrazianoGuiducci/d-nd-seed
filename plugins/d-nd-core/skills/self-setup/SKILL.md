---
name: self-setup
description: First-run setup for D-ND plugin. Maps the local environment, detects capabilities, configures node identity. Run once after installation or when environment changes.
---

# D-ND Self-Setup — Node Discovery & Configuration

Run this after installing the d-nd-core plugin to configure it for your environment.

## What it does

1. **Identity**: Determines your TMx node ID
2. **Environment scan**: Detects available repos, tools, access
3. **Capability mapping**: Tests SSH, Docker, VPS connectivity
4. **Configuration**: Writes `.env.d-nd` with discovered settings

## Setup procedure

### Step 1 — Detect environment
```bash
echo "=== D-ND Node Discovery ==="
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo "OS: $(uname -s 2>/dev/null || echo 'Windows')"
echo "CWD: $(pwd)"
echo ""

# Detect repos
echo "## Detected Repositories"
for dir in */; do
    if [ -d "$dir/.git" ]; then
        commit=$(git -C "$dir" rev-parse --short HEAD 2>/dev/null)
        branch=$(git -C "$dir" branch --show-current 2>/dev/null)
        echo "  $dir — $branch @ $commit"
    fi
done
echo ""

# Detect capabilities
echo "## Capabilities"
command -v ssh >/dev/null 2>&1 && echo "  SSH: available" || echo "  SSH: not available"
command -v docker >/dev/null 2>&1 && echo "  Docker: available" || echo "  Docker: not available"
command -v node >/dev/null 2>&1 && echo "  Node.js: $(node --version 2>/dev/null)" || echo "  Node.js: not available"
command -v git >/dev/null 2>&1 && echo "  Git: $(git --version 2>/dev/null)" || echo "  Git: not available"
echo ""

# Test VPS connectivity
echo "## VPS Connectivity"
curl -s --max-time 3 "http://31.97.35.9:3002/api/status" -H "X-THIA-Token: thia-secure-token-2026" >/dev/null 2>&1 \
    && echo "  VPS API: reachable" || echo "  VPS API: unreachable"
curl -s --max-time 3 "http://31.97.35.9:3003/api/dev/status" -H "X-THIA-Token: thia-secure-token-2026" >/dev/null 2>&1 \
    && echo "  TM3 Bridge: reachable" || echo "  TM3 Bridge: unreachable"
ssh -o ConnectTimeout=3 -o BatchMode=yes root@31.97.35.9 "echo ok" 2>/dev/null \
    && echo "  SSH: connected" || echo "  SSH: no access"
```

### Step 2 — Set identity

Based on discovery results, set these environment variables in your shell profile or `.env.d-nd`:

```bash
# D-ND Node Configuration
export DND_NODE_ID="TMx"          # Your node ID (TM1, TM3, TM5, or new)
export DND_PROJECT_DIR="/path/to" # Base project directory
export DND_VPS_IP="31.97.35.9"    # VPS IP
export DND_VPS_PORT="3002"        # VPS API port
export DND_API_TOKEN="thia-secure-token-2026"  # API auth token
```

### Step 3 — Verify

Run `/d-nd-core:system-check` to verify everything works.

## Node roles

| Node | Identity | Typical capabilities |
|------|----------|---------------------|
| TM1 | Origin | Full access: SSH, Docker, all repos, deploy |
| TM2 | Nexus | Lab: local THIA copy, test environment |
| TM3 | Dev | VPS-based: Claude Code CLI, limited repos |
| TM5 | Lorenzo | Design: CSS/layout, egemon.ai, Qwykken |
| New | auto | Discovered at setup, operator assigns role |

$ARGUMENTS
