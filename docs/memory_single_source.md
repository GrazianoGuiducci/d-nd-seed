# Memory — Single Source of Truth

> Durable memory has one canonical source. Active attention loads only the
> bounded present needed to act; recoverable history stays cold on demand.

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

For every memory class:

- Pick **one canonical path**. Write the path in the CLAUDE.md or in the hook that reads it.
- If another location contains a legacy version, first classify it as current
  source, cold evidence, generated output, duplicate or deletion candidate.
  Preserve a canonical pointer or explicit cold boundary before any move or
  deletion; destructive cleanup remains a separate owner-gated effect.
- Update every hook, skill, and doc that references the file so they all point at the same canonical path.
- When in doubt, search the repo for the filename. Every live reference must
  either resolve to the canonical source or declare why it consumes a cold or
  generated artifact.

## Active Attention And Cold Memory

The existence of a durable artifact does not make it part of every reentry:

```text
active_attention:
  accepted present; selected owner; smallest decision-relevant movement set;
  decisive evidence; open unknowns; exact boundary. One action is a compact
  default when the field supports it, not a ceiling.

cold_memory:
  closed receipts; historical chronology; reproducible outputs; supporting
  evidence recoverable for named proof, conflict, recovery or operator request.
```

Where a long state file uses the exact heading
`## Historical chronology — cold, on demand`, normal reentry stops before that
heading. This is a reading boundary, not a deletion marker.

Before creating or updating durable memory, apply one admission test:

```text
Will this change future behavior, proof, recovery or reentry?
```

If not, leave it non-durable. This prevents new files and repeated summaries
from becoming an accumulating tax on the cognitive working set.

## What the canonical path should be

The canonical path depends on scope:

| Scope | Canonical location |
|-------|---------------------|
| Project-specific neutral memory | `.seed/memory/<name>.md` inside the installed project |
| Claude Code adapter memory | `.claude/MEMORY.md` or `.claude/hooks/<name>.md` inside the project |
| Agent-specific memory across projects | User-level: `~/.claude/projects/<slug>/memory/<name>.md` |
| Team-wide memory | A git-tracked file in the shared repo, explicitly marked as authoritative |

Pick the **narrowest scope** that covers all legitimate readers. Memory that only one agent needs should not live in a shared repo. Memory that multiple projects need should not live inside one project. A coherent portable invariant, however, should participate across every relevant relation now; narrow placement governs its owner-native material incarnation, not its cognitive reach.

## Agent-Neutral Placement

Claude Code is one runtime, not the whole Seed. For external systems and
app-hosted coders, first classify the memory by consuming level:

| Placement | Consumer | Examples |
|---|---|---|
| `project_local` | one project or surface | project current state, QA checklist, local handoff |
| `workspace_root` | multiple projects in one workspace | entry gate, surface-selection rule, shared token policy |
| `coder_adapter` | one runtime/app/postazione | `.claude`, `.codex`, app-local config, runtime-specific memory |
| `shared_coordination` | multiple nodes/postazioni | packets, validation notices, delivery receipts |
| `portable_capability` | future systems | normalized invariant in Seed after proof |

The canonical path should be the lowest level that all legitimate consumers can
read. Do not store project state in Seed only because it is important. Do not
store portable capability truth only in a runtime-specific adapter. Do not force
non-Claude runtimes to miss Seed logic because the compatibility surface happens
to be named `.claude`.

## Why this rule matters after compaction

After context compaction, the post-compact hook re-injects memory into the agent's context. If two files exist, the hook picks one — often arbitrarily, based on the order of code. The agent reads it and treats it as truth. The other file, containing divergent content, silently rots.

A single source of truth makes the hook's choice deterministic and the agent's behavior reproducible. Without it, every compaction recovery is a coin flip.

## Diagnostic

To check your memory system for duplicates:

```bash
# From the project root
find . ~/.claude -name "MEMORY.md" -o -path "*/.seed/memory/*" -o -name "session_continuum.md" -o -name "active_reasoning.md" 2>/dev/null
```

If any filename appears more than once, classify the relation and reconcile the
live pointers. Archive, move, symlink or delete only through the exact owner and
effect gate; do not turn diagnosis into cleanup authority.
