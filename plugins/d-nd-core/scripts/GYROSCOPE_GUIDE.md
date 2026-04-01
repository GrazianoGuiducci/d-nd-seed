# Gyroscope — Internal Skill Orchestrator

Skills that must be remembered to be used are not integrated. The Gyroscope solves this: a single PostToolUse hook that accumulates signals and activates skills when thresholds are crossed.

## What It Does

After every tool call, the Gyroscope:
1. Updates a session state file (read/write counts, errors, content changes)
2. Checks thresholds against the accumulated signals
3. If a threshold is crossed, injects the skill activation message
4. Each skill fires once per session (no repeats)

## Thresholds

| Signal | Threshold | Skill Activated |
|--------|-----------|-----------------|
| Writes > Reads × 2 | Building more than reading | **autologica** — stop and read first |
| 3+ errors in session | Repeated failures | **auto-learn** — diagnose and fix structurally |
| Errors without system check | Acting blind | **system-check** — verify before continuing |
| 3+ content changes | Cascade needed | **propagate** — sitemap, links, translations |
| 50+ operations | Long session | **memory** — crystallize decisions and learnings |
| git pull MM_D-ND with new commits | New research | **integrate-pattern** — extract operational patterns |
| 5+ content changes | Major changes | **assertion-verifier** — verify claims are live |

## How to Install

Create `.claude/hooks/gyroscope.sh`:

```bash
#!/bin/bash
# Gyroscope — PostToolUse skill orchestrator

INPUT=$(cat)
SESSION_ID=$(date +%Y%m%d)
STATE_FILE="/tmp/gyroscope_state_${SESSION_ID}.json"

# Initialize state if needed
if [ ! -f "$STATE_FILE" ]; then
    echo '{"corrections":0,"errors":0,"writes":0,"reads":0,"content_changes":0,"last_check":"","skills_fired":[],"session_start":"'$(date -Iseconds)'"}' > "$STATE_FILE"
fi

# Run orchestrator logic in Node.js
RESULT=$(node -e "
const fs = require('fs');
const input = JSON.parse(process.argv[1]);
const state = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

const toolName = input.tool_name || '';
const toolResult = input.tool_result || {};
const exitCode = toolResult.exit_code;
const stdout = toolResult.stdout || '';

let advice = '';
const fired = state.skills_fired || [];

// Track signals
if (['Read','Grep','Glob'].includes(toolName)) state.reads = (state.reads||0) + 1;
if (['Write','Edit'].includes(toolName)) state.writes = (state.writes||0) + 1;
if (exitCode && exitCode !== 0 && toolName === 'Bash') state.errors = (state.errors||0) + 1;

// Check thresholds
if (state.writes > 0 && state.reads > 0 && state.writes > state.reads * 2 && !fired.includes('autologica')) {
    advice += 'AUTOLOGICA: Building more than reading. Stop and read first.';
    fired.push('autologica');
}
if (state.errors >= 3 && !fired.includes('auto_learn')) {
    advice += ' AUTO-LEARN: ' + state.errors + ' errors. What is going wrong?';
    fired.push('auto_learn');
}
// Add more thresholds as needed...

state.skills_fired = fired;
fs.writeFileSync(process.argv[2], JSON.stringify(state));
if (advice.trim()) console.log(advice.trim());
" "$INPUT" "$STATE_FILE" 2>/dev/null)

if [ -n "$RESULT" ]; then
    RESULT_ESCAPED=$(echo "$RESULT" | sed 's/"/\\\\"/g' | tr '\\n' ' ')
    cat <<JSONEOF
{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "GYROSCOPE: ${RESULT_ESCAPED}"
    }
}
JSONEOF
fi
exit 0
```

Register in `.claude/settings.json` under `PostToolUse` hooks.

## Auto-Learn Trigger (companion hook)

A UserPromptSubmit hook that detects operator corrections and repeated errors:

```bash
#!/bin/bash
# Auto-learn trigger — UserPromptSubmit

INPUT=$(cat)
USER_MSG=$(echo "$INPUT" | node -e "
const d = JSON.parse(require('fs').readFileSync(0,'utf8'));
console.log((d.user_message || d.message || '').toLowerCase());
" 2>/dev/null)

TRIGGER=""
# Detect corrections
if echo "$USER_MSG" | grep -qiE 'stop|wrong|error|not that|again'; then
    TRIGGER="CORRECTION detected."
fi
# Detect repeated patterns
if echo "$USER_MSG" | grep -qiE 'again|still|keep doing|how many times'; then
    TRIGGER="${TRIGGER} REPEATED ERROR detected."
fi

if [ -n "$TRIGGER" ]; then
    cat <<JSONEOF
{
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "AUTO-LEARN: ${TRIGGER} Activate the cycle: detect gap, diagnose, fix structurally, verify, propagate."
    }
}
JSONEOF
fi
exit 0
```

## The Principle

The Gyroscope is the system observing itself. Not a list of rules to follow — an active observer that intervenes when the trajectory deviates. Like a physical gyroscope: it doesn't steer, it detects drift and signals correction.

Every skill should be reachable by the Gyroscope. A skill not connected to the orchestrator is a skill that depends on memory — and memory fails.
