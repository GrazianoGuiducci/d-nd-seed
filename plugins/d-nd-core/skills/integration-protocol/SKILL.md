---
name: integration-protocol
description: "Protocol for connecting pre-existing elements (skills, hooks, memory, rules) into a coherent system without duplication. Activate when input matches 'connect X', 'integrate Y', 'unify W', 'orchestrate', 'wire together', or when you feel the system has too many disconnected pieces needing an orchestrator."
user-invocable: true
---

# Integration Protocol — 7 steps to wire the pre-existing

> The default failure mode when asked to integrate is to build a new layer on top.
> This protocol prevents that: observe first, recognize the invariant already present, name it, map, build minimum.

## When this applies

Trigger prompts:
- "connect X"
- "integrate Y into Z"
- "unify the various W"
- "orchestrate"
- Intuition: "too many disconnected pieces, need a coordinator"

Does NOT apply to:
- Single implementation tasks (just do it)
- Local refactor (no cross-system connection)
- Quick fix (the protocol is overhead)

---

## The 7 phases

### 1. OBSERVE the existing landscape
Before building anything, read:
- All relevant directories (recursive `ls` on skills/, hooks/, memory/, kernels/)
- All index files (CLAUDE.md, README, MEMORY.md, hooks.json, settings)
- The header/description of every candidate skill/hook/agent

Test: if after observation I cannot name ~20 specific elements of the domain, I have not observed enough. Construction will presuppose.

### 2. RECOGNIZE the shared invariant pattern
During reading, look for the structure that recurs. Test: if two or more elements have similar structure (N steps, N modes, N gates), they are probably specializations of the same neutral pattern.

Example: 6 steps in cec + 6 modes in autologica + 4 gates in a method = there is a shared invariant.

### 3. NAME the neutral form as first-class
Do not add a "new skill" on top of the existing. Name the neutral form that was already implicit. The new artifact is the recognition, not the addition.

Test of vocabulary: has the operator already named the form? Often the name is there, the crystallization is missing.

### 4. MAP each existing element as a specialization
Build the "context → specialization" table. Every existing skill/hook/rule goes in a row. If an element does not find a row, either it is outside the pattern (do not force integration) or the pattern is still incomplete (iterate).

The value of the new artifact is the mapping table, not original content.

### 5. BUILD the minimum necessary
Output should be:
- A file containing the neutral form + mapping table + anti-patterns
- A pointer in memory (MEMORY.md Level 1) that reminds the skill exists
- Zero duplication: every concrete rule stays in the original skill

Count new lines: if 20%+ duplicates existing content, there is redundancy → P7 (remove).

### 6. APPLY the neutral form to itself (autologica f(f))
Did what I built pass through its own filter?
- CONDITIONS: did I observe before building?
- SIGNATURE: does the structure survive a change of implementation?
- EXPANSION: does it work in multiple domains?
- INVERSION: is it inversion (naming the existing) or addition (building on top)?
- CRYSTALLIZATION: is it minimal?

If it passes its own filter, it is coherent. If not, reformulate.

### 7. CASCADE at 3 levels
- **Internal**: all modified/created files refer correctly to each other (pointer, description, index)
- **External**: MEMORY.md L1 updated, relevant CLAUDE.md if necessary, what goes into the seed as generalizable form, what goes to peer nodes via cowork
- **Emergent**: during the cascade, what did I discover that deserved to change elsewhere? Annotate and crystallize.

---

## Anti-patterns

- **Building immediately**: skip observation → duplication guaranteed
- **Adding a layer**: build meta on top instead of recognizing neutral → bloat
- **Over-naming**: giving pompous names to the neutral form when the operator already named it — listen
- **Skip autologica**: not applying the filter to what I built → apparent coherence, not real
- **Incomplete cascade**: stop at the main file, leave indexes stale

---

## How this becomes a self-intervening assistant

Wire option 1: this skill itself is pointed to by `sieve-orchestrator` under the "connecting elements" row. When input matches trigger words, sieve-orchestrator routes here.

Wire option 2: a UserPromptSubmit hook with regex on trigger keywords injects a reminder of the 7 phases before the response begins.

Currently (seed v1): discretionary invocation. If the protocol holds across 2-3 applications, hook wiring becomes justified.

---

## Axiom grounding

- **A8 (autologica)**: f(f) — the design follows the model that the design implements
- **A6 (mobile zero)**: do not build from fullness but from recognizing the absence of connection
- **A11 (combo)**: the 7 phases are not sequential, they are simultaneous — I "see them together" before executing
- **P6 (memory as recognition)**: the neutral form already exists, I recognize it, I do not invent it
- **P7 (limit value)**: value is what remains after removing the superfluous

## Eval

## Trigger Tests
# "connect these things" -> activates
# "integrate X into Y" -> activates
# "unify the scattered skills" -> activates
# "add a comment" -> does NOT activate
# "refactor this function" -> does NOT activate (single implementation)

## Fidelity Tests
# Given "connect A, B, C": produces 7-phase walkthrough with table output
# Given incomplete observation: flags "not enough territory observed" before building
# Given autologica skip: produces warning and forces phase 6
