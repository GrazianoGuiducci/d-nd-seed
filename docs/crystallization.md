# Crystallization Pattern Specification

> Version: 0.1 — First stable pattern, validated post-compaction.
> Origin: anamnesis repo (now archived). Canonical home: d-nd-seed.

## Overview

Crystallization is the process of capturing the **dynamic reasoning state** of an AI coder session in a structured format that survives context loss events (compaction, session restart, topic switch).

The output is a file (`active_reasoning.md`) that carries not just facts, but:
- **Why** the current approach was chosen
- **What** alternatives were explored and rejected (with reasons)
- **Where** the reasoning was heading (trajectory, not just position)
- **What** atomic insights emerged (KLI — Key Learning Insights)
- **What** was deferred or dormant (Vault)

## The Three Axioms

Every implementation of this pattern must respect these three irreducible principles:

### Axiom 1: Relational Invariance (Ω.1)

> Crystallize relationships, not isolated facts.

A fact ("we chose library X") without its relational context ("because Y failed and Z was too complex for our constraints") is noise after compaction. The relationship between the decision, its alternatives, and its constraints is what carries meaning.

### Axiom 2: Metabolic Cycle (Ω.2)

> Output of compaction becomes input of the next session.

The system must form a closed loop: what is written before compaction must be readable and useful after compaction. If the crystallization file is not re-injected, it serves no purpose. The cycle is: **Crystallize → Compact → Re-inject → Resume → Crystallize**.

### Axiom 3: Selective Integrity (Ω.3)

> Maximum coherence per minimum complexity.

Not everything deserves crystallization. The format must select for what carries the most reasoning density in the fewest tokens. A crystallization that is too verbose will itself be truncated or ignored. A crystallization that is too sparse will fail to restore context.

## Crystallization Format: CCCA-lite

The canonical format for `active_reasoning.md`:

```markdown
# Active Reasoning — [Session identifier]
> Session: [date or ID]

## Field

### Intent Core
[1-2 sentences: what is the current goal]

### Causal Chain
[Numbered list: the sequence of reasoning steps that led here]
1. [Starting observation or trigger]
2. [Analysis / discovery]
3. [Decision point]
...
n. [Current state]

### Bifurcations (Explored and Rejected)
[List: alternatives that were considered and WHY they were rejected]
- [Option A] → rejected because [reason]
- [Option B] → rejected because [reason]

### Active Decisions
[List: architectural or strategic decisions currently in effect]
- **[Decision name]**: [what was decided and why]

### KLI (Key Learning Insights)
[List: atomic insights that emerged during the session]
- "[Insight text]" — [brief context]

### Vault (Dormant, Reactivatable)
[List: items that were deferred — not rejected, just not active now]
- [Item] — [why dormant, when to reactivate]

## Metatags
[Comma-separated keywords for searchability]

## Proto-Actions
[Checklist: what was done and what remains]
- [x] [Completed action]
- [ ] [Pending action]

## Constraints
[List: rules or limitations that govern current work]
- [Constraint and why it exists]
```

## Lagrangian Capture Format

The `pre_compact.sh` hook captures the **mechanical state** — what git, filesystem, and tools report. This complements the semantic crystallization.

```markdown
# Active Context — Lagrangian Snapshot
> Pre-compact capture at [timestamp] | Mode: [FILE_EDIT|GENERAL]

## Repository State
### [Repo Name] ([branch])
- Last commit: `[hash] [message]`
- Uncommitted changes: [list]
- Untracked: [list]

## Field State
- **Attractor**: [most recently modified file — gravitational center]
- **Momentum**: [active-flow|warm|cold] ([minutes] since last commit)
- **Trajectory**: [last 3 commits — direction, not just position]

## Recovery Instructions
[Ordered list: what to check after compaction]
```

## Navigation Map Format

The `context_map.md` provides rapid orientation: "for this question, look there."

```markdown
# Navigation Map

### "[Question]?"
→ [file_path] — [what you'll find there]

### "[Question]?"
→ [file_path] — [what you'll find there]

## Post-Recovery Read Order
1. [First file to read] — [why] ([estimated time])
2. [Second file] — [why]
...
```

## Hook Events

The pattern uses two hook events. Adapt to your tool's event system:

| Event | When | What it does |
|-------|------|-------------|
| **PreCompact** | Before token window compaction | Runs `pre_compact.sh`: captures git state + field state → writes `active_context.md` |
| **PostCompact** | After compaction, at session resume | Runs `post_compact.sh`: reads `active_context.md` + `active_reasoning.md` → prints to stdout (injected into AI context) |

### Claude Code Events

- `PreCompact` → fires before compaction
- `SessionStart` with condition `compact` → fires after compaction

### Other Tools

Any tool that supports:
- A "before context reset" event → use for Lagrangian capture
- A "context injected at start" mechanism → use for re-injection

If your tool has no hook system, the pattern can still work manually: tell the AI coder to read `active_reasoning.md` at the start of each session.

## Feedback Loop (Hephaestus)

After each compaction recovery, evaluate:

1. **Did the reasoning chain help?** Could you resume faster than without it?
2. **What was missing?** What did you need that wasn't crystallized?
3. **What was noise?** What was crystallized but useless after recovery?

Document this feedback in the crystallization signal or directly in `active_reasoning.md`. This closes the loop and improves the next crystallization.

## Discipline

The crystallization is not automatic — it requires the AI coder to write to `active_reasoning.md` during the session when it detects significant reasoning chains. Guidelines:

- **When to crystallize**: after a decision with explored alternatives, after a significant insight, after a topic switch, before expected compaction
- **When NOT to**: routine file edits, simple bug fixes, mechanical operations
- **Incremental updates**: don't rewrite the file each time — update the relevant section
- **Keep it dense**: the crystallization competes for tokens with the actual work; make every line count
