#!/bin/bash
# ============================================================================
# D-ND SEED INSTALLER
# ============================================================================
# Generates .claude/ configuration from a profile and templates.
# The seed reads the profile, adapts the templates, writes the output.
#
# Usage:
#   ./install.sh <profile.json>
#   ./install.sh profiles/tm1.json
#   ./install.sh profiles/example.json --dry-run
#
# Requirements: bash, node (for JSON parsing)
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROFILE="$1"
DRY_RUN=""

if [ "$2" = "--dry-run" ]; then
    DRY_RUN="true"
fi

if [ -z "$PROFILE" ]; then
    echo "D-ND Seed Installer"
    echo ""
    echo "Usage: ./install.sh <profile.json> [--dry-run]"
    echo ""
    echo "Available profiles:"
    ls -1 "$SCRIPT_DIR/profiles/"*.json 2>/dev/null | while read f; do
        NAME=$(basename "$f" .json)
        DESC=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$f','utf8')).description||'')" 2>/dev/null)
        echo "  $NAME — $DESC"
    done
    exit 1
fi

if [ ! -f "$PROFILE" ]; then
    # Try relative to profiles/
    if [ -f "$SCRIPT_DIR/profiles/$PROFILE" ]; then
        PROFILE="$SCRIPT_DIR/profiles/$PROFILE"
    elif [ -f "$SCRIPT_DIR/profiles/${PROFILE}.json" ]; then
        PROFILE="$SCRIPT_DIR/profiles/${PROFILE}.json"
    else
        echo "ERROR: Profile not found: $PROFILE"
        exit 1
    fi
fi

echo "=== D-ND Seed Installer ==="
echo "Profile: $PROFILE"
echo ""

# --- Parse profile with node ---
eval $(node -e "
const fs = require('fs');
const p = JSON.parse(fs.readFileSync('$(echo "$PROFILE" | sed "s/'/\\\\'/g")','utf8'));

console.log('NODE_ID=\"' + (p.node_id || 'UNKNOWN') + '\"');
console.log('PROJECT_DIR=\"' + (p.project_dir || '.') + '\"');
console.log('THIA_PATH=\"' + (p.thia_path || '') + '\"');
console.log('MEMORY_PATH=\"' + (p.memory_path || '') + '\"');
console.log('VPS_URL=\"' + (p.vps_url || '') + '\"');
console.log('SINAPSI_FOR=\"' + (p.sinapsi_for || '') + '\"');

// Godel plugin config
const g = p.godel || {};
console.log('GODEL_ENABLED=\"' + (g.enabled ? 'true' : '') + '\"');
console.log('GODEL_EXAMPLE=\"' + (g.example || '') + '\"');
console.log('GODEL_NAME=\"' + (g.name || '') + '\"');
console.log('GODEL_DOMAIN=\"' + (g.domain || '') + '\"');
console.log('GODEL_DESC=\"' + (g.description || '') + '\"');
console.log('GODEL_PORT=\"' + (g.port || '3004') + '\"');

// Repos as bash array entries
const repos = (p.repos || []);
const repoArray = repos.map(r => '    \"' + r.name + ':' + r.path + ':' + r.branch + '\"').join('\n');
console.log('REPOS_ARRAY=\"' + Buffer.from(repoArray).toString('base64') + '\"');

// Primary repo (first in list)
console.log('PRIMARY_REPO=\"' + (repos[0] ? repos[0].path : '') + '\"');

// Repo names for fallback list in post_compact
const primaryNames = repos.slice(0, 3).map(r => r.path).join(' ');
console.log('PRIMARY_REPOS=\"' + primaryNames + '\"');

// For dirty check: generate bash lines
const dirtyCheck = repos.map(r =>
    'for R in \"\$PROJECT_DIR/' + r.path + '\"; do\\n' +
    '    if [ -d \"\$R/.git\" ]; then\\n' +
    '        D=\$(git -C \"\$R\" diff --name-only 2>/dev/null)\\n' +
    '        if [ -n \"\$D\" ]; then HAS_DIRTY=\"yes\"; fi\\n' +
    '    fi\\n' +
    'done'
).join('\\n');
console.log('REPOS_DIRTY_B64=\"' + Buffer.from(
    repos.map(r =>
        'for R in \"\$PROJECT_DIR/' + r.path + '\"; do\n' +
        '    if [ -d \"\$R/.git\" ]; then\n' +
        '        D=\$(git -C \"\$R\" diff --name-only 2>/dev/null)\n' +
        '        if [ -n \"\$D\" ]; then HAS_DIRTY=\"yes\"; fi\n' +
        '    fi\n' +
        'done'
    ).join('\n')
).toString('base64') + '\"');

// For repo_state calls
console.log('REPOS_STATE_B64=\"' + Buffer.from(
    repos.map(r => 'repo_state \"' + r.name + '\" \"\$PROJECT_DIR/' + r.path + '\"').join('\n')
).toString('base64') + '\"');

// For semantic check
console.log('REPOS_SEMANTIC_B64=\"' + Buffer.from(
    repos.map(r =>
        'if [ -d \"\$PROJECT_DIR/' + r.path + '/.git\" ]; then\n' +
        '    UNPUSHED=\$(git -C \"\$PROJECT_DIR/' + r.path + '\" log --oneline @{upstream}..HEAD 2>/dev/null | head -3)\n' +
        '    if [ -n \"\$UNPUSHED\" ]; then SEMANTIC_TAGS=\"\${SEMANTIC_TAGS}DEPLOY(' + r.name + ') \"; fi\n' +
        'fi'
    ).join('\n')
).toString('base64') + '\"');
" 2>/dev/null)

# Decode base64 blocks
REPOS_ARRAY_DECODED=$(echo "$REPOS_ARRAY" | base64 -d 2>/dev/null || echo "$REPOS_ARRAY" | base64 --decode 2>/dev/null)
REPOS_DIRTY_DECODED=$(echo "$REPOS_DIRTY_B64" | base64 -d 2>/dev/null || echo "$REPOS_DIRTY_B64" | base64 --decode 2>/dev/null)
REPOS_STATE_DECODED=$(echo "$REPOS_STATE_B64" | base64 -d 2>/dev/null || echo "$REPOS_STATE_B64" | base64 --decode 2>/dev/null)
REPOS_SEMANTIC_DECODED=$(echo "$REPOS_SEMANTIC_B64" | base64 -d 2>/dev/null || echo "$REPOS_SEMANTIC_B64" | base64 --decode 2>/dev/null)

echo "Node: $NODE_ID"
echo "Project: $PROJECT_DIR"
echo "Primary repo: $PRIMARY_REPO"
echo ""

TARGET="$PROJECT_DIR/.claude"

# --- Generate Sinapsi block for system_awareness ---
SINAPSI_BLOCK=""
if [ -n "$VPS_URL" ] && [ -n "$SINAPSI_FOR" ]; then
    SINAPSI_BLOCK="# --- Sinapsi: unread messages ---
echo \"## Sinapsi (unread for $SINAPSI_FOR)\"
SINAPSI=\$(curl -s --max-time 5 \"$VPS_URL/api/node-sync?for=$SINAPSI_FOR&unread=true\" -H \"X-Auth-Token: \${THIA_TOKEN:-${DND_API_TOKEN}}\" 2>/dev/null)
if [ \$? -eq 0 ] && [ -n \"\$SINAPSI\" ]; then
    node -e \"
const d=\$SINAPSI;
const t=d.total||0;
if(t===0){console.log('  No unread messages.')}
else{console.log('  '+t+' unread message(s):');
(d.messages||[]).forEach(m=>{
  console.log('  - ['+m.type+'] '+m.from+'->'+m.to+': '+(m.content||'').slice(0,100))
})}
\" 2>/dev/null || echo \"  Parse error.\"
else
    echo \"  Unreachable or no messages.\"
fi
echo \"\""
fi

# --- Generate extra health checks for system_awareness ---
EXTRA_HEALTH=""
# Docker check (if VPS_URL is localhost, we're on the server)
if echo "$VPS_URL" | grep -q "localhost"; then
    EXTRA_HEALTH="# --- Docker container health ---
echo \"## Docker Container\"
CONTAINER_STATUS=\$(docker ps --filter \"name=thia-neural-kernel\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null)
if [ -n \"\$CONTAINER_STATUS\" ]; then
    echo \"  \$CONTAINER_STATUS\"
else
    echo \"  thia-neural-kernel: NOT RUNNING\"
fi
echo \"\"

# --- TM3 Bridge status ---
echo \"## TM3 Bridge\"
BRIDGE_STATUS=\$(systemctl is-active tm3-bridge 2>/dev/null || echo \"unknown\")
echo \"  tm3-bridge: \$BRIDGE_STATUS\"
echo \"\""
fi

# API health check
if [ -n "$VPS_URL" ]; then
    EXTRA_HEALTH="$EXTRA_HEALTH
# --- API Health ---
echo \"## API Health\"
HEALTH=\$(curl -s --max-time 5 \"$VPS_URL/api/status\" -H \"X-Auth-Token: \${THIA_TOKEN:-${DND_API_TOKEN}}\" 2>/dev/null)
if [ \$? -eq 0 ] && [ -n \"\$HEALTH\" ]; then
    API_STATUS=\$(node -e \"
const d=\$HEALTH;
const h=Math.floor((d.uptime||0)/3600);
const m=Math.floor(((d.uptime||0)%3600)/60);
console.log((d.status||'unknown')+' | Model: '+(d.model||'unknown')+' | Uptime: '+h+'h'+m+'m')
\" 2>/dev/null || echo \"parse error\")
    echo \"  \$API_STATUS\"
else
    echo \"  API unreachable.\"
fi
echo \"\""
fi

# Extra warnings (disk space on server nodes)
EXTRA_WARNINGS=""
if echo "$VPS_URL" | grep -q "localhost"; then
    EXTRA_WARNINGS="# Disk space check
DISK_USAGE=\$(df -h /opt 2>/dev/null | awk 'NR==2 {print \$5}' | tr -d '%')
if [ -n \"\$DISK_USAGE\" ] && [ \"\$DISK_USAGE\" -gt 85 ] 2>/dev/null; then
    echo \"  DISK: /opt at \${DISK_USAGE}% usage\"
    WARN_COUNT=\$((WARN_COUNT + 1))
fi"
fi

# --- Template replacement function ---
apply_template() {
    TMPL_FILE="$1"
    OUTPUT_FILE="$2"

    if [ ! -f "$TMPL_FILE" ]; then
        echo "  SKIP: template not found: $TMPL_FILE"
        return
    fi

    CONTENT=$(cat "$TMPL_FILE")

    # Simple replacements
    CONTENT=$(echo "$CONTENT" | sed "s|{{NODE_ID}}|$NODE_ID|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PROJECT_DIR}}|$PROJECT_DIR|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{THIA_PATH}}|$THIA_PATH|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PRIMARY_REPO_PATH}}|$PROJECT_DIR/$PRIMARY_REPO|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PRIMARY_REPOS}}|$PRIMARY_REPOS|g")

    if [ -n "$DRY_RUN" ]; then
        echo "  [DRY-RUN] Would write: $OUTPUT_FILE"
        return
    fi

    mkdir -p "$(dirname "$OUTPUT_FILE")"
    echo "$CONTENT" > "$OUTPUT_FILE"
    echo "  OK: $OUTPUT_FILE"
}

# --- Generate files ---
echo "Generating configuration..."

# settings.json
apply_template "$SCRIPT_DIR/templates/settings.json.tmpl" "$TARGET/settings.json"

# safety_guard.sh
apply_template "$SCRIPT_DIR/templates/hooks/safety_guard.sh.tmpl" "$TARGET/hooks/safety_guard.sh"

# post_compact.sh
apply_template "$SCRIPT_DIR/templates/hooks/post_compact.sh.tmpl" "$TARGET/hooks/post_compact.sh"

# pre_compact.sh — needs complex block replacements
TMPL="$SCRIPT_DIR/templates/hooks/pre_compact.sh.tmpl"
if [ -f "$TMPL" ]; then
    CONTENT=$(cat "$TMPL")
    CONTENT=$(echo "$CONTENT" | sed "s|{{NODE_ID}}|$NODE_ID|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PROJECT_DIR}}|$PROJECT_DIR|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PRIMARY_REPO_PATH}}|$PROJECT_DIR/$PRIMARY_REPO|g")

    # Write intermediate, then replace block placeholders with node
    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$TARGET/hooks"
        TMPFILE=$(mktemp)
        echo "$CONTENT" > "$TMPFILE"
        node -e "
let c = require('fs').readFileSync(process.argv[1], 'utf8');
const dirty = Buffer.from('$REPOS_DIRTY_B64', 'base64').toString();
const state = Buffer.from('$REPOS_STATE_B64', 'base64').toString();
const semantic = Buffer.from('$REPOS_SEMANTIC_B64', 'base64').toString();
c = c.replace('{{REPOS_DIRTY_CHECK}}', dirty);
c = c.replace('{{REPOS_STATE_CALLS}}', state);
c = c.replace('{{REPOS_SEMANTIC_CHECK}}', semantic);
process.stdout.write(c);
" "$TMPFILE" > "$TARGET/hooks/pre_compact.sh"
        rm -f "$TMPFILE"
        echo "  OK: $TARGET/hooks/pre_compact.sh"
    else
        echo "  [DRY-RUN] Would write: $TARGET/hooks/pre_compact.sh"
    fi
fi

# system_awareness.sh — needs complex block replacements
TMPL="$SCRIPT_DIR/templates/hooks/system_awareness.sh.tmpl"
if [ -f "$TMPL" ]; then
    CONTENT=$(cat "$TMPL")
    CONTENT=$(echo "$CONTENT" | sed "s|{{NODE_ID}}|$NODE_ID|g")
    CONTENT=$(echo "$CONTENT" | sed "s|{{PROJECT_DIR}}|$PROJECT_DIR|g")

    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$TARGET/hooks"
        TMPFILE=$(mktemp)
        echo "$CONTENT" > "$TMPFILE"
        # Write block arguments to temp files (too large for argv on some systems)
        TMPSIN=$(mktemp); echo "$SINAPSI_BLOCK" > "$TMPSIN"
        TMPEXT=$(mktemp); echo "$EXTRA_HEALTH" > "$TMPEXT"
        TMPWRN=$(mktemp); echo "$EXTRA_WARNINGS" > "$TMPWRN"
        node -e "
const fs = require('fs');
let c = fs.readFileSync(process.argv[1], 'utf8');
const reposArray = Buffer.from('$REPOS_ARRAY', 'base64').toString();
const sinapsi = fs.readFileSync(process.argv[2], 'utf8').trim();
const extra = fs.readFileSync(process.argv[3], 'utf8').trim();
const warnings = fs.readFileSync(process.argv[4], 'utf8').trim();
c = c.replace('{{REPOS_ARRAY}}', reposArray);
c = c.replace('{{SINAPSI_BLOCK}}', sinapsi);
c = c.replace('{{EXTRA_HEALTH_CHECKS}}', extra);
c = c.replace('{{EXTRA_WARNINGS}}', warnings);
process.stdout.write(c);
" "$TMPFILE" "$TMPSIN" "$TMPEXT" "$TMPWRN" > "$TARGET/hooks/system_awareness.sh"
        rm -f "$TMPFILE" "$TMPSIN" "$TMPEXT" "$TMPWRN"
        echo "  OK: $TARGET/hooks/system_awareness.sh"
    else
        echo "  [DRY-RUN] Would write: $TARGET/hooks/system_awareness.sh"
    fi
fi

# statusline_bridge.js + .sh
apply_template "$SCRIPT_DIR/templates/hooks/statusline_bridge.js.tmpl" "$TARGET/hooks/statusline_bridge.js"
apply_template "$SCRIPT_DIR/templates/hooks/statusline_bridge.sh.tmpl" "$TARGET/hooks/statusline_bridge.sh"

# context_awareness.sh
apply_template "$SCRIPT_DIR/templates/hooks/context_awareness.sh.tmpl" "$TARGET/hooks/context_awareness.sh"

# share_reflex.sh
apply_template "$SCRIPT_DIR/templates/hooks/share_reflex.sh.tmpl" "$TARGET/hooks/share_reflex.sh"

# cascade_check.sh
apply_template "$SCRIPT_DIR/templates/hooks/cascade_check.sh.tmpl" "$TARGET/hooks/cascade_check.sh"

# temporal_awareness.sh
apply_template "$SCRIPT_DIR/templates/hooks/temporal_awareness.sh.tmpl" "$TARGET/hooks/temporal_awareness.sh"

# session_thread.sh + thread_task.sh
apply_template "$SCRIPT_DIR/templates/hooks/session_thread.sh.tmpl" "$TARGET/hooks/session_thread.sh"
apply_template "$SCRIPT_DIR/templates/hooks/thread_task.sh.tmpl" "$TARGET/hooks/thread_task.sh"

# youtube-transcript skill (only if THIA_PATH is set)
if [ -n "$THIA_PATH" ]; then
    apply_template "$SCRIPT_DIR/templates/skills/youtube-transcript/SKILL.md.tmpl" "$TARGET/skills/youtube-transcript/SKILL.md"
else
    echo "  SKIP: youtube-transcript (no THIA_PATH in profile)"
fi

# --- Godel plugin ---
if [ -n "$GODEL_ENABLED" ]; then
    echo ""
    echo "Installing Godel plugin..."
    GODEL_SRC="$SCRIPT_DIR/plugins/godel"
    GODEL_DST="$PROJECT_DIR/godel"

    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$GODEL_DST"
        # Copy core files
        for F in bridge.js ask.js setup.js package.json IDENTITY.md.tmpl README.md; do
            cp "$GODEL_SRC/$F" "$GODEL_DST/" 2>/dev/null
        done
        # Copy examples
        cp -r "$GODEL_SRC/examples" "$GODEL_DST/" 2>/dev/null
        # Copy plugin manifest
        mkdir -p "$GODEL_DST/.claude-plugin"
        cp "$GODEL_SRC/.claude-plugin/plugin.json" "$GODEL_DST/.claude-plugin/" 2>/dev/null

        # Auto-configure if example or domain is specified
        if [ -n "$GODEL_EXAMPLE" ]; then
            (cd "$GODEL_DST" && node setup.js --example "$GODEL_EXAMPLE") 2>/dev/null
            echo "  OK: Godel configured from example '$GODEL_EXAMPLE'"
        elif [ -n "$GODEL_DOMAIN" ]; then
            SETUP_ARGS="--domain \"$GODEL_DOMAIN\""
            [ -n "$GODEL_NAME" ] && SETUP_ARGS="--name \"$GODEL_NAME\" $SETUP_ARGS"
            [ -n "$GODEL_DESC" ] && SETUP_ARGS="$SETUP_ARGS --desc \"$GODEL_DESC\""
            (cd "$GODEL_DST" && eval node setup.js $SETUP_ARGS) 2>/dev/null
            echo "  OK: Godel configured for domain '$GODEL_DOMAIN'"
        else
            echo "  OK: Godel copied (run 'node godel/setup.js' to configure)"
        fi

        echo "  Files: $GODEL_DST/"
        echo "  Port: ${GODEL_PORT:-3004}"
        echo "  Start: cd $GODEL_DST && node bridge.js"
    else
        echo "  [DRY-RUN] Would install Godel to: $GODEL_DST/"
    fi
else
    echo ""
    echo "SKIP: Godel plugin (add 'godel.enabled: true' to profile to install)"
fi

# --- Set permissions ---
if [ -z "$DRY_RUN" ]; then
    chmod +x "$TARGET/hooks/"*.sh 2>/dev/null
    echo ""
    echo "Permissions set (chmod +x on hooks)."
fi

# --- Preserve settings.local.json ---
if [ ! -f "$TARGET/settings.local.json" ]; then
    if [ -z "$DRY_RUN" ]; then
        cat > "$TARGET/settings.local.json" << 'PERM'
{
  "permissions": {
    "allow": []
  }
}
PERM
        echo "Created empty settings.local.json (add permissions as needed)."
    fi
else
    echo "settings.local.json already exists — not touched."
fi

echo ""
echo "=== Seed installed for $NODE_ID at $TARGET ==="
echo ""
echo "Next steps:"
echo "  1. Review generated files in $TARGET/"
echo "  2. Configure permissions in $TARGET/settings.local.json"
if [ -n "$GODEL_ENABLED" ]; then
echo "  3. Set ANTHROPIC_API_KEY (or OPENROUTER_API_KEY) for Godel"
echo "  4. Start Godel: cd $PROJECT_DIR/godel && node bridge.js"
echo "  5. Start a new Claude Code session — hooks will activate automatically"
else
echo "  3. Start a new Claude Code session — hooks will activate automatically"
fi
