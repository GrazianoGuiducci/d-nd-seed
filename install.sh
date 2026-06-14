#!/bin/bash
# ============================================================================
# D-ND SEED INSTALLER
# ============================================================================
# Generates a neutral .seed/ manifest plus .claude/ adapter configuration.
# The seed reads the profile, adapts the templates, writes the output.
#
# Usage:
#   ./install.sh <profile.json>
#   ./install.sh profiles/example-origin-node.json
#   ./install.sh profiles/example.json --dry-run
#   ./install.sh profiles/example.json --plan
#   ./install.sh --check
#   ./install.sh profiles/example.json --legacy-all
#
# Requirements: bash, node (for JSON parsing)
# ============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROFILE="$1"
DRY_RUN=""
PLAN_MODE=""
CHECK_MODE=""
LEGACY_ALL=""

UPDATE_MODE=""
for arg in "$@"; do
    [ "$arg" = "--dry-run" ] && DRY_RUN="true"
    [ "$arg" = "--update" ] && UPDATE_MODE="true"
    [ "$arg" = "--plan" ] && PLAN_MODE="true"
    [ "$arg" = "--check" ] && CHECK_MODE="true"
    [ "$arg" = "--legacy-all" ] && LEGACY_ALL="true"
done

TEMP_FILES=""
cleanup() {
    if [ -n "$TEMP_FILES" ]; then
        rm -f $TEMP_FILES 2>/dev/null || true
    fi
}
trap cleanup EXIT

make_temp() {
    local f
    f=$(mktemp)
    TEMP_FILES="$TEMP_FILES $f"
    printf '%s\n' "$f"
}

require_node() {
    if ! command -v node >/dev/null 2>&1; then
        echo "ERROR: node is required for this command but was not found in PATH"
        exit 1
    fi
}

if [ -n "$CHECK_MODE" ]; then
    require_node
    node "$SCRIPT_DIR/scripts/validate_capability_registry.js"
    exit $?
fi

if [ -z "$PROFILE" ]; then
    echo "D-ND Seed Installer"
    echo ""
    echo "Usage: ./install.sh <profile.json> [--dry-run] [--update]"
    echo ""
    echo "  --dry-run   Show what would be written without changing anything"
    echo "  --plan      Show routed installer options without writing anything"
    echo "  --check     Validate the seed capability registry"
    echo "  --legacy-all Install all legacy hooks/skills instead of routed capabilities"
    echo "  --update    Only add NEW files. Existing files are preserved."
    echo "              Changed files are saved as .new for manual review."
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

if [ -n "$PLAN_MODE" ]; then
    require_node
    node "$SCRIPT_DIR/scripts/validate_profile.js" "$PROFILE" --target-policy=read-only >/dev/null
    node "$SCRIPT_DIR/scripts/installer_option_router.js" "$PROFILE"
    exit $?
fi

require_node
node "$SCRIPT_DIR/scripts/validate_capability_registry.js" >/dev/null

UNAME_S="$(uname -s 2>/dev/null || echo unknown)"
WINDOWS_BASH=""
case "$UNAME_S" in
    MINGW*|MSYS*|CYGWIN*) WINDOWS_BASH="true" ;;
esac

if [ -n "$WINDOWS_BASH" ] && [ -z "$DRY_RUN" ] && [ "${DND_SEED_ALLOW_WINDOWS_BASH:-}" != "1" ]; then
    echo "ERROR: Windows Bash runtime detected."
    echo "Refusing to write files unless DND_SEED_ALLOW_WINDOWS_BASH=1 is set."
    echo "Use Node read-only checks first:"
    echo "  node scripts\\validate_capability_registry.js"
    echo "  node scripts\\installer_option_router.js <profile.json>"
    exit 1
fi

TARGET_POLICY="write"
[ -n "$DRY_RUN" ] && TARGET_POLICY="dry-run"
node "$SCRIPT_DIR/scripts/validate_profile.js" "$PROFILE" --target-policy="$TARGET_POLICY" >/dev/null

PLAN_FILE=""
INCLUDED_PATHS_FILE=""
if [ -z "$LEGACY_ALL" ]; then
    PLAN_FILE=$(make_temp)
    INCLUDED_PATHS_FILE=$(make_temp)
    node "$SCRIPT_DIR/scripts/installer_option_router.js" "$PROFILE" --json > "$PLAN_FILE"
    node "$SCRIPT_DIR/scripts/installer_option_router.js" "$PROFILE" --paths > "$INCLUDED_PATHS_FILE"
    echo "Registry gate: enabled"
    echo "Plan: $(node -e "const p=require('fs').readFileSync(process.argv[1],'utf8'); const d=JSON.parse(p); console.log(d.included.length+' included, '+d.withheld.length+' withheld by risk, '+d.available.length+' available')" "$PLAN_FILE")"
    echo ""
else
    echo "Registry gate: bypassed with --legacy-all"
    echo ""
fi

capability_selected() {
    local rel="$1"
    if [ -n "$LEGACY_ALL" ]; then
        return 0
    fi
    grep -Fxq "$rel" "$INCLUDED_PATHS_FILE"
}

skip_unselected() {
    local label="$1"
    local rel="$2"
    if capability_selected "$rel"; then
        return 1
    fi
    echo "  SKIP: $label (not selected by registry plan)"
    return 0
}

echo "=== D-ND Seed Installer ==="
echo "Profile: $PROFILE"
echo ""

# --- Parse profile with node ---
profile_value() {
    node - "$PROFILE" "$1" "$2" <<'NODE'
const fs = require('fs');
const profilePath = process.argv[2];
const key = process.argv[3];
const fallback = process.argv[4] || '';
const p = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const g = p.godel || {};
const values = {
  node_id: p.node_id || 'UNKNOWN',
  project_dir: p.project_dir || '.',
  system_path: p.system_path || '',
  memory_path: p.memory_path || '',
  vps_url: p.vps_url || '',
  sinapsi_for: p.sinapsi_for || p.sync_for || '',
  godel_enabled: g.enabled ? 'true' : '',
  godel_example: g.example || '',
  godel_name: g.name || '',
  godel_domain: g.domain || '',
  godel_desc: g.description || '',
  godel_port: String(g.port || '3004'),
  primary_repo: (p.repos && p.repos[0] && p.repos[0].path) || '',
  primary_repos: (p.repos || []).slice(0, 3).map(r => r.path || '').join(' ')
};
process.stdout.write(String(values[key] ?? fallback));
NODE
}

profile_block_b64() {
    node - "$PROFILE" "$1" <<'NODE'
const fs = require('fs');
const profilePath = process.argv[2];
const key = process.argv[3];
const p = JSON.parse(fs.readFileSync(profilePath, 'utf8'));
const repos = p.repos || [];
const q = value => String(value || '').replace(/"/g, '\\"');
let out = '';
if (key === 'repos_array') {
  out = repos.map(r => `    "${q(r.name)}:${q(r.path)}:${q(r.branch)}"`).join('\n');
} else if (key === 'repos_dirty') {
  out = repos.map(r =>
    `for R in "$PROJECT_DIR/${q(r.path)}"; do\n` +
    '    if [ -d "$R/.git" ]; then\n' +
    '        D=$(git -C "$R" diff --name-only 2>/dev/null)\n' +
    '        if [ -n "$D" ]; then HAS_DIRTY="yes"; fi\n' +
    '    fi\n' +
    'done'
  ).join('\n');
} else if (key === 'repos_state') {
  out = repos.map(r => `repo_state "${q(r.name)}" "$PROJECT_DIR/${q(r.path)}"`).join('\n');
} else if (key === 'repos_semantic') {
  out = repos.map(r =>
    `if [ -d "$PROJECT_DIR/${q(r.path)}/.git" ]; then\n` +
    `    UNPUSHED=$(git -C "$PROJECT_DIR/${q(r.path)}" log --oneline @{upstream}..HEAD 2>/dev/null | head -3)\n` +
    `    if [ -n "$UNPUSHED" ]; then SEMANTIC_TAGS="\${SEMANTIC_TAGS}DEPLOY(${q(r.name)}) "; fi\n` +
    'fi'
  ).join('\n');
}
process.stdout.write(Buffer.from(out).toString('base64'));
NODE
}

reject_control_value() {
    local label="$1"
    local value="$2"
    case "$value" in
        *$'\n'*|*$'\r'*|*'`'*|*'$'*|*';'*|*'&'*|*'|'*|*'<'*|*'>'*)
            echo "ERROR: Unsafe profile value for $label"
            exit 1
            ;;
    esac
}

NODE_ID=$(profile_value node_id UNKNOWN)
PROJECT_DIR=$(profile_value project_dir .)
SYSTEM_PATH=$(profile_value system_path "")
MEMORY_PATH=$(profile_value memory_path "")
VPS_URL=$(profile_value vps_url "")
SINAPSI_FOR=$(profile_value sinapsi_for "")
GODEL_ENABLED=$(profile_value godel_enabled "")
GODEL_EXAMPLE=$(profile_value godel_example "")
GODEL_NAME=$(profile_value godel_name "")
GODEL_DOMAIN=$(profile_value godel_domain "")
GODEL_DESC=$(profile_value godel_desc "")
GODEL_PORT=$(profile_value godel_port "3004")
REPOS_ARRAY=$(profile_block_b64 repos_array)
PRIMARY_REPO=$(profile_value primary_repo "")
PRIMARY_REPOS=$(profile_value primary_repos "")
REPOS_DIRTY_B64=$(profile_block_b64 repos_dirty)
REPOS_STATE_B64=$(profile_block_b64 repos_state)
REPOS_SEMANTIC_B64=$(profile_block_b64 repos_semantic)

reject_control_value "node_id" "$NODE_ID"
reject_control_value "project_dir" "$PROJECT_DIR"
reject_control_value "system_path" "$SYSTEM_PATH"
reject_control_value "memory_path" "$MEMORY_PATH"
reject_control_value "vps_url" "$VPS_URL"
reject_control_value "sinapsi_for" "$SINAPSI_FOR"
reject_control_value "godel_example" "$GODEL_EXAMPLE"
reject_control_value "godel_name" "$GODEL_NAME"
reject_control_value "godel_domain" "$GODEL_DOMAIN"
reject_control_value "godel_desc" "$GODEL_DESC"
reject_control_value "primary_repo" "$PRIMARY_REPO"
reject_control_value "primary_repos" "$PRIMARY_REPOS"

if [ -z "$DRY_RUN" ] && [ "$PROJECT_DIR" = "/path/to/your/project" ]; then
    echo "ERROR: Refusing to install to placeholder project_dir: $PROJECT_DIR"
    echo "Copy a profile and set project_dir to the intended target first."
    exit 1
fi

case "$PROJECT_DIR" in
    ""|"/"|"\\"|"C:"|"C:\\"|"C:/"|".."|"../"*)
        echo "ERROR: Refusing unsafe project_dir: $PROJECT_DIR"
        exit 1
        ;;
esac

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
NEUTRAL_TARGET="$PROJECT_DIR/.seed"

# --- Generate sync block for system_awareness ---
SINAPSI_BLOCK=""
if [ -n "$VPS_URL" ] && [ -n "$SINAPSI_FOR" ]; then
    SINAPSI_BLOCK="# --- Inter-node: unread messages ---
echo \"## Messages (unread for $SINAPSI_FOR)\"
SINAPSI=\$(curl -s --max-time 5 \"$VPS_URL/api/sync?for=$SINAPSI_FOR&unread=true\" -H \"X-Auth-Token: \${DND_API_TOKEN}\" 2>/dev/null)
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
CONTAINER_STATUS=\$(docker ps --filter \"name=\${DND_CONTAINER_NAME:-app}\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null)
if [ -n \"\$CONTAINER_STATUS\" ]; then
    echo \"  \$CONTAINER_STATUS\"
else
    echo \"  \${DND_CONTAINER_NAME:-app}: NOT RUNNING\"
fi
echo \"\"

# --- Node Bridge status ---
echo \"## Node Bridge\"
BRIDGE_STATUS=\$(systemctl is-active \${DND_BRIDGE_SERVICE:-node-bridge} 2>/dev/null || echo \"unknown\")
echo \"  \${DND_BRIDGE_SERVICE:-node-bridge}: \$BRIDGE_STATUS\"
echo \"\""
fi

# API health check
if [ -n "$VPS_URL" ]; then
    EXTRA_HEALTH="$EXTRA_HEALTH
# --- API Health ---
echo \"## API Health\"
HEALTH=\$(curl -s --max-time 5 \"$VPS_URL/api/status\" -H \"X-Auth-Token: \${DND_API_TOKEN}\" 2>/dev/null)
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

    CONTENT=$(TMPL_FILE="$TMPL_FILE" NODE_ID="$NODE_ID" PROJECT_DIR="$PROJECT_DIR" SYSTEM_PATH="$SYSTEM_PATH" PRIMARY_REPO_PATH="$PROJECT_DIR/$PRIMARY_REPO" PRIMARY_REPOS="$PRIMARY_REPOS" node <<'NODE'
const fs = require('fs');
let content = fs.readFileSync(process.env.TMPL_FILE, 'utf8');
const replacements = {
  NODE_ID: process.env.NODE_ID || '',
  PROJECT_DIR: process.env.PROJECT_DIR || '',
  SYSTEM_PATH: process.env.SYSTEM_PATH || '',
  PRIMARY_REPO_PATH: process.env.PRIMARY_REPO_PATH || '',
  PRIMARY_REPOS: process.env.PRIMARY_REPOS || ''
};
for (const [key, value] of Object.entries(replacements)) {
  content = content.split(`{{${key}}}`).join(value);
}
process.stdout.write(content);
NODE
)

    if [ -n "$DRY_RUN" ]; then
        if [ -f "$OUTPUT_FILE" ]; then
            echo "  [DRY-RUN] EXISTS: $OUTPUT_FILE (would skip in --update)"
        else
            echo "  [DRY-RUN] NEW: $OUTPUT_FILE"
        fi
        return
    fi

    mkdir -p "$(dirname "$OUTPUT_FILE")"

    # In update mode: don't overwrite existing files — save as .new
    if [ -n "$UPDATE_MODE" ] && [ -f "$OUTPUT_FILE" ]; then
        # Check if content is different
        EXISTING=$(cat "$OUTPUT_FILE")
        if [ "$EXISTING" = "$CONTENT" ]; then
            echo "  SAME: $OUTPUT_FILE (unchanged)"
        else
            echo "$CONTENT" > "${OUTPUT_FILE}.new"
            echo "  UPDATE: ${OUTPUT_FILE}.new (review and merge manually)"
        fi
        return
    fi

    echo "$CONTENT" > "$OUTPUT_FILE"
    echo "  OK: $OUTPUT_FILE"
}

# --- Generate files ---
echo "Generating configuration..."

# settings.json
apply_template "$SCRIPT_DIR/templates/settings.json.tmpl" "$TARGET/settings.json"
if [ -z "$DRY_RUN" ]; then
    node - "$TARGET/settings.json" "$INCLUDED_PATHS_FILE" "$LEGACY_ALL" <<'NODE'
const fs = require('fs');
const settingsPath = process.argv[2];
const includedFile = process.argv[3] || '';
const legacyAll = process.argv[4] === 'true';

const settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
const included = new Set();
if (legacyAll) {
  included.add('*');
} else if (includedFile && fs.existsSync(includedFile)) {
  for (const line of fs.readFileSync(includedFile, 'utf8').split(/\r?\n/)) {
    if (line.trim()) included.add(line.trim());
  }
}

const selected = rel => legacyAll || included.has(rel);
const hookPathByCommand = [
  ['session_monitor.py', 'templates/hooks/session_monitor.py.tmpl'],
  ['safety_guard.sh', 'templates/hooks/safety_guard.sh.tmpl'],
  ['pre_compact.sh', 'templates/hooks/pre_compact.sh.tmpl'],
  ['post_compact.sh', 'templates/hooks/post_compact.sh.tmpl'],
  ['statusline_bridge.js', 'templates/hooks/statusline_bridge.js.tmpl'],
  ['statusline_bridge.sh', 'templates/hooks/statusline_bridge.sh.tmpl'],
  ['system_awareness.sh', 'templates/hooks/system_awareness.sh.tmpl'],
  ['cea_hook.sh', 'templates/hooks/cea_hook.sh.tmpl'],
  ['share_reflex.sh', 'templates/hooks/share_reflex.sh.tmpl'],
  ['cascade_check.sh', 'templates/hooks/cascade_check.sh.tmpl'],
  ['session_thread.sh', 'templates/hooks/session_thread.sh.tmpl'],
];

function commandAllowed(command) {
  for (const [needle, rel] of hookPathByCommand) {
    if (command.includes(needle)) return selected(rel);
  }
  return true;
}

if (settings.statusLine && settings.statusLine.command && !commandAllowed(settings.statusLine.command)) {
  delete settings.statusLine;
}

if (settings.hooks) {
  for (const eventName of Object.keys(settings.hooks)) {
    const eventHooks = settings.hooks[eventName]
      .map(group => {
        const hooks = (group.hooks || []).filter(hook => {
          if (hook.type !== 'command' || !hook.command) return true;
          return commandAllowed(hook.command);
        });
        return { ...group, hooks };
      })
      .filter(group => (group.hooks || []).length > 0);

    if (eventHooks.length) settings.hooks[eventName] = eventHooks;
    else delete settings.hooks[eventName];
  }
}

fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
NODE
fi

# safety_guard.sh
if ! skip_unselected "safety_guard.sh" "templates/hooks/safety_guard.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/safety_guard.sh.tmpl" "$TARGET/hooks/safety_guard.sh"
fi

# post_compact.sh
if ! skip_unselected "post_compact.sh" "templates/hooks/post_compact.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/post_compact.sh.tmpl" "$TARGET/hooks/post_compact.sh"
fi

# pre_compact.sh — needs complex block replacements
TMPL="$SCRIPT_DIR/templates/hooks/pre_compact.sh.tmpl"
if [ -f "$TMPL" ] && capability_selected "templates/hooks/pre_compact.sh.tmpl"; then
    CONTENT=$(TMPL_FILE="$TMPL" NODE_ID="$NODE_ID" PROJECT_DIR="$PROJECT_DIR" PRIMARY_REPO_PATH="$PROJECT_DIR/$PRIMARY_REPO" node <<'NODE'
const fs = require('fs');
let content = fs.readFileSync(process.env.TMPL_FILE, 'utf8');
const replacements = {
  NODE_ID: process.env.NODE_ID || '',
  PROJECT_DIR: process.env.PROJECT_DIR || '',
  PRIMARY_REPO_PATH: process.env.PRIMARY_REPO_PATH || ''
};
for (const [key, value] of Object.entries(replacements)) {
  content = content.split(`{{${key}}}`).join(value);
}
process.stdout.write(content);
NODE
)

    # Write intermediate, then replace block placeholders with node
    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$TARGET/hooks"
        TMPFILE=$(make_temp)
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
if [ -f "$TMPL" ] && capability_selected "templates/hooks/system_awareness.sh.tmpl"; then
    CONTENT=$(TMPL_FILE="$TMPL" NODE_ID="$NODE_ID" PROJECT_DIR="$PROJECT_DIR" node <<'NODE'
const fs = require('fs');
let content = fs.readFileSync(process.env.TMPL_FILE, 'utf8');
const replacements = {
  NODE_ID: process.env.NODE_ID || '',
  PROJECT_DIR: process.env.PROJECT_DIR || ''
};
for (const [key, value] of Object.entries(replacements)) {
  content = content.split(`{{${key}}}`).join(value);
}
process.stdout.write(content);
NODE
)

    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$TARGET/hooks"
        TMPFILE=$(make_temp)
        echo "$CONTENT" > "$TMPFILE"
        # Write block arguments to temp files (too large for argv on some systems)
        TMPSIN=$(make_temp); echo "$SINAPSI_BLOCK" > "$TMPSIN"
        TMPEXT=$(make_temp); echo "$EXTRA_HEALTH" > "$TMPEXT"
        TMPWRN=$(make_temp); echo "$EXTRA_WARNINGS" > "$TMPWRN"
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
if ! skip_unselected "statusline_bridge.js" "templates/hooks/statusline_bridge.js.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/statusline_bridge.js.tmpl" "$TARGET/hooks/statusline_bridge.js"
fi
if ! skip_unselected "statusline_bridge.sh" "templates/hooks/statusline_bridge.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/statusline_bridge.sh.tmpl" "$TARGET/hooks/statusline_bridge.sh"
fi

# context_awareness.sh
if ! skip_unselected "context_awareness.sh" "templates/hooks/context_awareness.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/context_awareness.sh.tmpl" "$TARGET/hooks/context_awareness.sh"
fi

# cea_hook.sh + awareness templates
if ! skip_unselected "cea_hook.sh" "templates/hooks/cea_hook.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/cea_hook.sh.tmpl" "$TARGET/hooks/cea_hook.sh"
    apply_template "$SCRIPT_DIR/templates/awareness.json.tmpl" "$TARGET/hooks/awareness.json.example"
    apply_template "$SCRIPT_DIR/templates/awareness_map.json.tmpl" "$TARGET/hooks/awareness_map.json.example"
fi

# share_reflex.sh
if ! skip_unselected "share_reflex.sh" "templates/hooks/share_reflex.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/share_reflex.sh.tmpl" "$TARGET/hooks/share_reflex.sh"
fi

# cascade_check.sh
if ! skip_unselected "cascade_check.sh" "templates/hooks/cascade_check.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/cascade_check.sh.tmpl" "$TARGET/hooks/cascade_check.sh"
fi

# temporal_awareness.sh
if ! skip_unselected "temporal_awareness.sh" "templates/hooks/temporal_awareness.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/temporal_awareness.sh.tmpl" "$TARGET/hooks/temporal_awareness.sh"
fi

# session_thread.sh + thread_task.sh
if ! skip_unselected "session_thread.sh" "templates/hooks/session_thread.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/session_thread.sh.tmpl" "$TARGET/hooks/session_thread.sh"
fi
if ! skip_unselected "thread_task.sh" "templates/hooks/thread_task.sh.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/hooks/thread_task.sh.tmpl" "$TARGET/hooks/thread_task.sh"
fi

# Any selected hook template not handled above.
for tmpl in "$SCRIPT_DIR"/templates/hooks/*.tmpl; do
    [ -f "$tmpl" ] || continue
    name=$(basename "$tmpl" .tmpl)
    case "$name" in
        safety_guard.sh|post_compact.sh|pre_compact.sh|system_awareness.sh|statusline_bridge.js|statusline_bridge.sh|context_awareness.sh|cea_hook.sh|share_reflex.sh|cascade_check.sh|temporal_awareness.sh|session_thread.sh|thread_task.sh)
            continue
            ;;
    esac
    if ! skip_unselected "$name" "templates/hooks/$name.tmpl"; then
        apply_template "$tmpl" "$TARGET/hooks/$name"
    fi
done

# youtube-transcript is currently reference-only. This branch stays registry-gated
# so a future promotion cannot bypass the routed install contract.
if ! skip_unselected "youtube-transcript" "templates/skills/youtube-transcript/SKILL.md.tmpl"; then
    apply_template "$SCRIPT_DIR/templates/skills/youtube-transcript/SKILL.md.tmpl" "$TARGET/skills/youtube-transcript/SKILL.md"
fi

# --- Core skills from seed ---
echo ""
echo "Installing core skills..."
for skill_dir in "$SCRIPT_DIR"/plugins/d-nd-core/skills/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")
    if ! capability_selected "plugins/d-nd-core/skills/$name"; then
        echo "  SKIP: $name (not selected by registry plan)"
        continue
    fi
    skill_target="$TARGET/skills/$name"

    if [ -n "$DRY_RUN" ]; then
        if [ -d "$skill_target" ]; then
            echo "  [DRY-RUN] EXISTS: $skill_target/"
        else
            echo "  [DRY-RUN] NEW: $skill_target/"
        fi
        continue
    fi

    if [ -n "$UPDATE_MODE" ] && [ -d "$skill_target" ]; then
        echo "  SAME: $name (already installed)"
    else
        mkdir -p "$skill_target"
        cp -r "$skill_dir"* "$skill_target/" 2>/dev/null
        echo "  OK: $name"
    fi
done

# --- Projector scripts (copy to accessible location) ---
PROJECTOR_SRC="$SCRIPT_DIR/plugins/d-nd-core/scripts"
PROJECTOR_DST="$PROJECT_DIR/d-nd-tools"
if [ -f "$PROJECTOR_SRC/scenario_projector.py" ]; then
    echo ""
    echo "Installing projector tools..."
    if ! capability_selected "plugins/d-nd-core/skills/scenario-projector"; then
        echo "  SKIP: projector tools (scenario-projector not selected by registry plan)"
    elif [ -z "$DRY_RUN" ]; then
        mkdir -p "$PROJECTOR_DST/examples"
        cp "$PROJECTOR_SRC/scenario_projector.py" "$PROJECTOR_DST/"
        cp "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" "$PROJECTOR_DST/" 2>/dev/null
        # Copy domain pre-configs and automation pattern
        for f in "$PROJECTOR_SRC"/examples/*.json "$PROJECTOR_SRC"/examples/*.py "$PROJECTOR_SRC"/examples/*.md; do
            [ -f "$f" ] && cp "$f" "$PROJECTOR_DST/examples/"
        done
        echo "  OK: $PROJECTOR_DST/ (projector + ${#} domain seeds + automation pattern)"
        echo "  Usage: python $PROJECTOR_DST/scenario_projector.py --help"
    else
        echo "  [DRY-RUN] Would install projector to: $PROJECTOR_DST/"
    fi
fi

# --- Godel plugin ---
if [ -n "$GODEL_ENABLED" ]; then
    echo ""
    echo "Installing Godel plugin..."
    GODEL_SRC="$SCRIPT_DIR/plugins/godel"
    GODEL_DST="$PROJECT_DIR/godel"

    if ! capability_selected "plugins/godel"; then
        echo "  SKIP: Godel plugin (not selected by registry plan)"
    elif [ -z "$DRY_RUN" ]; then
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
            SETUP_ARGS=(--domain "$GODEL_DOMAIN")
            [ -n "$GODEL_NAME" ] && SETUP_ARGS=(--name "$GODEL_NAME" "${SETUP_ARGS[@]}")
            [ -n "$GODEL_DESC" ] && SETUP_ARGS=("${SETUP_ARGS[@]}" --desc "$GODEL_DESC")
            (cd "$GODEL_DST" && node setup.js "${SETUP_ARGS[@]}") 2>/dev/null
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

# --- Save profile reference for update.sh ---
if [ -z "$DRY_RUN" ]; then
    mkdir -p "$NEUTRAL_TARGET/memory"
    cp "$PROFILE" "$TARGET/seed_profile.json" 2>/dev/null
    echo "Profile saved to $TARGET/seed_profile.json (for update.sh)."
    cp "$PROFILE" "$NEUTRAL_TARGET/seed_profile.json" 2>/dev/null
    echo "Neutral profile saved to $NEUTRAL_TARGET/seed_profile.json."
    if [ -n "$PLAN_FILE" ]; then
        cp "$PLAN_FILE" "$TARGET/seed_install_plan.json" 2>/dev/null
        echo "Install plan saved to $TARGET/seed_install_plan.json."
        cp "$PLAN_FILE" "$NEUTRAL_TARGET/seed_install_plan.json" 2>/dev/null
        echo "Neutral install plan saved to $NEUTRAL_TARGET/seed_install_plan.json."
    fi
    cat > "$NEUTRAL_TARGET/adapter_notes.md" << NOTES
# Seed Adapter Notes

This .seed directory is the runtime-neutral recognition surface for the
installed Seed.

.claude remains the Claude Code adapter and compatibility surface.
Other runtimes should read seed_profile.json and seed_install_plan.json here,
then map selected capabilities to their own native, adapted, documented or
unsupported behavior.

Related design resources:
- UX/UI/design seeds: https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed
- Public examples and adoption context: https://d-nd.com
NOTES
else
    echo "[DRY-RUN] Would save neutral Seed manifest to $NEUTRAL_TARGET/"
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

if [ -n "$DRY_RUN" ]; then
    echo ""
    echo "=== Seed dry-run complete for $NODE_ID at $TARGET ==="
    echo ""
    echo "No target files were written."
    echo "Review the plan and rerun without --dry-run only after runtime, profile and target are confirmed."
    echo ""
    echo "Related resources:"
    echo "  UX/UI/design seeds: https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed"
    echo "  Public examples and portfolio: https://d-nd.com"
    exit 0
fi

echo ""
echo "=== Seed installed for $NODE_ID at $TARGET ==="
echo ""
echo "Next steps:"
echo "  1. Review generated files in $TARGET/"
echo "  2. Review neutral manifest in $NEUTRAL_TARGET/"
echo "  3. Configure permissions in $TARGET/settings.local.json"
echo "  4. If this project needs UX/UI/design consistency, inspect:"
echo "     https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed"
echo "     Public examples and portfolio: https://d-nd.com"
STEP=5
if [ -n "$GODEL_ENABLED" ]; then
echo "  $STEP. Set GODEL_API_KEY + GODEL_API_URL for Godel"
STEP=$((STEP + 1))
echo "  $STEP. Start Godel: cd $PROJECT_DIR/godel && node bridge.js"
STEP=$((STEP + 1))
fi
if [ -n "$PROJECTOR_DST" ] && [ -f "$PROJECTOR_SRC/scenario_projector.py" ]; then
echo "  $STEP. Try the projector: python $PROJECTOR_DST/scenario_projector.py --seed $PROJECTOR_DST/examples/startup_strategy.json --action-plan"
STEP=$((STEP + 1))
fi
echo "  $STEP. Start a new Claude Code session — hooks will activate automatically"
