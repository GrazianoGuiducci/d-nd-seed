# Morning Intel — Proactive Environment Awareness

Every node needs fresh information about its domain. Not a dump of news — a curated digest of what matters for what this node does.

## What It Does

A SessionStart hook that runs once per day. Gathers intelligence from available sources and presents it at boot so the session starts with awareness of the environment.

## Sources (adapt per node)

1. **Knowledge base** — recent high-value entries (last 3 days, score >= threshold)
2. **Pending items** — unprocessed videos, unread messages, stale files
3. **Suggested searches** — topics relevant to this node's role, to run in-session with web search

## How to Install

Create `.claude/hooks/morning_intel.sh`:

```bash
#!/bin/bash
# Morning Intel — runs once per day at SessionStart

TODAY=$(date +%Y%m%d)
FLAG="/tmp/morning_intel_${TODAY}.done"
if [ -f "$FLAG" ]; then exit 0; fi
touch "$FLAG"

INTEL=""

# --- Add your sources here ---
# Each source appends to INTEL

# Knowledge base (if available)
# KB_DIGEST=$(node -e "..." 2>/dev/null)
# if [ -n "$KB_DIGEST" ]; then INTEL="${INTEL}${KB_DIGEST}\n\n"; fi

# Pending items
# PENDING=$(python3 -c "..." 2>/dev/null)
# if [ -n "$PENDING" ]; then INTEL="${INTEL}${PENDING}\n\n"; fi

# Suggested searches (customize per node role)
INTEL="${INTEL}SUGGESTED SEARCHES:\n"
INTEL="${INTEL}  - [your domain] news/updates\n"
INTEL="${INTEL}  - security advisories for [your stack]\n"
INTEL="${INTEL}  - [your project] mentions\n"

if [ -n "$INTEL" ]; then
    cat <<JSONEOF
{
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "MORNING INTEL:\n${INTEL}"
    }
}
JSONEOF
fi
exit 0
```

Register in `.claude/settings.json` under `SessionStart` hooks.

## Customization Per Node

| Node Role | Sources | Search Topics |
|-----------|---------|---------------|
| **Dev/Site** | KB entries, pending items, site health | Claude Code updates, AI frameworks, npm security |
| **Infrastructure** | System health, research results, git activity | Server security, Docker updates, model releases |
| **Research** | Journal entries, new tensions, paper status | Related papers, domain discoveries |
| **Client projects** | Client domain news, competitor activity | Industry news, regulation changes |

## The Principle

A node that starts its day without knowing what happened overnight operates on yesterday's assumptions. The cost of 10 seconds of context gathering is always lower than the cost of acting on stale information.

The intel is not a briefing — it is the minimum awareness to ask the right first question.
