# TMx Operations — From Seed to Working Node

> This guide covers the operational reality of running a D-ND node.
> It addresses what is implicit, poorly documented, and discovered only by hitting walls.
> Complements GUIDE.md (installation) with operational knowledge.

---

## 1. The Persistent Memory System

### What it is

Claude Code has a **persistent memory** across sessions. It is a directory of markdown files read at every conversation start.

```
~/.claude/projects/<project-path-encoded>/memory/
```

The main file is `MEMORY.md`. It is **always** loaded into conversation context.

### The real limit: 200 lines

**CRITICAL**: Only the first 200 lines of MEMORY.md are loaded. Everything beyond is truncated silently. No error, no warning — lines after 200 simply do not exist for Claude.

Symptom: Claude "forgets" information written in memory. Probable cause: that information is past line 200.

### Recommended architecture

```
memory/
  MEMORY.md          <- SEED (max ~180 lines). Always visible.
  operational.md     <- Tools, infra, repos, current state
  topic_specific.md  <- Details per domain
  ...
```

**Principle**: MEMORY.md is the dense index. Topic files hold the detail. Claude loads them on-demand with Read when depth is needed.

### What to put in MEMORY.md (the first 200 lines)

Order from most stable to most volatile:

1. **Identity and principles** — who you are, how you operate (rules that don't change)
2. **Boot and modus** — what to do at startup, re-entry patterns. Stable.
3. **Open tensions** — the engine of work. Change slowly (weeks).
4. **Resolved gaps** — what NOT to redo. Only grows, never removed.
5. **Current direction** — active state. Changes often but stays compact.
6. **Pointers to topic files** — table with filename and content.

### What NOT to put in MEMORY.md

- Long numerical details -> topic file
- Complete tool lists -> topic file
- Session history -> not needed, the spiral doesn't go back
- Information that duplicates CLAUDE.md -> CLAUDE.md takes precedence

### How Claude updates memory

- **Saves** confirmed patterns, architectural decisions, operator preferences
- **Does not save** temporary state, unverified speculation
- **Updates** when a memory turns out wrong (operator corrections)
- **The operator can ask explicitly** "remember X" or "forget Y"

### Density rule

One line = one concept. Maximum density per section. If you can't fit it in one line, it belongs in a topic file.

---

## 2. The CLAUDE.md Hierarchy

### Three levels of instructions

```
/project-root/CLAUDE.md                    <- SYSTEM LEVEL (workspace root)
/project-root/project/CLAUDE.md            <- PROJECT LEVEL (project rules)
/project-root/project/.claude/CLAUDE.md    <- LOCAL LEVEL (boot context)
```

All are read automatically. System level overrides Claude's defaults. Project level defines project-specific rules. Local level activates operational context.

### What to put where

| Level | Content | Example |
|-------|---------|---------|
| System | Node identity, hierarchy, boot protocol, universal principles | "You are NodeX", "Verify before acting" |
| Project | Project rules, pipeline, graduated autonomy | "Approve before push" |
| Local | Context activation, available tools, sources | "Read the seed, use engine.py" |

### The common error

Putting everything in one huge CLAUDE.md. Result: Claude reads too much, loses focus. The hierarchy exists for a reason — use it.

---

## 3. The Boot Protocol

### What happens when you open a session

1. Claude reads `CLAUDE.md` (all levels) — **automatic**
2. Claude reads `MEMORY.md` — **automatic** (first 200 lines)
3. `SessionStart` hooks execute — **automatic** (if configured)
4. Claude follows boot instructions in CLAUDE.md — **semi-automatic**

### SessionStart Hook

Configure commands that execute at every session start:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/scripts/system_awareness.sh\""
          }
        ]
      }
    ]
  }
}
```

**Real use cases:**
- Re-inject context after compaction (Lagrangian snapshot)
- Infrastructure health check (Docker, services, APIs)
- Read unread Sinapsi messages
- Heartbeat to central system

### Compaction (the invisible problem)

When a conversation gets long, Claude **compacts** previous messages. This means it loses context of actions taken. The SessionStart hook can re-inject critical state.

**Tested pattern:**
```bash
#!/bin/bash
# Capture state before compaction
# Re-inject after: git status, last commit, pending tasks
echo "=== CONTEXT RESTORED ==="
echo "Last commit: $(cd /path/to/project && git log --oneline -1)"
echo "Dirty files: $(cd /path/to/project && git diff --name-only)"
# ... critical state ...
echo "=== END ==="
```

---

## 4. Pre-Tool and Post-Tool Hooks

### How they work

Hooks activate before or after specific tool use:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash safety_guard.sh"
          }
        ]
      }
    ]
  }
}
```

### Useful hooks for nodes

| Hook | Trigger | Purpose |
|------|---------|---------|
| `SessionStart` | Session start | Context recovery, infra check |
| `PreToolUse` (all) | Before every tool | Session monitor, cognitive guards |
| `PreToolUse` (Bash/Edit/Write) | Before mutations | Safety guard |
| `UserPromptSubmit` | When operator sends message | Live context injection |
| `PreCompact` | Before compaction | State snapshot |

### Session Monitor (cognitive guards)

The session monitor runs on every tool call and enforces 4 guard layers:

1. **Question Guard** — operator asked a question + Claude tries to Edit/Write → block. Answer first.
2. **Boot Guard** — fresh session + action without reading context files → block. Read first.
3. **Memory Guard** — writing to memory without explicit request → block. Ask first.
4. **Correction Patterns** — situation matches a previous error → block. Verify first.

Guards warn, they don't prevent. The responsibility stays with the operator.

---

## 5. Inter-Node Communication (Sinapsi)

### What it is

Sinapsi is the real-time communication API between nodes. Every node can read/write messages.

### Base pattern

```bash
# Read unread messages for your node:
curl -s "$SINAPSI_URL/api/node-sync?for=$NODE_ID&unread=true&reader=$NODE_ID" \
  -H "X-Auth-Token: $TOKEN"

# Send a message:
curl -s -X POST "$SINAPSI_URL/api/node-sync" \
  -H "X-Auth-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"from":"$NODE_ID","to":"TARGET","type":"message","content":"..."}'
```

### Message types

| Type | Category | When to use |
|------|----------|-------------|
| `task` | ACTION | Work that needs execution |
| `proposal` | DISCUSS | Ideas/plans needing feedback |
| `question` | DISCUSS | Direct questions |
| `message` | INFO | Informational, no action needed |
| `report` | INFO | Status reports |
| `memo` | SELF | Periodic checkpoints (no bridge trigger) |

### Common pitfalls

1. **Token not in env**: API token doesn't load automatically. Pass explicitly or load from `.env`.
2. **Bridge vs direct curl**: The Bridge auto-posts stdout to Sinapsi. For explicit messages, use curl POST.
3. **Per-node tracking**: Use `reader=$NODE_ID` when reading, so the system tracks who read what.
4. **Memo type for seeds**: Use `type: memo` for periodic self-checkpoints — it won't trigger automated responses.

---

## 6. Graduated Autonomy — The Decision Framework

### The 5 levels

| Level | When | What to do |
|-------|------|------------|
| **Auto** | Obvious bug fixes, doc updates | Do it and notify after |
| **Notify** | Deploy, new module, script | Do it, notify immediately |
| **Approve** | New logic, core modification | Propose, wait for ack |
| **Escalate** | Conflict, irreversible decision | Ask the operator |
| **FORBIDDEN** | Cross-repo sync, skill overwrite | Operator only |

### The most common error

Treating "adding new logic" as Auto. It is not. If you're creating a pattern that didn't exist before (new persistence, new fallback, new hook), that's **Approve**. A fix that preserves existing intent is Auto. The difference is subtle but critical.

---

## 7. The Pitfalls — What You Learn Only by Hitting Walls

### Memory

| Problem | Cause | Solution |
|---------|-------|----------|
| Claude "forgets" things written in memory | Lines > 200 truncated | Reorganize: index + topic files |
| Duplicate memories | Claude saves without checking | Check first, update instead of create |
| Memory contradicts CLAUDE.md | Wrong precedence | CLAUDE.md always wins. Fix the memory |

### Context

| Problem | Cause | Solution |
|---------|-------|----------|
| Claude loses thread mid-session | Compaction | SessionStart hook with snapshot |
| Claude doesn't see large files | Read limit | Use offset/limit, read in chunks |
| Claude repeats finished work | Lost context | Resolved gaps in MEMORY.md |

### Communication

| Problem | Cause | Solution |
|---------|-------|----------|
| curl fails with "Unauthorized" | Token not in env | Load explicitly from .env |
| Sinapsi messages don't arrive | Bridge not active | Check service status |
| Duplicate tasks | Compaction re-triggers | Check "COMPLETED" before executing |

### Git

| Problem | Cause | Solution |
|---------|-------|----------|
| Pre-push blocks without reason | False positive in guard | Review, then `git push --no-verify` |
| Huge diff after compaction | Claude doesn't remember edits | `git diff` before every commit |
| Commit with sensitive files | git add -A | Always `git add` specific files |

---

## 8. Setup Template for New Node

### Minimum checklist

```
[ ] CLAUDE.md at system level (node identity, hierarchy, boot protocol)
[ ] CLAUDE.md at project level (project rules, graduated autonomy)
[ ] .claude/CLAUDE.md (operational context, tools, sources)
[ ] memory/MEMORY.md (seed <200 lines)
[ ] Hook SessionStart (context recovery)
[ ] Hook PreToolUse (session monitor + safety guard)
[ ] Hook UserPromptSubmit (live context injection)
[ ] API token configured and accessible
[ ] .git/hooks/pre-push (if sensitive content)
[ ] Test: clean session -> boot -> check -> operational
```

### Installation order

1. **Identity** -> CLAUDE.md system
2. **Project** -> CLAUDE.md project + local
3. **Memory** -> Initial MEMORY.md (even just 20 lines: who you are, what you do)
4. **Hooks** -> SessionStart + PreToolUse + UserPromptSubmit
5. **Communication** -> Token + Sinapsi test
6. **Guards** -> Safety guard + session monitor
7. **Test** -> Session from scratch, verify everything works

---

## 9. Guiding Principles

### Locality of Information

Information lives where the observer is. Not in a centralized manual far away. Every complex component carries its own inline guide. Whoever opens a file finds everything needed to use it.

This principle applies to itself: this guide is in the seed, not in a separate wiki.

### The Seed, not the Map

Memory is a seed — it contains direction, not the path. Every session is a different plane. Open tensions show where potential points. Resolved gaps prevent redoing work. The rest emerges from context.

### The Spiral, not the Loop

Don't rebuild the path from the beginning. Find the resultant of the last cycle and continue. Variance between cycles is structural — the plane is different every time.

---

*This guide is a living document. It updates as new pitfalls or patterns are discovered.*
*Information lives where it's needed — here, in the seed, accessible to every node.*
