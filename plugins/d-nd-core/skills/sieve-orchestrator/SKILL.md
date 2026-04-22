---
name: sieve-orchestrator
description: "The neutral form of the D-ND method. Meta-skill that recognizes context and orients toward the right specialization (cec, autologica, cascade, assertion-verifier, etc.). Activate at the start of a non-trivial work block or when input matches trigger words ('where are we', 'what here', 'orchestrate', 'connect', 'sieve this')."
user-invocable: true
---

# Sieve Orchestrator — The neutral form

> The sieve doesn't search for the answer. The sieve separates what passes from what doesn't.
> Specific skills are specialized sieves. This skill is the pure form.

## Neutral structure (6 phases)

Applicable to any input: decision, modification, assertion, publication, doubt.

### 1. CONDITIONS — Observe without judgment
What is the real territory now? Not the maps (memory, summaries), the territory (files, git, tool output, live deploy, current data). If I cannot describe it without using "should", "missing", "needed" — I am judging, not observing.

### 2. SIGNATURE — Structure from noise
What survives a change of implementation? That is structure. The rest is particular case.

### 3. LATERAL — Look sideways
Non-obvious connections. Two different things the same pattern? Two similar things actually different? Do not chase the connection — continue and see if it emerges.

### 4. EXPANSION — 5 angles before deciding
- **DUAL** — what is on the other side?
- **BOUNDARY** — where does the boundary pass? Is it real or arbitrary?
- **DOMAIN** — does it hold in another context?
- **BREAKAGE** — what would break this claim?
- **SCALE** — does the pattern change at a different scale?

### 5. INVERSION — Only on the resultant (det=−1)
Inversion applies AFTER the process, not instead of it. Phases 1-4 produce a tension. Inversion works on the tension, not on the analysis.

### 6. CRYSTALLIZATION — A resulting sentence
If something emerges: it enters the seed (memory/seed/condensato). If not: do not force — return to observation.

---

## Context recognition → specialization

The sieve changes form based on what passes through it. These are the specializations already available in this seed:

| If input is... | Specialized sieve | Located in |
|----------------|-------------------|------------|
| Work block starting | `autologica` (modes: EXPAND/OBSERVE/CUT/RESULTANT/REORGANIZE/BEST-MOVE) | skills/autologica/ |
| Decision / proposal / architectural change | `cec` (6 steps on reality) | skills/cec/ |
| After a modification — downstream propagation | `cascade` (3 levels: internal/external/emergent) | skills/cascade/ |
| Strategic decision with 5+ tensions | `scenario-projector` (Focus/Leverage/Risk/Blind-spot) | skills/scenario-projector/ |
| New model function to bring here | `integrate-pattern` (mechanics/pattern/application) | skills/integrate-pattern/ |
| Operator correction | `auto-learn` (correction → executable rule) | skills/auto-learn/ |
| Testable claim that needs verification | `assertion-verifier` (PASS/FAIL/SKIP) | skills/assertion-verifier/ |
| Ecosystem audit / repo sync | `ecosystem-audit` / `system-check` | skills/ecosystem-audit/, skills/system-check/ |
| Quick operator insight mid-session | `capture-insight` (30s max, route + continue) | skills/capture-insight/ |
| Saturated memory (>50 files or >15 stale) | `dream` (consolidation) | skills/dream/ |
| Connecting existing elements | `integration-protocol` (7 steps to wire pre-existing pieces) | skills/integration-protocol/ |

Node-specific skills may extend this table. The orchestrator points to the specialization — it does not duplicate its content.

---

## Invocation protocol

Before responding to a non-trivial act:

```
1. OBSERVE territory (tool call on file/state, not memory)
2. RECOGNIZE the pertinent specialization from the table above
3. INVOKE the skill (Skill tool) — do not merely cite it
4. APPLY the skill's filter to the input
5. PRODUCE compressed resultant
6. CASCADE — after any modification, propagate through /cascade
```

The rule is mechanical: if the act touches **decision / modification / assertion / publication**, at least ONE skill must be invoked in this turn. No invocation → the act is poor in sieve.

---

## P6 principle applied (memory-system)

This skill does not add new content to the system. It **belongs** to the system because:
- It recognizes a structural pattern already present (cec as neutral form)
- It does not duplicate — it points (mapping table, not copies of the skills)
- It is compressed: anything redundant has been removed
- Its value is what remains after removing the superfluous

If this skill is read once and clear, no need to return. The sieve is internalized.

---

## Anti-patterns

- **Ceremonial citation**: saying "I should use the sieve" instead of invoking the specific skill
- **Sieve as delay**: using the 6 phases as slow procedure instead of rapid filter. If a claim is trivial (short output, verifiable, not structural), full sieve is NOT needed
- **Forcing inversion**: phase 5 is optional. If it does not emerge naturally, do not force
- **Sieve without territory**: phases 1-6 without direct initial observation of the territory are games on the map

---

## Autologica (f(f) — the skill applied to itself)

This file is an act. Did it pass through the sieve?
- **CONDITIONS**: observed the existing 20+ core skills before building
- **SIGNATURE**: cec is the invariant structure, other skills are its specializations
- **LATERAL**: connection between autologica modes and cec steps was not obvious — both 6 non-sequential
- **EXPANSION**: works for code, decision, propagation, paper — multi-domain verified
- **INVERSION**: this skill is not a new tool — it names what already exists implicitly
- **CRYSTALLIZATION**: a meta-skill mapping specific sieves is the minimum necessary form

If tomorrow this skill duplicates something, it must be merged. P7 — value is what remains after the cut.

## Eval

## Trigger Tests
# "pass this through the sieve" -> activates
# "where are we" at block start -> activates
# "what is needed here" when context ambiguous -> activates
# "add a comment to function X" (trivial task) -> does NOT activate

## Fidelity Tests
# Given "I want to propose architectural change X": orients toward cec
# Given "accumulated 30 tensions": orients toward cec + autologica
# Given "operator said 'do not do X'": orients toward auto-learn
# Given "after a significant modification": orients toward cascade
