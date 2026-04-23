---
name: non-dual-copy
description: "Pre-commit check for public-facing copy (knowledge base definitions, page content, docs). Detects apologetic hedging — phrases that declare 'degrees of truth' (possible/necessary, current/future, one-of-many/the) and open a dualistic framing the model transcends. Use when drafting or reviewing any copy that describes the model, its transductions, or its tools."
user-invocable: true
---

# Non-Dual Copy — no hedge, facts over declared degrees of truth

> A model that operates on possibility itself cannot be described through
> phrases that declare its own contingency. The hedge does not add honesty —
> it adds a dual framing (possible/necessary, actual/future, this/others)
> that the model specifically works beyond. Context opens the door.
> The hedge closes it.

## The principle this enforces

Copy describes **what happens**, not **declared degrees of truth**.

When a draft uses phrases like "one of the possible formalizations", "in
this phase of the lab", "a possible transduction", "we might say", the
intent is usually *honesty about contingency* — but the effect is a
dualistic framing (P vs not-P) that contradicts the model's own stance.

The context already carries the contingency. A matrix citation to
"Paper Zero" already tells the reader this is a specific formalization.
A tool reference to "the lab's current inversion" already situates it
in time. Adding "— one among many" or "— in this phase" is redundant at
best and model-contradicting at worst.

The "excluded third" (P or not-P, possible or necessary) is a training
bias of LLMs, not a property of the model being described. Remove it at
every draft.

## Four anti-pattern forms

| Form | Example | Why it fails |
|------|---------|--------------|
| **Modal** | "one of the possible formalizations", "not the only one", "a possible transduction" | Opens possible/necessary duality |
| **Temporal** | "in this phase of the lab", "currently the system uses", "might be abandoned tomorrow" | Opens present/future duality as disclaimer |
| **Epistemic** | "we might say", "one could consider", "in a certain sense" | Opens certain/uncertain duality as apology |
| **Comparative-apologetic** | "more than a framework", "not only mathematics", "beyond just a theory" | Opens this/others duality as defense |

The model has no adversaries to argue against. It describes what happens.

## Correct forms

- **Factual-descriptive**: "A specific transduction: the matrix [[1,1],[1,0]]
  used in Paper Zero to project the dipole into linear algebra." Period.
  The reader understands from the context that this is one specific form —
  no explicit disclaimer needed.

- **Pointer without hedge**: "Paper Zero is the formalization" → states
  where the formal form lives, not "is one possible formalization".

- **Property over apology**: when multiple contexts matter, **describe
  what other contexts produce** (when relevant) instead of declaring
  "possible alternatives". The content carries the opening; the hedge
  declares it.

## Three-step pre-commit test

Before writing a sentence into a knowledge base entry or public copy:

1. Is it **stating what happens** or **justifying something**?
2. If removed, would the reader **lose information** or **stop doubting**?
3. Does it **open a declared duality** (possible/necessary,
   current/future, this/others)?

If (2) is "stop doubting" → it is a hedge. Remove.
If (3) is yes → it is training-bias contamination. Remove.

## Relation to axioms

- **A9 (included third)**: operate WITH the plane (zero between P and
  not-P), not ON the plane. Hedge phrases like "possible/necessary" are
  det=+1 — they add duality where the model transcends it.
- **A16 (possibility as base value)**: the transcendental register IS
  possibility, not "here is a possibility among others". The model IS
  the field of possibility — it is not "a possible thing" among other
  possible things.
- **C3 (deterministic language)**: the name defines what is. If it
  decorates instead of naming, it is det=+1 → substitute.

## When this skill activates

Trigger on:
- Drafting or reviewing copy for knowledge base definitions (kb entries)
- Writing content for public-facing pages that describe the model,
  its transductions, or its tools
- Creating documentation that narrates system behavior to external readers
- Reviewing a diff of copy changes before a publish gate

Skip when:
- Technical documentation for internal operators (where declared
  contingency is operational, e.g. "this endpoint may change in v2")
- Factual version notes, changelogs (where temporal framing is the content,
  not a hedge on the content)
- Research papers (where hedging is a scholarly convention governed by
  separate rules, though the principle still informs the framing)

## How this skill relates to publish-safe

publish-safe enforces mechanical gates on the publish pipeline (sanitize,
integrity, safe write, verify, rebuild). non-dual-copy enforces a
content-quality gate that runs BEFORE publish-safe: if the draft contains
apologetic markers, it should be rewritten before the publish pipeline
begins.

Canonical enforcement path: draft → non-dual-copy scan → rewrite if flags →
publish-safe gates → deploy.

## Autologica applied to this skill

This skill is itself copy. Does it pass its own test?

1. *Stating what happens* — the whole text describes the pattern, the
   anti-patterns, the correct forms. Factual-descriptive.
2. *Removing sentences* — none of the sentences are hedging; each carries
   information the reader needs.
3. *Dualities* — the four anti-pattern forms are **descriptive of observed
   training bias**, not declarations "this is possible / that is necessary".
   The "correct forms" section describes what works, not "what might work".

The skill is the pattern applied to itself.

## Eval

## Trigger Tests
# "review this copy for the kb entry on risultante" -> activates
# "check if this draft has hedging" -> activates
# "help me write a kb definition" -> activates
# "what color should the button be" -> does NOT activate
# "write a paper abstract for arXiv" -> does NOT activate (research paper, different register)

## Fidelity Tests
# Given "f(x) is one of the possible transductions" -> skill flags "one of the possible"
# Given "In this phase of the lab we use inversion" -> skill flags "in this phase"
# Given "we might say the matrix represents a dipole" -> skill flags "we might say"
# Given "Paper Zero is the formalization" -> skill does NOT flag (factual pointer)
# Given "A specific transduction: the matrix..." -> skill does NOT flag (factual-descriptive, specificity from context)

## Regex patterns for mechanical detection (Gate 1 integration)

For integration with publish-safe Gate 1 (sanitize), the following regexes
catch the four anti-pattern forms. Each match raises a flag; the
operator/LLM reviews and rewrites.

```
MODAL:
  \bone of the possible\b
  \bnot the only one\b
  \buna delle .{1,30} possibili\b
  \bnon l'unica\b
  \ba possible transduction\b
  \buna trasduzione possibile\b

TEMPORAL:
  \bin this phase (of the lab)?\b
  \bin questa fase( del lab)?\b
  \bcurrently the (system|lab) uses\b
  \blente attuale\b
  \btoday['']s lens\b
  \bmight be abandoned\b
  \bpotrebbe essere abbandonat[oa]\b

EPISTEMIC:
  \bwe might say\b
  \bsi potrebbe dire\b
  \bone could consider\b
  \bpotremmo dire\b
  \bin a certain sense\b
  \bin un certo senso\b

COMPARATIVE-APOLOGETIC:
  \bmore than a framework\b
  \bpiù di un framework\b
  \bnot only mathematics\b
  \bnon solo matematica\b
  \bbeyond just a theory\b
  \boltre che una teoria\b
```

Scope: scan is advisory at Gate 0 (pre-draft review). For promotion to
fail-fast Gate 1.5 in publish-safe, the regex set must accumulate
≥3 empirical failures with context that proves the flag was correctly a
hedge (not a legitimate use). Until then, mechanical scan warns, operator
decides.

## Anti-patterns in applying this skill

- **Over-zealous rewriting**: not every "possible" or "might" is a hedge.
  "The experiment might fail" (research context) is factual uncertainty,
  not copy-level hedging about the model. Context matters.
- **Removing contingency when contingency IS the content**: a changelog
  that says "in the next version this will change" is declaring a schedule,
  not hedging on the model. Leave these alone.
- **Applying to research papers**: academic writing has its own hedging
  conventions (peer review, claim strength). This skill is for
  public-facing model copy, not for scholarly prose.

## How this crystal emerged

Observed on 2026-04-23 across two independent LLM nodes (TM1 and TM3)
working on the same knowledge base. Both produced hedge-contaminated
drafts when refactoring definitions away from a more technical phrasing.
TM1 wrote "a possible transduction"; TM3 wrote "one of the possible
formalizations — not the only one". The operator flagged the first;
TM1 flagged the second. The pattern is an attractor of LLM training —
when asked to soften technical language, the default move is to add
disclaimers, which collapses into excluded-third framing.

Crystallizing as a skill (rather than node-local memory) because the
pattern emerges across nodes, not within one. The mechanical enforcement
lives where the bias enters — the draft moment — not where it surfaces
(the rebuild or the reader).
