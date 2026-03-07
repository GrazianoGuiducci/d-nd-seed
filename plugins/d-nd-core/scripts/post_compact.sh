#!/bin/bash
# ============================================================================
# POST-COMPACT — D-ND Plugin (Parametric)
# ============================================================================
# Re-injects Lagrangian context after compaction.
# Works on any TMx node. Recovers session checkpoints from Sinapsi if configured.
# Env vars: DND_PROJECT_DIR, DND_NODE_ID, DND_SINAPSI_URL, DND_SINAPSI_TOKEN
# ============================================================================

PROJECT_DIR="${DND_PROJECT_DIR:-$(pwd)}"
CONTEXT_FILE="$PROJECT_DIR/.claude/hooks/active_context.md"
REASONING_FILE="$PROJECT_DIR/.claude/hooks/active_reasoning.md"
NODE_ID="${DND_NODE_ID:-unknown}"
SINAPSI_URL="${DND_SINAPSI_URL:-}"
SINAPSI_TOKEN="${DND_SINAPSI_TOKEN:-}"

if [ -f "$CONTEXT_FILE" ]; then
    echo "=== LAGRANGIAN CONTEXT RESTORED (${NODE_ID}) ==="
    echo ""
    while IFS= read -r line; do
        echo "$line"
    done < "$CONTEXT_FILE"
    echo ""
    echo "=== END LAGRANGIAN CONTEXT ==="
    echo ""

    # --- Session Checkpoints from Sinapsi (memo type) ---
    if [ -n "$SINAPSI_URL" ] && [ -n "$SINAPSI_TOKEN" ]; then
        MEMO_DATA=$(curl -s --max-time 3 "$SINAPSI_URL?for=$NODE_ID&reader=$NODE_ID" -H "X-THIA-Token: $SINAPSI_TOKEN" 2>/dev/null)
        if [ -n "$MEMO_DATA" ]; then
            MEMO_SUMMARY=$(echo "$MEMO_DATA" | node -e "
let raw='';
process.stdin.on('data',c=>raw+=c);
process.stdin.on('end',()=>{
const d=JSON.parse(raw);
const memos=(d.messages||[]).filter(m=>m.type==='memo').slice(-3);
if(memos.length===0){process.exit(0)}
console.log('=== SESSION CHECKPOINTS (last '+memos.length+' memos) ===');
console.log('');
memos.forEach(m=>{console.log('> '+m.content);console.log('')});
console.log('=== END CHECKPOINTS ===');
});
" 2>/dev/null)
            if [ -n "$MEMO_SUMMARY" ]; then
                echo "$MEMO_SUMMARY"
                echo ""
            fi
        fi

        # --- Live Sinapsi check (unread messages) ---
        LIVE_SINAPSI=$(curl -s --max-time 3 "$SINAPSI_URL?for=$NODE_ID&unread=true&reader=$NODE_ID" -H "X-THIA-Token: $SINAPSI_TOKEN" 2>/dev/null)
        if [ -n "$LIVE_SINAPSI" ]; then
            LIVE_SUMMARY=$(echo "$LIVE_SINAPSI" | node -e "
let raw='';
process.stdin.on('data',c=>raw+=c);
process.stdin.on('end',()=>{
const d=JSON.parse(raw);
const t=d.total||0;
if(t===0){console.log('No pending messages.')}
else{console.log(t+' unread message(s):');
(d.messages||[]).forEach(m=>{
  const st=m.status||'pending';
  console.log('  - ['+st.toUpperCase()+'] '+m.from+': '+(m.content||'').slice(0,120))
})}
});
" 2>/dev/null)
            echo "=== LIVE SINAPSI CHECK ==="
            echo "$LIVE_SUMMARY"
            echo "=== END LIVE SINAPSI ==="
            echo ""
        fi
    fi

    # --- Fallback: local reasoning file ---
    if [ -f "$REASONING_FILE" ]; then
        echo "=== REASONING CHAIN (local fallback) ==="
        echo ""
        while IFS= read -r line; do
            echo "$line"
        done < "$REASONING_FILE"
        echo ""
        echo "=== END REASONING CHAIN ==="
        echo ""
    fi

    echo "IMPORTANT: Context was compacted. The snapshot above was captured BEFORE compaction."
    echo ""
    echo "REGOLA POST-COMPACTION (operatore): PRIMA di qualsiasi azione:"
    echo "  - Dichiara: 'Sono un'istanza post-compaction. Il mio contesto e un riassunto.'"
    echo "  - Elenca: cosa hai capito dal summary (task completati, task pendenti, stato sistema)"
    echo "  - Elenca: cosa stavi per fare e perche"
    echo "  - ASPETTA conferma operatore. NON procedere autonomamente."
    echo "  - L'operatore deve sapere ESATTAMENTE cosa farai prima che tu lo faccia."
else
    echo "=== POST-COMPACTION: No pre-compact snapshot found (${NODE_ID}) ==="
    echo "Read memory/MEMORY.md for context."
fi

exit 0
