#!/bin/bash
# ============================================================================
# CLOSURE REMINDER — third-act soft trigger
# ============================================================================
# Fires on UserPromptSubmit. Scans for closure signals across active repos,
# memory crystals, and Sinapsi. Soft prompt to operator — never executes
# anything automatically. Silent when below threshold.
# ============================================================================

SINCE_HUMAN="${CLOSURE_WINDOW:-2 hours ago}"
SINCE_ISO=$(date -d "$SINCE_HUMAN" --iso-8601=seconds 2>/dev/null || date -v-2H -u +%FT%TZ 2>/dev/null)
STATE_FILE="/tmp/.third_act_last_check"
THRESHOLD="${CLOSURE_THRESHOLD:-2}"

# Skip if ran recently (avoid redundant prompts per message batch)
if [ -f "$STATE_FILE" ]; then
    LAST=$(stat -c %Y "$STATE_FILE" 2>/dev/null || stat -f %m "$STATE_FILE" 2>/dev/null)
    NOW=$(date +%s)
    [ $((NOW - LAST)) -lt 300 ] && exit 0  # 5-min cooldown
fi

SIGNALS=0
OUTPUT=""

# --- Scan repos for closure-pattern commits ---
for repo in /opt/THIA /opt/MM_D-ND /opt/d-nd_com /opt/d-nd-seed /opt/Godel_DND /opt/tm7; do
    [ -d "$repo/.git" ] || continue
    COUNT=$(cd "$repo" && git log --since="$SINCE_ISO" --format="%h|%s" 2>/dev/null \
        | grep -cE "closes:|ships:|feat\(skills?\)|feat\(kernel\)|feat\(seed\)" 2>/dev/null)
    if [ "${COUNT:-0}" -gt 0 ]; then
        OUTPUT="${OUTPUT}  - $(basename $repo): $COUNT closure commit(s)\n"
        SIGNALS=$((SIGNALS + COUNT))
    fi
done

# --- Scan memory for new crystals ---
MEM_DIR="/root/.claude/projects/-opt/memory"
if [ -d "$MEM_DIR" ] && [ -f "$STATE_FILE" ]; then
    NEW=$(find "$MEM_DIR" \( -name "feedback_*.md" -o -name "arc_*.md" \) -newer "$STATE_FILE" 2>/dev/null | wc -l)
    if [ "${NEW:-0}" -gt 0 ]; then
        OUTPUT="${OUTPUT}  - memory: $NEW new crystal(s)\n"
        SIGNALS=$((SIGNALS + NEW))
    fi
fi

# --- Scan Sinapsi for EOD-pattern messages ---
TOKEN="${THIA_API_TOKEN:-thia-secure-token-2026}"
EOD=$(curl -s -m 3 "http://localhost:3002/api/node-sync?since=$SINCE_ISO" \
    -H "X-THIA-Token: $TOKEN" 2>/dev/null \
    | grep -oE '"content":"[^"]{0,300}' | grep -cE "EOD|CHIUSO|chiudiamo|finiamo|closure|end.of.day" 2>/dev/null)
if [ "${EOD:-0}" -gt 0 ]; then
    OUTPUT="${OUTPUT}  - sinapsi: $EOD EOD-pattern message(s)\n"
    SIGNALS=$((SIGNALS + EOD))
fi

# --- Emit reminder only if threshold reached ---
if [ "$SIGNALS" -ge "$THRESHOLD" ]; then
    echo "[THIRD-ACT MEMO] Closure signals detected (last $SINCE_HUMAN, total $SIGNALS):"
    printf "$OUTPUT"
    echo "  → Consider running /third-act for reflection + 4-artifact output."
fi

touch "$STATE_FILE"
exit 0
