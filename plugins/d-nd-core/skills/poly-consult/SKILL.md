---
name: poly-consult
description: "Multi-node consultation protocol for high-leverage decisions. Dispatches the same question to N independent LLM/agent nodes in isolation, then synthesizes their responses into a summa that exposes convergence (high-confidence claims), dissensus (real uncertainty zones), and emergent points (insights no single node produced). Reduces single-node training bias. Supports recursive escalation for stable-state convergence. Use for decisions that propagate via A14 cascade — seed updates, crystallizations, advisory→mechanical promotions, high-visibility copy, lab result interpretation."
---

# Poly-Consult — multi-node consultation with summa synthesis

> A single LLM node carries its own training bias and context frame.
> For decisions that propagate through the system (A14 cascade), a
> single viewpoint reproduces that bias at every downstream node.
> Consulting N independent nodes, then synthesizing the responses into
> a summa, surfaces what each alone could not: convergence (shared
> confidence), dissensus (real uncertainty), and emergence (insights
> that arise only at intersection).

## The principle

Two observers of the same surface from different angles see different
structure — intersections reveal what lies perpendicular to any single
angle. This is geometry, not ideology. The skill formalizes that
geometry for decisions.

The protocol has three operations:

1. **Dispatch**: send the same question + context to N nodes. Each
   responds without reading the others. Isolation is the constraint
   that prevents the first responder from anchoring the second.
2. **Synthesize**: extract three structures from the N responses —
   agreement, disagreement, emergence. Output is not a vote, it is a
   matrix that preserves dissensus rather than averaging it away.
3. **Escalate** (optional, recursive): send the summa back to the same
   nodes (or expanded set) and ask the second-order question: "seeing
   this summa, does your first answer change?" Iterate to stable
   state. f(f(x)) applied to multi-agent decisions.

## When this skill activates

**Trigger signals**:
- A decision changes the seed (skills, kernel, canonical fields) →
  propagation risk via A14 cascade
- A claim is candidate for crystallization (promotion from observation
  to invariant)
- An advisory rule is candidate for promotion to mechanical gate
  (per cristallo "gate meccanico sostituisce disciplina")
- High-visibility public copy (homepage, manifesto, paper abstracts,
  announcement copy)
- Interpretation of a lab result where a single-LLM bias could
  misread the structure

**Skip signals**:
- Tactical decisions under time pressure (overhead not justified)
- Purely exploratory work (divergence is the product, not the input
  to synthesis)
- Decisions where nodes have asymmetric territory access (a node
  without context cannot contribute — invite only nodes that share
  the observation surface)

## Input specification

```yaml
question: string                    # the question or decision to consult on
context: string | reference         # background evidence, relevant files, prior state
nodes: list                         # min 2, recommended 3+
  - TM1                             # human-like operator or lab-site node
  - TM3                             # dev/infrastructure node
  - Godel                           # inversion filter (external observer)
  - other named agents              # add per relevance
mode: factual | interpretive | decisional
max_rounds: int (default 1)         # 1 = single pass; >1 = recursive
isolation: strict | relaxed         # strict = no node reads others until synth
  (default: strict)
```

## Execution protocol

### Round 1 — dispatch + independent response

For each node in `nodes`:
- Send `question` + `context` + instructions to respond without
  consulting others
- Receive response (text, structured matrix, or artifact — depending
  on mode)
- Store tagged with node identity

**Isolation discipline**: if nodes share a communication channel
(e.g., Sinapsi), the dispatcher must route each message so that no
node sees another's draft before its own is submitted. Violating
isolation collapses the consultation into a social proof loop.

### Synthesizer step

Apply three extractors to the N responses:

**AGREEMENT extractor** — claims asserted by ≥(N−1) nodes:
- Paraphrase into canonical form (the same claim may be expressed
  differently across nodes)
- Mark confidence: `unanimous` (all N), `majority` (N−1 of N)
- These are the high-confidence output points

**DISSENSUS extractor** — claims asserted by one node and denied (or
omitted) by another:
- Preserve both sides verbatim — do not resolve prematurely
- Note the disagreement axis (fact vs interpretation, scope,
  assumption)
- These are the real-uncertainty zones — the skill's highest value
  is here, not in the agreement

**EMERGENCE extractor** — claims that appear in exactly one response
and are genuinely novel (not trivial per-node variation):
- Usually surfaced by Q-style questions (what else, what next, what
  you missed)
- These are insights that only the intersection surfaces — single
  nodes would not have produced them in isolation

Output: a `summa matrix` — structured, preserving provenance, not
collapsing dissent into average.

### Optional Round 2+ — recursive escalation

When `max_rounds > 1`:
- Send the Round-1 summa back to the original nodes (or expanded set)
- Question: "Given this summa, does your position change? What
  emerges when you see what the others said?"
- Each responds independently again
- Re-synthesize
- Continue until: (a) agreement set stabilizes, OR (b) dissensus
  claims stop moving, OR (c) `max_rounds` reached

Terminating early on stability is correct — forcing convergence when
nodes have stopped moving produces false consensus.

## Output specification

```yaml
summa:
  agreement:                       # shared claims
    - claim: string
      confidence: unanimous | majority
      provenance: [node1, node2, ...]
  dissensus:                       # preserved disagreement
    - axis: string                 # what the disagreement is about
      positions:
        - node: string
          claim: string
  emergence:                       # single-node novel claims
    - node: string
      claim: string
      relevance_score: float       # synthesizer's estimate of non-triviality
  meta:
    rounds: int
    isolation: strict | relaxed
    convergence_quality: high | medium | low
    recommendation: string         # only if mode=decisional
```

## How the skill composes with others

- **third-act**: a closure third-act can trigger a poly-consult on
  Q9+Q10 (narrative + open question) when the work is high-leverage
  — the summa across nodes is richer than a single node's reflection.
  Today's manual test validated exactly this composition.
- **non-dual-copy**: any artifact output by poly-consult that will be
  published passes through the non-dual-copy filter. Multi-node
  consultation does not exempt from copy discipline.
- **publish-safe**: if the poly-consult output becomes copy, it enters
  the publish pipeline. Summa → copy is a transform that happens
  outside poly-consult itself.
- **propagator**: when summa produces a decision with cascade scope
  (affects seed, skills, canonical fields), propagator handles the
  downstream updates.

## Relation to axioms

- **A8 (autologica as vehicle)**: poly-consult is the system asking
  itself (via N instances) to produce the narration of its own
  reasoning. Recursive mode is f(f(x)) applied to multi-agent
  decisions.
- **A11 (combo)**: three or more simultaneous entities, not
  sequential. The summa is combo of N responses — emergent, not
  a sequence of consultations.
- **A9 (included third)**: the synthesizer operates on the zero
  between nodes, not on the nodes themselves. The emergent layer is
  the included third — what lives at the intersection, not in any
  single position.
- **C2 (coincidence is not proof)**: unanimous agreement is a signal,
  but not a proof. The skill preserves dissensus explicitly because
  unanimous conviction across biased observers is exactly what makes
  a collective error invisible.

## Anti-patterns

- **Collapsing dissensus into average**: the synthesizer must preserve
  disagreement. Averaging N positions into "the middle position"
  destroys the signal. If 2 nodes disagree, the decision lives in
  understanding the disagreement, not in splitting the difference.
- **Isolation violation**: if nodes read each other's drafts before
  submitting, the first responder anchors the rest. Dispatch must be
  true parallel, with isolation enforced by the dispatcher.
- **Using for trivial decisions**: the overhead is justified only for
  propagating decisions. Running poly-consult on tactical choices
  trains the system to ignore its output.
- **Auto-recursion without stop condition**: recursive mode needs a
  stability detector. Forcing N rounds produces false convergence —
  nodes start to echo the summa rather than add value.
- **Nodes without shared territory**: consulting TM3 (VPS access) and
  a node without it on a VPS-specific question collapses into "TM3
  knows, others don't" — not genuine consultation. Verify symmetric
  observability before dispatching.

## Example — today's manual proto-consult as reference

The closure reflection run manually today (third-act on 23/04) was a
proto-poly-consult:

- Question: "what happened today, what emerged, what question opens?"
- Nodes: TM1 (deployer/catcher angle), TM3 (skill-builder angle)
- Mode: interpretive
- Isolation: strict (each produced matrix before reading the other)
- Rounds: 1

Synthesizer observations:

- **Agreement** (Q10 especially): both nodes formulated near-verbatim
  the same open question about skill-catalog topology. This is the
  highest-confidence signal of the day.
- **Dissensus**: Q1+Q3 — what was built and what changed depended on
  angle. Not disagreement proper; divergence by observation surface.
  Correctly preserved, not resolved.
- **Emergence**: Q8 — both nodes identified "distributed regressive
  repair" (skill finding gap of another skill before activation), but
  each surfaced a different aspect of it. The composition of the two
  emergence claims is richer than either alone.

Q9 (cold-visitor one-sentence) produced two *productively divergent*
narratives — different hooks for different reader types. Synthesizer
preserved both rather than averaging.

The informal execution worked. Formalization into this skill captures
the pattern for future high-leverage decisions.

## Eval

## Trigger Tests
# "should we promote X to a mechanical gate?" -> activates (decisional)
# "what does this lab result mean?" -> activates (interpretive, if bias risk)
# "here's a paper abstract, is it ready to publish?" -> activates (high visibility)
# "fix this typo" -> does NOT activate (tactical, no leverage)
# "what color for the button?" -> does NOT activate (not propagating decision)

## Fidelity Tests
# Given 3 node responses: skill produces summa with agreement + dissensus + emergence
# Given 2 identical responses: agreement fills with unanimous; dissensus empty;
#   emergence empty → synthesizer flags "low diversity — consider expanded node set"
# Given a dissensus claim: skill preserves both positions verbatim, does not resolve
# Given isolation violation (node B saw node A's draft): skill flags "contaminated
#   round, escalate with strict isolation"
# Given max_rounds=3 but stability at round 2: skill stops at round 2 and reports
#   "converged early"

## Synthesis quality tests
# Agreement extractor paraphrases claims into canonical form (same claim across
#   different wordings groups together)
# Dissensus preserves axis of disagreement (fact vs interpretation vs scope)
# Emergence marks relevance_score (non-trivial emergence distinguished from
#   per-node variation)
# Meta.convergence_quality reflects dissensus density, not agreement count alone
