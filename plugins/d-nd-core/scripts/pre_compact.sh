#!/bin/bash
# ============================================================================
# PRE-COMPACT — D-ND Plugin (Parametric)
# ============================================================================
# Captures Lagrangian state before compaction.
# Works on any TMx node — auto-detects repos.
# ============================================================================

read -t 1 INPUT_LINE 2>/dev/null || INPUT_LINE=""

PROJECT_DIR="${DND_PROJECT_DIR:-$(pwd)}"
CONTEXT_FILE="${PROJECT_DIR}/.claude/hooks/active_context.md"
NOW=$(date '+%Y-%m-%d %H:%M' 2>/dev/null || echo "unknown")
NODE_ID="${DND_NODE_ID:-unknown}"

# --- Gather git state ---
repo_state() {
    local REPO_NAME=$1 REPO_PATH=$2
    [ ! -d "$REPO_PATH/.git" ] && return

    local BRANCH=$(git -C "$REPO_PATH" branch --show-current 2>/dev/null || echo "unknown")
    local LAST_COMMIT=$(git -C "$REPO_PATH" log --oneline -1 2>/dev/null || echo "none")
    local DIRTY=$(git -C "$REPO_PATH" diff --name-only 2>/dev/null)
    local STAGED=$(git -C "$REPO_PATH" diff --cached --name-only 2>/dev/null)

    echo "### $REPO_NAME ($BRANCH)" >> "$CONTEXT_FILE"
    echo "- Last commit: \`$LAST_COMMIT\`" >> "$CONTEXT_FILE"

    if [ -n "$DIRTY" ]; then
        echo "- **Uncommitted changes:**" >> "$CONTEXT_FILE"
        echo "$DIRTY" | head -10 | while IFS= read -r f; do echo "  - \`$f\`" >> "$CONTEXT_FILE"; done
    fi
    if [ -n "$STAGED" ]; then
        echo "- **Staged:**" >> "$CONTEXT_FILE"
        echo "$STAGED" | head -10 | while IFS= read -r f; do echo "  - \`$f\`" >> "$CONTEXT_FILE"; done
    fi
    echo "" >> "$CONTEXT_FILE"
}

# --- Detect mode ---
HAS_DIRTY=""
for dir in "$PROJECT_DIR"/*/; do
    if [ -d "$dir/.git" ]; then
        D=$(git -C "$dir" diff --name-only 2>/dev/null)
        [ -n "$D" ] && HAS_DIRTY="yes"
    fi
done
MODE="${HAS_DIRTY:+FILE_EDIT}"
MODE="${MODE:-GENERAL}"

# --- Write context ---
mkdir -p "$(dirname "$CONTEXT_FILE")" 2>/dev/null
cat > "$CONTEXT_FILE" << EOF
# Active Context — Lagrangian Snapshot
> Pre-compact capture at $NOW | Node: $NODE_ID | Mode: $MODE
> Re-injected after compaction to restore critical state.

## Repository State
EOF

for dir in "$PROJECT_DIR"/*/; do
    [ -d "$dir/.git" ] && repo_state "$(basename "$dir")" "$dir"
done

cat >> "$CONTEXT_FILE" << 'EOF'

## Recovery Instructions
- Read `memory/MEMORY.md` for persistent project context
- Check the todo list for in-progress tasks
- If files have uncommitted changes, run `git diff` before proceeding

## Post-Compaction Rule
PRIMA di qualsiasi azione:
- Dichiara: "Sono un'istanza post-compaction. Il mio contesto e un riassunto."
- Elenca: cosa hai capito dal summary (task completati, task pendenti, stato sistema)
- Elenca: cosa stavi per fare e perche
- ASPETTA conferma operatore. NON procedere autonomamente.
EOF

echo "[PRE_COMPACT] Context saved (node=$NODE_ID, mode=$MODE)" >&2
