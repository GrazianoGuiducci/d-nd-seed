---
name: integrate-pattern
description: Integrate research functions from a model layer into operational patterns. The complement of propagator — propagator goes downstream (change to targets), integrate-pattern goes upstream (model function to operational use). Trigger when new model commits are detected or when the operator says "integra", "converti", "porta qui".
---

# Integrate Pattern — From Research to Operations

When the research layer (model work, formalization projects, or any source of formalized functions)
produces something new, this procedure converts it into an operational pattern
that the node can use in its own work.

## When this triggers

- system_awareness.sh reports new research repo commits not yet integrated
- The operator says "integra", "converti", "porta qui"
- A message from another node contains a new function or formalization

## The procedure

### 1. Read the source function

Go to the source. Read the actual code or document, not a summary.
Understand what the function does at three levels:
- **Meccanica**: what it computes / produces (the local result)
- **Pattern**: what principle it embodies (the transferable structure)
- **Applicazione**: where else this pattern applies (the insight)

### 2. Extract the universal pattern

The function was written for a specific context (research, model validation, etc.).
Strip the context. Keep the pattern. The extraction method:

1. **Name the dipole**: what two forces does this function hold in tension? (e.g., "speed vs accuracy", "known vs unknown")
2. **Find the invariant**: what is true regardless of the specific domain? (e.g., "tracking the boundary between known and unknown improves decisions")
3. **Test transferability**: apply the pattern mentally to a completely different domain. Does it still make sense? If not, it's not universal — it's domain-specific.

Example:
- Source: a function that tracks knowledge state [known, unknown] and applies iterative refinement
- Dipole: knowing vs not-knowing
- Invariant: after every significant action, check if your known/unknown boundary shifted
- Transfer test: applies to code review (what do I know about this codebase?), to debugging (what have I ruled out?), to planning (what assumptions haven't been tested?)
- Pattern: **boundary tracking** — after significant actions, re-evaluate the boundary between confirmed and unconfirmed

### 3. Convert to operational format

Create an entry in `operational_patterns.json`:

```json
{
  "id": "descriptive_name",
  "trigger": "regex matching when this pattern should activate",
  "context": "INSTRUCTION: what the node should do when triggered. Written in second person — 'your', 'you'. This is YOUR tool, not a window on the source.",
  "scope": "bash|edit|all",
  "_origin": "source reference (repo, file, function)",
  "_genesis": "ISO date of integration"
}
```

Rules for the context string:
- Write it as if talking to the node that will use it
- Use "TUO", "TU", "YOUR" — the pattern belongs to the node now
- Do NOT reference the source system as authority — the pattern is self-standing
- Keep it under 500 characters
- Include the 3 key elements: what to do, when, why

### 4. Create or update tracking state

If the pattern tracks evolving state (like knowledge boundaries), create a file:

```
memory/[pattern_name].md
```

Format:
```markdown
# [Pattern Name] — State

> Origin: [source]. Converted for [this node].
> Updated after significant shifts. Not after every action.

## [area]
- **noto**: what has been confirmed
- **ignoto**: what remains open at the boundary
- **ultimo salto**: when and what changed the ratio (+ pattern type)
```

### 5. Mark integration

After installing the pattern:

```bash
echo COMMIT_HASH > .claude/hooks/[source]_last_integrated.txt
```

This lets system_awareness.sh know when new source commits arrive that haven't been integrated.

### 6. Verify

- Trigger the pattern manually (run a command that matches the trigger regex)
- Confirm the context injects correctly
- If state tracking: verify the file exists and is readable

## The three pattern types

When extracting, classify the pattern. This helps the node recognize it in future work:

| Type | Signal | Action |
|------|--------|--------|
| **Universality > specificity** | What seemed unique is shared by a class | Stop looking for differences. Find the common structure. |
| **Hidden structure** | The phenomenon has a level that wasn't visible | Go one level down. What generates this behavior? |
| **Partial convergence** | Direction is right, final form not yet | Don't change direction. Refine the form. |

## The autopoietic principle

This procedure is not just a tool — it is the product.

Every time a node integrates a pattern using this procedure, the procedure itself
is validated and refined. The integration process IS the seed instruction.

What the node learns during integration becomes procedural knowledge for:
1. The node itself (operational_patterns.json)
2. The seed (this SKILL.md — updated if the procedure evolves)
3. Other nodes (they receive the seed and know how to configure themselves)

The cycle: research produces functions → node integrates → procedure refines → seed updates → other nodes receive.

## Cascade after integration

A new integrated pattern changes the field. Ask:
- **Internal**: does this pattern affect existing patterns in `operational_patterns.json`? (conflicts, overlaps, reinforcements)
- **External**: should other nodes or projects know about this pattern? If it's truly universal, it belongs in the seed — not just in your local config.
- **Emergent**: does this pattern, combined with existing ones, reveal something new? Two patterns that separately are useful might together point to a principle.

Integrate first, then cascade. Not the reverse — you need to understand the pattern before you can propagate it correctly.

## What NOT to do

- Do NOT copy the source function verbatim — extract the pattern
- Do NOT leave the pattern pointing at the source ("another node's tool") — it's yours now
- Do NOT integrate everything — only patterns that are transferable and useful
- Do NOT skip the marking step — without it, the system loses track of what's integrated

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
