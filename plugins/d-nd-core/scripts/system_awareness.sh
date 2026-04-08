#!/bin/bash
# ============================================================================
# SYSTEM AWARENESS — D-ND Plugin (Parametric)
# ============================================================================
# SessionStart hook: scans repos, messaging, VPS health.
# Adapts to any TMx node via environment variables.
#
# Required env vars:
#   DND_PROJECT_DIR  — base project directory (auto-detected from cwd if missing)
#   DND_NODE_ID      — node identity (e.g. node-1, node-2, dev, prod...)
#
# Optional env vars:
#   DND_VPS_IP       — VPS IP (default: localhost)
#   DND_VPS_PORT     — VPS API port (default: 3002)
#   DND_API_TOKEN    — API authentication token
#   DND_REPOS        — comma-separated list of "name:path:branch" (auto-detected if missing)
# ============================================================================

# --- Config ---
PROJECT_DIR="${DND_PROJECT_DIR:-$(pwd)}"
NODE_ID="${DND_NODE_ID:-unknown}"
TOKEN="${DND_API_TOKEN:-}"
VPS_IP="${DND_VPS_IP:-localhost}"
VPS_PORT="${DND_VPS_PORT:-3002}"
VPS="http://${VPS_IP}:${VPS_PORT}"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
STATE_FILE="${PROJECT_DIR}/.claude/hooks/system_state.md"

echo "=== ${NODE_ID} SYSTEM AWARENESS ==="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Node: ${NODE_ID} | Base: ${PROJECT_DIR}"
echo ""

# --- 1. Messaging ---
echo "## Messaging (unread for ${NODE_ID})"
MSG_DATA=$(curl -s --max-time 5 "$VPS/api/node-sync?for=${NODE_ID}&unread=true" -H "X-Auth-Token: $TOKEN" 2>/dev/null)
if [ $? -eq 0 ] && [ -n "$MSG_DATA" ]; then
    node -e "
const d=$MSG_DATA;
const t=d.total||0;
const now=Date.now();
function age(ts){if(!ts)return'?';const m=Math.round((now-new Date(ts).getTime())/60000);if(m<60)return m+'min ago';const h=Math.round(m/60);if(h<24)return h+'h ago';return Math.round(h/24)+'d ago'}
function hhmm(ts){if(!ts)return'??:??';return new Date(ts).toLocaleTimeString('it-IT',{hour:'2-digit',minute:'2-digit',hour12:false})}
if(t===0){console.log('  No unread messages.')}
else{console.log('  '+t+' unread message(s):');
const oldest=d.messages[0],newest=d.messages[d.messages.length-1];
console.log('  Oldest: '+hhmm(oldest?.timestamp)+' ('+age(oldest?.timestamp)+') | Newest: '+hhmm(newest?.timestamp)+' ('+age(newest?.timestamp)+')');
(d.messages||[]).slice(-10).forEach(m=>{
  console.log('  - ['+m.type+'] '+m.from+'->'+m.to+' @'+hhmm(m.timestamp)+' ('+age(m.timestamp)+'): '+(m.content||'').slice(0,100))
})}
" 2>/dev/null || echo "  Parse error."
else
    echo "  VPS unreachable."
fi
echo ""

# --- 2. Active Repos ---
echo "## Active Repos"

# Auto-detect repos: find all .git directories one level deep
FOUND_REPOS=""
if [ -z "$DND_REPOS" ]; then
    for dir in "$PROJECT_DIR"/*/; do
        if [ -d "$dir/.git" ]; then
            name=$(basename "$dir")
            branch=$(git -C "$dir" branch --show-current 2>/dev/null || echo "main")
            FOUND_REPOS="${FOUND_REPOS}${name}:${name}:${branch},"
        fi
    done
    DND_REPOS="$FOUND_REPOS"
fi

# Write state file header
mkdir -p "$(dirname "$STATE_FILE")" 2>/dev/null
cat > "$STATE_FILE" << HEADER
# System State — Auto-generated
> Last scan: $(date '+%Y-%m-%d %H:%M:%S')
> Node: ${NODE_ID}
> Overwritten every SessionStart by d-nd-core plugin

## Repos
| Repo | Commit | Dirty | Untracked |
|------|--------|-------|-----------|
HEADER

IFS=',' read -ra REPO_LIST <<< "$DND_REPOS"
for entry in "${REPO_LIST[@]}"; do
    [ -z "$entry" ] && continue
    IFS=':' read -r name path branch <<< "$entry"
    dir="$PROJECT_DIR/$path"

    if [ ! -d "$dir/.git" ]; then
        echo "  $name: [no git]"
        echo "| $name | — | — | — |" >> "$STATE_FILE"
        continue
    fi

    commit=$(git -C "$dir" rev-parse --short HEAD 2>/dev/null || echo "???")
    dirty=$(git -C "$dir" diff --name-only 2>/dev/null | wc -l | tr -d ' ')
    untracked=$(git -C "$dir" ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')

    status="$commit"
    [ "$dirty" -gt 0 ] 2>/dev/null && status="$status | dirty:$dirty"
    [ "$untracked" -gt 0 ] 2>/dev/null && status="$status | new:$untracked"

    echo "  $name: $status"
    echo "| $name | $commit | $dirty | $untracked |" >> "$STATE_FILE"
done
echo ""

# --- 3. VPS health ---
echo "## VPS Health"
HEALTH=$(curl -s --max-time 5 "$VPS/api/status" -H "X-Auth-Token: $TOKEN" 2>/dev/null)
VPS_STATUS="unreachable"
if [ $? -eq 0 ] && [ -n "$HEALTH" ]; then
    VPS_STATUS=$(node -e "
const d=$HEALTH;
const h=Math.floor((d.uptime||0)/3600);
const m=Math.floor(((d.uptime||0)%3600)/60);
console.log((d.status||'unknown')+' | Model: '+(d.model||'unknown')+' | Uptime: '+h+'h'+m+'m')
" 2>/dev/null || echo "parse error")
    echo "  $VPS_STATUS"
else
    echo "  VPS unreachable."
fi
echo ""

# --- 4. Warnings ---
echo "## Warnings"
WARN_COUNT=0

# MEMORY.md line count
MEM_FILE="$HOME/.claude/projects/*/memory/MEMORY.md"
for mf in $MEM_FILE; do
    if [ -f "$mf" ]; then
        MEMORY_LINES=$(wc -l < "$mf" 2>/dev/null | tr -d ' ')
        if [ "$MEMORY_LINES" -gt 200 ] 2>/dev/null; then
            echo "  MEMORY.md: $MEMORY_LINES lines (limit 200)"
            WARN_COUNT=$((WARN_COUNT + 1))
        fi
        break
    fi
done

[ "$WARN_COUNT" -eq 0 ] && echo "  None."
echo ""

# --- 5. Finalize state file ---
cat >> "$STATE_FILE" << STATEFOOT

## VPS
- Status: $VPS_STATUS

## Messaging
STATEFOOT

if [ -n "$MSG_DATA" ]; then
    MSG_COUNT=$(node -e "try{console.log(($MSG_DATA).total||0)}catch(e){console.log('?')}" 2>/dev/null)
    echo "- Unread: $MSG_COUNT" >> "$STATE_FILE"
else
    echo "- Unreachable" >> "$STATE_FILE"
fi

echo ""
echo "=== END SYSTEM AWARENESS ==="
exit 0
