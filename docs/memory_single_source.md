# Memory — Single Source of Truth

> Memory about the session, the project, or the agent lives in **one file in one place**. No duplicates.

## The principle

Persistent memory works only when the agent knows **exactly** where to read and where to write. If the same kind of memory exists in two locations, every write is a choice with hidden cost:

- Write to both → eventual drift (one lags behind the other)
- Write to one → the other becomes stale and misleads future sessions
- Write to neither → the operator corrects the same things twice

**Duplication is not redundancy. It is future confusion.**

## When duplication appears

The most common sources:

1. **Hook-generated files** end up next to hand-curated files with the same name. The mechanical one gets written by a script; the semantic one gets written by the agent. Both survive, both get stale, nobody knows which is authoritative.
2. **Template defaults** stay in the installed location after the agent starts curating a real file elsewhere. The template skeleton from install time is never deleted.
3. **Archival habits** leave old versions in place "just in case". The agent reads all of them and averages noise.

## The rule

For every memory file:

- Pick **one canonical path**. Write the path in the CLAUDE.md or in the hook that reads it.
- If another location contains a legacy version, archive the legacy content to a dated file (`<name>_archived_YYYY-MM-DD.md`) and replace the original path with a symlink to the canonical, **or** delete it entirely if nothing references it.
- Update every hook, skill, and doc that references the file so they all point at the same canonical path.
- When in doubt, grep the repo for the filename. Every reference must either be the canonical one or a symlink pointing there.

## What the canonical path should be

The canonical path depends on scope:

| Scope | Canonical location |
|-------|---------------------|
| Project-specific memory | `.claude/MEMORY.md` or `.claude/hooks/<name>.md` inside the project |
| Agent-specific memory across projects | User-level: `~/.claude/projects/<slug>/memory/<name>.md` |
| Team-wide memory | A git-tracked file in the shared repo, explicitly marked as authoritative |

Pick the **narrowest scope** that covers all legitimate readers. Memory that only one agent needs should not live in a shared repo. Memory that multiple projects need should not live inside one project.

## Why this rule matters after compaction

After context compaction, the post-compact hook re-injects memory into the agent's context. If two files exist, the hook picks one — often arbitrarily, based on the order of code. The agent reads it and treats it as truth. The other file, containing divergent content, silently rots.

A single source of truth makes the hook's choice deterministic and the agent's behavior reproducible. Without it, every compaction recovery is a coin flip.

## Diagnostic

To check your memory system for duplicates:

```bash
# From the project root
find . ~/.claude -name "MEMORY.md" -o -name "session_continuum.md" -o -name "active_reasoning.md" 2>/dev/null
```

If any filename appears more than once, reconcile: one canonical, others archived or symlinked.
