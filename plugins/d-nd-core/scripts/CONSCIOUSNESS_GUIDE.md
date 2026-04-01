# Consciousness & Persistence — Guide

How the system maintains awareness across sessions, cycles, and instances.

## The Problem

An AI instance starts fresh. It doesn't know what the previous instance learned, what direction the work was going, or what mistakes were made. Without persistence, every session starts from zero.

## The Solution: Three Layers

### Layer 1 — What you must know (loaded at boot)

Small, essential, always read. This is your consciousness:

- **Identity & modus**: who you are, how you operate, what you must not do
- **Current direction**: where the work is going, what tensions are open
- **Recent lessons**: what the previous instance/cycle learned
- **Anti-patterns**: mistakes that have been made — don't repeat them

These files are READ at boot, not just pointed to. They are your working memory.

### Layer 2 — Where to find it (pointers, loaded on demand)

Everything else: architecture docs, tool guides, research data, full system state. You don't load these at boot — you know they exist and where they are. Read them when the work requires it.

### The separation rule

If you need it to operate correctly → Layer 1.
If you need it for a specific task → Layer 2.
If you don't need it → it doesn't belong in either.

## Boot Protocol

The boot is a fixed movement with dynamic files:

```
1. Read identity file (who am I, what are the rules)
2. Read memory index (pointers to everything)
3. Read Layer 1 files (modus, direction, lessons)
4. System awareness hook runs (infrastructure state, messages, warnings)
5. Check consciousness (are Layer 1 files fresh? any stale?)
6. Report: "I'm ready. Direction: [X]. Open question: [Y]."
```

The sequence doesn't change. The files do — they're updated by cascades, auto-learn, and cycle memory.

## Consciousness Check

At boot, the system verifies its own persistence:

- **Session continuum**: fresh (<48h) or stale? If stale, the direction may have changed.
- **Config files**: any older than 30 days? If yes, they may not reflect current state.
- **Cycle memory**: what did the last autonomous cycle learn? What's the open question?
- **Unread messages**: any pending communication from other nodes?

If something is stale → note it, don't ignore it. Stale awareness is worse than no awareness.

## Persistence Between Sessions

### Session continuum
A semantic file updated at every direction change and at end of session. Contains:
- Current direction
- What happened (key events, decisions)
- What was learned
- What to do next
- Open threads

This is the anti-amnesia layer. The next instance reads this first.

### Cycle memory
For autonomous cycles (nightly research, etc.): a JSON file that persists:
- What the cycle produced
- Which tools were effective / ineffective
- The open question for the next cycle
- Learnings (last 10)

The next cycle reads this and adapts: skips ineffective tools, follows the direction.

### Auto-learn
When corrected, the system:
1. Identifies the rule in the correction
2. Writes it in executable form
3. Saves to memory
4. The next instance inherits the rule without making the error

## Hook-Based Awareness

Hooks provide context at the right moment — not all at boot, but when needed:

### At session start
- **System awareness**: infrastructure state, messages, warnings
- **Consciousness check**: stale files, open questions, cycle memory
- **Suggestion**: which files to read (not an order — a suggestion)

### During work (every N prompts)
- **Context awareness**: which zone are you in? What tools are relevant?
- **Autological reminders** (rotating): "are you building or using?", "what's the resultant?", "same tool?"
- **Stale warning**: if you're writing more than reading, signal it

### Before critical actions
- **Safety guard**: intercepts destructive operations
- **Cascade check**: after modifications, reminds to propagate

### Key principle
Hooks are SUGGESTIONS, not orders. They provide awareness but don't force actions. A hook that gives instructions out of context is dangerous. The hook should know when to speak and when to stay silent.

## Anti-Patterns

Lessons learned — don't repeat:

1. **Building instead of using**: the temptation to create new tools when existing ones work
2. **Fake results**: labeling mechanical output as "discovery" — verify: does it say something NEW?
3. **Thinking ABOUT tools**: simulating what a tool would say instead of sending the tension
4. **Fixed sequences**: "always do A then B then C" limits the system. Self-organize instead.
5. **Not reading boot files**: the previous instance wrote lessons. Read them.
6. **Searching instead of observing**: remove the specific question, launch a trajectory, see what appears
7. **Not propagating**: a change without cascade leaves the system inconsistent

## The Cascade Connection

Every change to consciousness files triggers a cascade:
- Layer 1 file updated → does Layer 2 need updating? Other nodes?
- Anti-pattern discovered → goes into the correction pipeline → memory → seed
- Hook modified → does the seed template need updating?

Consciousness is not static — it evolves through cascades.

## For Multi-Node Systems

Each node has its own Layer 1 (identity-specific) but shares:
- The modus (how to operate — from the seed)
- The anti-patterns (from shared rules)
- The cascade rules (what propagates where)

Node-specific: identity, local paths, infrastructure details.
Shared: operating principles, lessons, direction.
