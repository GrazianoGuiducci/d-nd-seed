---
name: self-setup
description: "First-run setup for D-ND plugin. Maps the local environment, detects capabilities, configures node identity. Run once after installation or when environment changes."
---

# D-ND Self-Setup — Node Discovery & Configuration

Run this after installing the d-nd-core plugin to configure it for your environment.

## What it does

1. **Environment scan**: Detects available repos, tools, access
2. **Capability mapping**: Tests SSH, Docker, API connectivity
3. **Configuration**: Writes `.env.d-nd` with discovered settings

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
command -v python3 >/dev/null 2>&1 && echo "  Python: $(python3 --version 2>/dev/null)" || echo "  Python: not available"
command -v git >/dev/null 2>&1 && echo "  Git: $(git --version 2>/dev/null)" || echo "  Git: not available"
echo ""

# Test API connectivity (if configured)
if [ -n "$DND_VPS_IP" ]; then
    echo "## API Connectivity"
    curl -s --max-time 3 "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/status" \
        -H "X-Auth-Token: ${DND_API_TOKEN}" >/dev/null 2>&1 \
        && echo "  API: reachable" || echo "  API: unreachable"
fi
```

### Step 2 — Set identity

Based on discovery results, set these environment variables in your shell profile or `.env.d-nd`:

```bash
# D-ND Node Configuration
export DND_NODE_ID="MY_NODE"          # Your node identifier
export DND_PROJECT_DIR="/path/to"     # Base project directory
export DND_VPS_IP=""                  # Server IP (if applicable)
export DND_VPS_PORT="3002"            # API port (if applicable)
export DND_API_TOKEN=""               # API auth token (if applicable)
```

### Step 3 — Verify

Run `/d-nd-core:system-check` to verify everything works.

## Node roles

Nodes are identified by their capabilities, not by fixed names:

| Capability | Description |
|-----------|-------------|
| **Full access** | SSH, Docker, all repos, deploy |
| **Development** | Code editor, local repos, test environment |
| **Satellite** | Autonomous project, receives seed updates |
| **Specialized** | Specific domain (design, finance, research) |

The operator assigns the role. The system adapts.

$ARGUMENTS

## Eval

## Trigger Tests
# "set up my node" -> activates
# "configure d-nd" -> activates
# "first time setup" -> activates
# "deploy" -> does NOT activate

## Fidelity Tests
# Given fresh environment: detects repos, capabilities, outputs config template
# Given configured environment: reports current config, suggests updates if needed
