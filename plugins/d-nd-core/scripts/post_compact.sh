#!/bin/bash
# ============================================================================
# POST-COMPACT — D-ND Plugin (Parametric)
# ============================================================================
# Re-injects Lagrangian context after compaction.
# Works on any TMx node.
# ============================================================================

PROJECT_DIR="${DND_PROJECT_DIR:-$(pwd)}"
CONTEXT_FILE="$PROJECT_DIR/.claude/hooks/active_context.md"
NODE_ID="${DND_NODE_ID:-unknown}"

if [ -f "$CONTEXT_FILE" ]; then
    echo "=== LAGRANGIAN CONTEXT RESTORED (${NODE_ID}) ==="
    echo ""
    while IFS= read -r line; do
        echo "$line"
    done < "$CONTEXT_FILE"
    echo ""
    echo "=== END LAGRANGIAN CONTEXT ==="
    echo ""
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
