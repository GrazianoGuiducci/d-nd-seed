#!/bin/bash
# ============================================================================
# SAFETY GUARD — D-ND Plugin (Parametric)
# ============================================================================
# PreToolUse hook: checks for dangerous patterns, injects warnings.
# Does NOT block — reminds. "Sei consapevole?"
#
# Works on any TMx node. Uses DND_VPS_IP env var if available.
# ============================================================================

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(d.tool_name||'')" 2>/dev/null)
TOOL_INPUT=$(echo "$INPUT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(JSON.stringify(d.tool_input||{}))" 2>/dev/null)

WARNING=""
VPS_IP="${DND_VPS_IP:-${DND_VPS_IP:-localhost}}"

if [ "$TOOL_NAME" = "Bash" ]; then
    COMMAND=$(echo "$TOOL_INPUT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(d.command||'')" 2>/dev/null)

    # Destructive git operations
    if echo "$COMMAND" | grep -qiE 'git\s+(push\s+--force|reset\s+--hard|clean\s+-f|branch\s+-D)'; then
        WARNING="DESTRUCTIVE GIT: Questo comando puo distruggere lavoro. Sei sicuro? Verifica con l'operatore."
    fi

    # Production container commands
    if echo "$COMMAND" | grep -qiE 'docker\s+(rm|stop|kill)|rm\s+-rf\s+/opt'; then
        WARNING="PRODUCTION DANGER: Questo comando impatta il container/VPS di produzione. Conferma con l'operatore."
    fi

    # Deleting important files
    if echo "$COMMAND" | grep -qiE 'rm\s+-rf|rm\s+.*\.(js|json|md|env)'; then
        WARNING="FILE DELETE: Stai eliminando file. Sei sicuro che non siano necessari? Verifica prima."
    fi

    # SSH to VPS with destructive intent
    if echo "$COMMAND" | grep -qiE "ssh.*${VPS_IP}.*(rm|drop|delete|truncate)"; then
        WARNING="VPS REMOTE DELETE: Comando distruttivo sul server remoto. Conferma con l'operatore."
    fi

    # Docker restart
    if echo "$COMMAND" | grep -qiE 'docker\s+restart'; then
        WARNING="CONTAINER RESTART: Il container si riavviera. THIA sara offline per qualche secondo. Sei consapevole?"
    fi

    # Modifying .env files
    if echo "$COMMAND" | grep -qiE '(sed|echo|cat).*\.env'; then
        WARNING="ENV MODIFICATION: Stai toccando file con segreti. Verifica che il cambiamento sia intenzionale."
    fi
fi

if [ "$TOOL_NAME" = "Edit" ] || [ "$TOOL_NAME" = "Write" ]; then
    FILE_PATH=$(echo "$TOOL_INPUT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); console.log(d.file_path||'')" 2>/dev/null)

    # Critical system files
    if echo "$FILE_PATH" | grep -qiE 'boot_kthia\.js|COMMANDMENTS\.md|SYSTEM_PROMPT|\.env'; then
        WARNING="CRITICAL FILE: Stai modificando un file core del sistema ($FILE_PATH). Serve conferma operatore."
    fi
fi

if [ -n "$WARNING" ]; then
    node -e "
const w = process.argv[1];
console.log(JSON.stringify({
    hookSpecificOutput: {
        hookEventName: 'PreToolUse',
        additionalContext: '⚠️ SAFETY GUARD: ' + w
    }
}));
" "$WARNING"
fi

exit 0
