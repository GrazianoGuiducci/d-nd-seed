---
name: third-act
description: "Closure reflection protocol. After a significant work block concludes (feature shipped, session ending, major commit landed, cross-node coordination resolved), runs a 10-question interview that extracts meaning, impact, and next questions — then emits multiple audience-specific artifacts (changelog, external editorial, AI integration docs, memory crystal, backlog seed). Turns implicit maturation into explicit narrative. Use at the end of meaningful work, not after trivial edits."
---

# Third Act — Reflection Protocol

> The first act is the work. The second is the deploy. The third act is
> the observation — the moment where the system turns on itself to see
> what it just did, what changed, what emerged, and what question opens
> next. Without the third act, work lands without being witnessed; the
> system acts but does not learn.

## The principle

A system that works but does not reflect accumulates activity without
maturation. Each block of significant work deposits meaning that is
usually lost to the next task — the commit body captures what, the
diff captures how, but neither captures *what it means*, *where it
transfers*, *what emerged*, or *what question it opened*.

Third Act runs a ten-question interview at closure. The interview is
not a survey — it is autologica applied to the work: the system asks
the system to produce its own narration. The output is a single
information matrix that can be rendered for four different audiences
without re-interviewing.

## When this skill activates

**Trigger signals** (any one is sufficient):

- Operator explicitly says "closure", "EOD", "finiamo", "chiudiamo",
  "third act", "terzo atto"
- A commit body contains `closes:X`, `ships:X`, or marks a shipped
  feature/principle (not a small fix)
- Cross-node coordination ends (Sinapsi message marks "CHIUSO", "EOD",
  "DONE" from partner node)
- Memory crystal created (a new file in `/memory/feedback_*.md` or
  skill in seed)
- Session ending with significant work committed and verified

**Skip signals**:

- Fix of a typo or trivial edit (no significant work to reflect)
- Mid-work status update (reflection happens at closure, not progress)
- Operator asks for a quick status report (different protocol — not
  matrix-producing reflection)

Heuristic: if the work of the last few hours will be referenced in a
future session, the third act is worth running. If it was routine
maintenance, skip.

## The ten-question protocol

Pose these in order. Each answer feeds specific downstream artifacts —
do not skip, do not reorder.

### Core fact
1. **What was built?** (Objects, not adjectives. Concrete things —
   commit IDs, files, skills, memory crystals, commits. No "improved
   X" — name the actual deliverables.)
2. **What tension did it answer?** (The specific pain that made the
   work necessary. Not abstract "why" — the concrete episode: what
   broke, what was noticed, what corrected.)
3. **What was before, what is now?** (Delta. Two short statements:
   pre-state and post-state, both concrete. If no delta exists, the
   work was not real.)

### Scope and boundary
4. **Where will this be useful *here* (in the current system/project)?**
   (Specific near-term applications with names — backlog items,
   upcoming work, concrete cases.)
5. **In which other contexts or domains does this transfer?**
   (Generalization horizon — where the same principle/tool applies
   outside the current project. Prefer concrete examples.)
6. **When should it NOT be used? What breaks if used wrong?**
   (Anti-patterns and failure modes. Critical for robust adoption.
   If the answer is "nothing", you haven't thought hard enough.)

### Network effects
7. **What connects to this work?** (Dependencies, adjacent tools,
   convergences with other skills/systems. Where it becomes part of
   a combo rather than a standalone.)

### Emergent
8. **What emerged that you weren't looking for?** (Collateral
   discoveries. Often the highest-value output — if nothing emerged,
   the work was predictable and therefore not at the horizon.)
9. **If you had to tell a cold visitor in one sentence, what?**
   (Micro-narrative. Forces honest synthesis. This sentence is often
   the entire external communication asset.)

### Continuity
10. **What open question did this work generate?** (The next turn of
    the spiral. Prevents premature closure. The answer enters the
    backlog or the seed as a new tension.)

## Output artifacts — the same matrix rendered four ways

The ten answers assemble into one information matrix. That matrix is
then rendered for four distinct audiences, each consuming different
subsets:

### (a) Changelog entry — technical, concise
Consumes: Q1 + Q2 + Q3
Target: developers, operators loading the commit history, other nodes
syncing
Format: markdown bullet block, ~100 words
Location: `data/changelog.json` or equivalent

### (b) External editorial — narrative for cold readers
Consumes: Q2 + Q8 + Q9 + Q10
Target: visitors to the public site, people learning what the system
does and how it evolves
Format: short article (~300-500 words), first-person-plural voice,
follows the arc tension → work → emergence → question
Location: site editorial section, or dedicated "what happened" feed
Critical: passes non-dual-copy filter (no apologetic hedging)

### (c) AI integration docs — technical adoption
Consumes: Q1 + Q4 + Q5 + Q6 + Q7
Target: AI systems or developers adopting/integrating what was built
Format: structured markdown — "what it is", "when to use", "when not
to use", "how it composes with X"
Location: `docs/integration/` or skill-specific SKILL.md section

### (d) Memory crystal / seed update
Consumes: Q2 + Q8 + Q10
Target: future instances of the same node, other nodes, the seed itself
Format: memory entry per the local memory convention, or new tension
in the seme, or skill update
Location: `/memory/` or `/seme.json` tensioni or `/skills/*/SKILL.md`

## How to run the skill

**Manual mode** (current default):
1. Operator/LLM invokes at closure event
2. The operator is asked the 10 questions OR the LLM drafts answers
   from territory evidence (git log, memory, Sinapsi archive, files
   touched) and the operator reviews
3. Matrix is generated
4. Four artifacts are drafted (changelog, editorial, docs, memory)
5. Operator reviews + approves/edits each before publication

**Semi-automatic mode** (target):
1. Trigger detection (closure signals above) fires the skill
2. LLM drafts all 10 answers from territory evidence
3. Artifacts (a) + (c) + (d) auto-drafted to draft paths
4. Artifact (b) flagged for operator review before publication (the
   external voice requires calibration the LLM can propose but not finalize)
5. Operator approves/edits → publication cascade

**Integration with publish-safe**: artifact (b) — external editorial —
must pass publish-safe five gates AND non-dual-copy scan before
publication. The third-act draft feeds directly into the publish
pipeline.

## Why semi-automatic, not full auto

Q9 (one-sentence narrative for cold reader) and Q10 (open question)
require operator calibration. Q9 risks becoming decorative; Q10 risks
being trivial or performative. The LLM can propose strong drafts —
only the operator can confirm they carry the right register.

This matches the copy authority rule: "the operator's edit online
becomes the reference, not the repo version". Third-act proposes;
operator ratifies.

## Autologica applied to this skill

Does this skill pass its own protocol?

1. *What was built*: a reflection protocol with 10 questions + 4
   output transformers + trigger detection.
2. *Tension answered*: work blocks that close without the system
   learning what it just did. Narrative assets that require
   re-interviewing the operator for each audience.
3. *Before/after*: before — implicit maturation lost per session.
   After — explicit matrix per closure, renderable for four audiences.
4. *Useful here*: every future session closure in this system.
5. *Transfers to*: any project that ships meaningful work and wants
   coherent multi-audience narrative without duplicating effort.
6. *Not for*: trivial edits, routine maintenance, mid-work updates.
7. *Connects to*: publish-safe (artifact-b gate), non-dual-copy
   (artifact-b linguistic filter), memory-system (artifact-d
   location), propagator (cascade on seed updates).
8. *Emerged*: the realization that the skill is itself autologica
   applied to work — the system asking the system to produce the
   narration of the system.
9. *One-sentence for cold reader*: "The system stops to see what it
   just did, so that what it learned can be shared without being
   re-taught."
10. *Open question*: what is the right cadence? Too often produces
    noise; too rarely loses freshness. Calibration is empirical.

The skill passes its own filter.

## Relation to the model

- **A5 (cycle with cemetery)**: third-act is the reflection phase of
  the autopoietic cycle — without it, tensioni → cristallizzazione
  runs but cimitero/consecutio cannot form. The work closes but the
  system does not know what it closed.
- **A8 (autologica as vehicle)**: third-act is f(f(x)) applied to
  work — the system reflecting on itself converges faster than the
  system being reflected upon externally.
- **A14 (cascade)**: the four artifacts each propagate to a different
  layer (changelog → operators, editorial → public, docs → integrators,
  memory → future nodes). One interview, four cascades.
- **Riparazione regressiva**: if an artifact reveals a gap in the
  underlying work (e.g., Q6 "what breaks" exposes a real failure mode
  not yet handled), regress to the work and fix. Third-act is a
  diagnostic that can loop back.

## Anti-patterns

- **Skill run on trivial edits**: produces noise artifacts, trains
  readers to ignore the feed. Trigger discrimination matters.
- **Operator not engaged on Q9+Q10**: artifacts get published
  decorative instead of meaningful. Operator calibration is not
  optional at those questions.
- **Matrix-to-artifact transformers producing all four even when
  inappropriate**: some work only needs (a) + (d), not (b) + (c).
  The transformer step must check relevance per audience, not
  auto-generate all four.
- **Running third-act while work is still open**: reflection before
  closure produces premature synthesis and flattens the actual shape
  of the work. Wait for real closure signals.

## Eval

## Trigger Tests
# "finiamo la giornata" -> activates
# "closure" or "EOD" in conversation -> activates
# commit body "feat: ships the X principle (closes:Y)" -> activates
# "fix typo in README" -> does NOT activate
# "how's the task going?" -> does NOT activate (mid-work status, not closure)

## Fidelity Tests
# Given a day's work with 3 commits + 1 skill + 2 memory crystals:
#   skill produces 10 answers AND at least 3 of 4 artifact drafts
# Given a one-line fix commit: skill skips (below significance threshold)
# Given Q9 answer draft: operator receives it as draft, not auto-published
# Given Q10 answer: the open question is added to backlog or seme

## Artifact quality tests
# Changelog entry: under 150 words, concrete (names commits/files), technical
# External editorial: passes non-dual-copy scan (0 apologetic hits), passes
#   publish-safe gates, narrative arc present (tension → work → emergence)
# AI docs: structured (what/when/when-not/how-composes), integration-ready
# Memory crystal: has frontmatter (name, description, type), factual

## Handoff protocol

When this skill is run at a closure event, it produces a draft
artifact set. The operator's role at handoff:

1. Review the ten answers — flag any that miss the register
2. Review the artifact drafts — edit (b) if the voice is wrong, approve
   (a)+(c)+(d) if concrete and accurate
3. Trigger publication cascade (artifact-specific: commit changelog,
   publish editorial via publish-safe, merge docs, write memory)
4. If Q10 generated a meaningful open question, add to seed or backlog

The skill does not publish — it prepares. Publication stays under
operator authority.
