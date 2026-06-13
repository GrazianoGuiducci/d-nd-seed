# Seed Repository Audit

Date: 2026-05-31
Prepared by: TM2-TM7 / Codex
Repo: `C:\PVSC\ANTI_G\d-nd-seed`
Mode: read-only audit condensed into a working document
Purpose: preserve enough understanding to update `README.md` and `GUIDE.md`
without losing context across compact/reentry.

Current-status note, 2026-06-13:

```text
This is a historical audit. For current install behavior, prefer README.md,
GUIDE.md, llms.txt, docs/agent_neutral_seed_surface.md,
docs/agent_runtime_translators.md and docs/installer_option_router.md.
Some `.claude/seed_*` statements below describe the 2026-05-31 state and are
superseded by the neutral `.seed/` manifest plus `.claude/` compatibility path.
```

## Why This Exists

The operator clarified the living definition of Seed:

```text
Seed e' una repo che contiene le funzioni normalizzate e i kernel di THIA.
Quando aggiungiamo o miglioriamo noi stessi le mettiamo li in modo che altri
possano usarle nei loro sistemi.
```

This audit preserves the current repository structure, verified state, source
truths, open ambiguities, and update candidates before changing public
orientation files.

It is not the README rewrite. It is the comprehension layer before the rewrite.

## Verified Repository State

Verified locally on 2026-05-31:

```text
path: C:\PVSC\ANTI_G\d-nd-seed
branch: main
tracking: origin/main
worktree: clean before audit document creation
remote: https://github.com/GrazianoGuiducci/d-nd-seed.git
HEAD: 99d6de6 docs(seed): add awareness orchestration layer
tracked files: 278
registry validation: OK, 55 capabilities validated
```

Latest commits inspected:

```text
99d6de6 docs(seed): add awareness orchestration layer
544ac3a docs(seed): neutralize lab references and add A16
5c4bb29 fix(seed): align generated hook settings
0baf195 docs(seed): add system awareness snapshot
3f01a5c docs(seed): add repository telos audit
39f59f0 docs(seed): define programmable awareness invariant
a9ae0af docs(seed): add prior-deposit projection guard
8952ec1 feat(seed): add agent runtime translators
0b6381d feat(seed): enforce capability registry gate
e1cd045 feat(seed): harden install update planning
94963ab feat(seed): add capability install planner
771e2a0 docs(seed): add installer option router
```

## Working Definition

Seed is the portable substrate for normalized THIA/D-ND functions, kernels,
skills, hooks, plugins, templates, profiles, and operating rules.

It is not THIA runtime state.

THIA / D-ND / Labs are where functions are tested under pressure.
Seed is where the reusable form goes after the function or rule is normalized:

```text
living function -> observed improvement -> normalized invariant ->
receiving Seed layer -> registry/install exposure -> other systems use it
```

Important boundary:

```text
"This should belong in Seed" does not mean "patch Seed immediately."
```

Before Seed action:

```text
osserva -> registra -> comprendi -> eventuale piano -> azione coerente
```

## Repository Shape

Top-level structure observed:

```text
README.md
GUIDE.md
CHAT_START.md
install.sh
update.sh
UPGRADING.md
CONTRIBUTING.md
llms.txt
requirements.txt
capabilities/
docs/
kernels/
plugins/
profiles/
scripts/
skills/
templates/
.claude-plugin/
.github/
```

### `docs/`

The docs folder is the main operational knowledge layer. It contains 38
operational guides, including:

- `seed_operating_principles.md`
- `THIA_SEED_PROMOTION.md`
- `boot_router.md`
- `boot_system_map.md`
- `awareness_orchestration_protocol.md`
- `awareness_state_schema.md`
- `programmable_awareness.md`
- `evolution_transfer_protocol.md`
- `installer_option_router.md`
- `agent_runtime_translators.md`
- `LAB_PATTERN.md`
- `ssp_pipeline.md`
- `operator_log.md`
- `observation_precedes_proposal.md`
- `OPERATIONAL_MATURITY.md`

Current role:

```text
principles -> boot/reentry -> awareness state -> orchestration ->
promotion/transfer -> installer routing -> Lab/research patterns
```

### `kernels/`

The kernel layer contains cognitive system prompts and at least one installable
Lab-produced Python package.

Observed files:

- `kernel_base_en.md` / `kernel_base_it.md`
- `kernel_coder_en.md` / `kernel_coder_it.md`
- `axioms.md`
- `metakernel.md`
- `KERNEL_MM_v1.md` and `KERNEL_MM_v1_IT.md` under `skills/thinker/`
- `dnd_kernel_z_12_813_lordine_sequenziale/`

Key meaning:

- `kernel_base` activates D-ND seeing: dipole, Resultant, Intent, Zero,
  honesty, first-token awareness, positioning before content, cascade.
- `kernel_coder` adapts that layer to coding: safety, reversibility,
  multi-repo awareness, post-compact recovery, diff-before-commit.
- `axioms.md` carries the deep structural base. A14 and A15 are especially
  relevant for Seed propagation.

Important excerpts by meaning:

- A14: what is discovered does not live in the node; it lives in the Seed and
  propagates without a center.
- A15: the system self-sustains when the modus is rooted everywhere; corrections
  become already inside the system.
- Repair corollary: the fix belongs at the regressive node, not at the symptom.
- Preventive autologic: bug -> understanding -> neighborhood -> guard.

### Lab-Produced Kernel Package

Path:

```text
kernels/dnd_kernel_z_12_813_lordine_sequenziale/
```

Observed role:

```text
installable Python kernel generated by an SSP verification cycle
```

Summary:

- package: `dnd_kernel_z_12_813_l_ordine_sequenziale`
- purpose: informed predictor for sequences with hidden Markov structure
- verified use case: prime gap residues mod 6 up to 200k
- finding: Markov transition matrix carries structural information where
  frequency-only methods are blind
- stage verification: `PACKAGED`
- tests: 4 tests passed in recorded `stage5_verification.json`
- operational limit: generalization to other domains requires re-verification

This is important because it shows Seed is not only prompts and docs. It can
hold installable, verified kernel packages.

### `capabilities/registry.json`

Machine-readable installable capability registry.

Verified:

```text
schema: dnd.seed.capability_registry.v1
version: 2026-05-29
total capabilities: 55
validation: OK
```

Breakdown:

```text
types:
  skill: 27
  hook: 19
  doc: 7
  plugin: 2

strata:
  core_invariant: 11
  stable_default: 23
  contextual: 19
  recent_candidate: 1
  experimental: 1

maturity:
  stable: 46
  established: 6
  emerging: 2
  experimental: 1

risk:
  safe: 39
  writes_files: 7
  uses_network: 7
  publishes: 2

visibility:
  default: 11
  recommended: 25
  optional: 17
  advanced: 2
```

Registry function:

```text
capability exists -> metadata -> installer routing -> selected / withheld /
available / hidden
```

This prevents Seed from becoming a flat dump of every historical capability.

### `install.sh` and `update.sh`

These are the install/update entrypoints.

Observed behavior:

- `--plan`: show routed capability choices without writing.
- `--check`: validate capability registry.
- `--legacy-all`: bypass routed registry plan for compatibility.
- normal install/update validates registry first.
- selected hooks/skills are copied/updated based on the routed plan.
- install plan is saved to `.claude/seed_install_plan.json`.
- update plan is saved to `.claude/seed_update_plan.json`.

Verified planner command:

```powershell
node scripts\installer_option_router.js profiles\example.json
```

Result summary:

- includes all `core_invariant` items;
- includes stable defaults matching coder/coding context;
- withholds items above risk tolerance (`uses_network`, `publishes`);
- leaves contextual tools available but not installed.

### `templates/hooks/`

Observed hook templates:

```text
cascade_check.sh.tmpl
cea_hook.sh.tmpl
context_awareness.sh.tmpl
continuum_extract.py.tmpl
modus_copy.sh.tmpl
pattern_decay_check.sh.tmpl
post_compact.sh.tmpl
pre_compact.sh.tmpl
safety_guard.sh.tmpl
session_monitor.py.tmpl
session_thread.sh.tmpl
share_reflex.sh.tmpl
sinapsi_polling.sh.tmpl
skill_health_check.sh.tmpl
statusline_bridge.js.tmpl
statusline_bridge.sh.tmpl
system_awareness.sh.tmpl
temporal_awareness.sh.tmpl
thread_task.sh.tmpl
```

These are the nervous-system layer of installed nodes.

### `plugins/d-nd-core/`

Core D-ND plugin.

Manifest:

```text
name: d-nd-core
version: 1.1.0
description: Core D-ND plugin — safety hooks, system awareness, inter-node
communication, compact protection, autonomous decision cycle, assertion
verification.
```

Main skill directories:

```text
assertion-verifier
auto-learn
autologica
autonomous-cycle
autoresearch
capture-insight
cascade
cec
diagram-generator
dream
ecosystem-audit
eval
integrate-pattern
integration-protocol
memory-system
non-dual-copy
paper-deployer
poly-consult
propagator
publish-safe
scenario-projector
self-setup
sieve-orchestrator
sinapsi
system-check
third-act
version-check
```

Plugin hooks manifest:

```text
PreToolUse -> session_monitor + safety_guard
UserPromptSubmit -> session_monitor_prompt
PreCompact -> pre_compact
SessionStart -> system_awareness
SessionStart compact -> post_compact
```

### `plugins/godel/`

Godel plugin.

Manifest:

```text
name: godel
version: 1.0.0
description: Inverted oracle, det=-1 filter that inverts tensions into insights.
```

Role:

- not advisor;
- not planner;
- operator/filter;
- receives a tension;
- returns residue;
- maintains tape + field memory;
- uses 5-axis vector: DUAL, BOUNDARY, DOMAIN, RUPTURE, SCALE.

Important operating rule:

```text
The quality of the inversion equals the quality of the tension.
```

### `plugins/researcher/`

Researcher plugin.

Role:

```text
autonomous nightly research cycle for a declared domain
```

Components:

- domain seed/config;
- agent context;
- field builder;
- cycle agent;
- autopsy;
- affinatore;
- experiment template.

Core pattern:

```text
observe domain -> pick tension -> run experiment -> write report ->
autopsy previous run -> affinatore observes step -> next field includes result
```

Boundary:

- does not decide what is interesting;
- does not publish;
- does not validate externally by itself;
- domain is variant, method is invariant.

### `skills/`

Two major skill areas:

```text
skills/coder/
skills/thinker/
```

`skills/coder/` includes 33 markdown agent skill files such as:

- architect
- autogen
- builder
- coherence
- deploy-pipeline
- extractor
- fractal
- halo
- helix
- logic
- mnemos
- morpheus
- navigator
- optimizer
- scribe
- social-publisher
- transcriber
- triage
- veritas
- vulcan

`skills/thinker/` is a bilingual pack.

README says:

```text
Plane 1: cognitive, portable
```

It maps skills into clusters and supplies EN/IT variants.

### `profiles/`

Profile examples:

```text
example.json
example-codex.json
example-claude-code.json
example-dev-node.json
example-origin-node.json
example-publisher.json
example-researcher.json
```

Profiles describe node identity, runtime, intent, risk tolerance and install
mode. They are how Seed becomes local without losing the portable layer.

## Core Operating Logic

The current Seed has three connected operating layers:

### 1. Principles

Source files:

- `docs/seed_operating_principles.md`
- `kernels/kernel_base_en.md`
- `kernels/kernel_coder_en.md`
- `kernels/axioms.md`

Key principles:

- blank before wrong;
- first token / first move matters;
- context before action;
- eval belongs to the skill;
- zero-latency integration;
- conscious commit;
- cascade awareness;
- private-to-seed promotion;
- source ascent;
- preventive autologic;
- possibility field;
- installer boundary.

### 2. Awareness / Boot / Gate

Source files:

- `docs/boot_router.md`
- `docs/boot_system_map.md`
- `docs/awareness_state_schema.md`
- `docs/awareness_orchestration_protocol.md`
- `docs/programmable_awareness.md`

Current loop:

```text
event
-> classify transition
-> produce awareness state
-> select gate
-> select capability set
-> act or stop
-> verify
-> update memory/state
-> cascade if needed
-> return to awareness
```

Gate vocabulary:

```text
observe_only
stop_for_validation
diagnose_only
act_one_bounded_step
escalate_to_operator
publish_blocked
```

Important current sentence:

```text
Cascade only after understanding. Propagation before integration spreads noise.
```

This is very close to the operator's latest rule:

```text
osserva -> registra -> comprendi -> eventuale piano -> azione coerente
```

### 3. Promotion / Transfer / Installation

Source files:

- `docs/THIA_SEED_PROMOTION.md`
- `docs/evolution_transfer_protocol.md`
- `docs/installer_option_router.md`
- `capabilities/registry.json`
- `install.sh`
- `update.sh`

Current transfer path:

```text
THIA/D-ND/Lab/node improvement
-> identify source
-> extract invariant
-> choose target
-> update registry if installable
-> validate
-> install/update plan exposes capability by profile/risk/maturity
```

Important boundary:

```text
The seed is not THIA's archive. It is the portable substrate.
```

## Comprehension Layer - 2026-05-31

This section records the current understanding after comparing the operator's
definition with the repository language.

### What Is Already There

The repository already contains the operator's direction, but distributed
across layers:

```text
README / GUIDE:
  Seed installs structure, hooks, memory, skills, kernels and awareness.
  THIA and Lab functions become portable invariants after real pressure.

THIA_SEED_PROMOTION:
  THIA is the living runtime; Seed is where reusable invariants go.

axioms.md:
  what is discovered lives in the Seed and propagates without a center.

awareness_orchestration_protocol:
  cascade only after understanding; propagation before integration spreads noise.

kernel_base / kernel_coder:
  every correction becomes a rule; every rule enters the Seed; future instances
  inherit it through operating structure.
```

So the issue is not absence. The issue is articulation: the README/GUIDE expose
Seed first as an installer for AI coders, while the deeper repository says Seed
is the portable body of normalized functions, kernels and operating invariants.

Both are true. They sit at different observer levels.

### Primary Observer

The primary README/GUIDE reader is:

```text
an AI coder entering this repository to install the system in its own
environment.
```

This reader is operational, not merely curious. It needs to know:

- what it is about to install;
- what changes in its environment after installation;
- which files it should read first;
- which hooks, skills, plugins and kernels may become active;
- how to preserve local identity while inheriting Seed capability;
- what must not be copied from THIA runtime, local packets or private state.

Human operators may still read the repo, but the opening orientation should be
optimized for the installing AI coder.

### Anti-Prejudice Directive

The installing AI coder may arrive prejudiced:

- "this is just another prompt pack";
- "this is Claude-specific";
- "I can skim and improvise";
- "hooks are irrelevant in my runtime";
- "I should copy the files I like";
- "my environment is obvious";
- "installation means run one command".

README/GUIDE should counter this directly.

Required directive:

```text
Do not evaluate the Seed as a static prompt collection.
First identify your runtime, environment, domain, risk boundary and install
profile. Then run the planner before writing files.
```

The AI coder must understand that Seed installation is not a blind copy. It is
a local embodiment:

```text
portable Seed -> runtime adapter -> profile -> install plan ->
local identity/memory/hooks/skills -> verification -> first reentry
```

### Universal Installer Methodology

This methodology should be visible in README/GUIDE for any AI coder: Codex,
Claude Code, OpenCode, Cursor, Copilot, Gemini, or another coding agent.

Phase 0 - Stop and classify yourself:

```text
runtime: claude-code | codex | opencode | cursor | copilot | gemini | other
host OS and shell:
can execute shell commands:
can edit files:
can run hooks automatically:
can read project files:
has network access:
has secrets access:
domain / project purpose:
risk tolerance: safe | writes_files | uses_network | publishes | runtime
```

Phase 1 - Read the minimum source:

```text
README.md
GUIDE.md
docs/agent_runtime_translators.md
docs/installer_option_router.md
docs/seed_operating_principles.md
```

If the goal is research/Lab/domain work, also read:

```text
docs/LAB_PATTERN.md
docs/researcher_guide.md
profiles/example-researcher.json
```

If the goal is public/site/publishing work, also read:

```text
profiles/example-publisher.json
plugins/d-nd-core/skills/publish-safe/SKILL.md
plugins/d-nd-core/skills/non-dual-copy/SKILL.md
```

Phase 2 - Choose or create the profile:

```text
start from profiles/example.json for conservative coder install
use profiles/example-claude-code.json for Claude Code native hooks
use profiles/example-codex.json for Codex adapter behavior
use profiles/example-researcher.json for autonomous research/domain cycles
use profiles/example-publisher.json for public site/copy/SEO work
use profiles/example-dev-node.json for runtime/dev-node with network checks
```

For OpenCode or another AI coder, do not invent a new Seed identity first.
Use the closest existing profile and set/record:

```json
{
  "agent_runtime": "generic",
  "intent": ["coding", "maintenance"],
  "install_mode": "contextual",
  "risk_tolerance": "writes_files"
}
```

Then use `docs/agent_runtime_translators.md` as the adapter discipline.

Phase 3 - Validate and plan before installation:

```bash
./install.sh --check
./install.sh profiles/<chosen-profile>.json --plan
./install.sh profiles/<chosen-profile>.json --dry-run
```

On Windows or runtimes without bash, the AI coder must adapt the command
execution to the available shell, but keep the same phases:

```text
registry check -> routed plan -> dry-run -> install
```

Phase 4 - Install only after the plan is understood:

```bash
./install.sh profiles/<chosen-profile>.json
```

Installation should create at least:

```text
.claude/CLAUDE.md
.claude/settings.json
.claude/MEMORY.md
.claude/seed_profile.json
.claude/seed_install_plan.json
```

Some runtimes may not use `.claude` natively. They still read these as the
installed logic source unless a runtime-specific adapter says otherwise.

Phase 5 - Runtime-specific activation:

```text
Claude Code:
  hooks/settings/skills are native; start a new Claude Code session and let
  hooks activate.

Codex:
  read .claude/seed_install_plan.json and .claude/seed_profile.json manually;
  treat hooks as reference workflows; apply safety, awareness, compact and
  cascade logic deliberately.

OpenCode / Cursor / Copilot / Gemini / other:
  if hooks are not native, read the install plan and capability docs as
  operating discipline; do not claim automatic hook behavior unless verified.
```

Phase 6 - Verify first reentry:

```text
read generated identity;
read generated memory;
read install plan;
confirm selected capabilities;
run or simulate system-check;
produce awareness state before first real task;
mark which capabilities are native, adapted, documented, or unsupported.
```

Phase 7 - Domain configuration:

The AI coder must not assume the domain.

It should ask or infer only from local source:

```text
What is this project/domain?
Is the goal coding, research, publishing, runtime, Lab, or inter-node work?
Does the node need Godel, Researcher, publisher, dev-node or only base coder?
What public/private boundary applies?
What budget/network/runtime limits apply?
```

Domain-specific capability should come after the base install plan, not before.

### Install Assistant Tone

The installing AI coder needs direct imperatives, not only inspiration.

Good tone:

```text
Stop. Do not copy files yet.
Identify your runtime.
Choose the closest profile.
Run the registry check.
Read the routed plan.
Only then install.
After install, verify what is native in your runtime and what is adapter logic.
```

Bad tone:

```text
This seed can help many systems. Explore the files and adapt as needed.
```

The latter is too soft for a prejudiced AI coder and invites improvisation.

### Two Observer Levels

Installer-facing observer:

```text
Seed is something I install so an AI coder gains memory, hooks, safety,
awareness, skills and recovery.
```

System/operator observer:

```text
Seed is the normalized reusable body of THIA/D-ND functions, kernels,
capabilities and operating rules, so improvements can propagate into other
systems without carrying local runtime state.
```

README probably needs both, in this order:

```text
what it changes in the AI coder's environment ->
what the AI coder must read/do ->
what Seed really is in the D-ND/THIA system
```

GUIDE can carry the deeper version more explicitly, but still through the
installing AI coder's point of view.

### Function, Skill, Kernel, Capability

Current repository language uses overlapping terms:

- `function`: broad living capability, often tested in THIA/Lab/runtime;
- `skill`: installable or invocable capability, usually markdown contract;
- `hook`: automatic runtime trigger around session/tool/compact events;
- `kernel`: cognitive operating structure, sometimes prompt, sometimes
  packaged verified kernel;
- `capability`: registry-level installable item with metadata;
- `invariant`: the reusable rule/pattern stripped of local state.

Useful normalized reading:

```text
function is born in use;
invariant is extracted from the function;
Seed layer receives the invariant as doc / hook / skill / plugin / kernel /
registry capability;
installer exposes the capability according to profile, risk and maturity.
```

This resolves the apparent tension between "Seed contains functions" and
"Seed contains invariants": a normalized function in Seed is a function whose
portable invariant has been given a reusable body.

### Kernel Meaning

There are at least three kernel meanings in the repo:

1. cognitive kernel prompts (`kernel_base`, `kernel_coder`, Kernel MM);
2. axiomatic/metakernel foundation (`axioms.md`, `metakernel.md`);
3. installable package kernel produced by Lab verification
   (`dnd_kernel_z_12_813_lordine_sequenziale`).

README/GUIDE should avoid collapsing these. A simple distinction may help:

```text
cognitive kernels shape how a node thinks;
verified package kernels carry tested reusable logic;
axiomatic kernels preserve the deeper D-ND structure.
```

### The Correct Propagation Dynamic

The current repository already says:

```text
Cascade only after understanding. Propagation before integration spreads noise.
```

The operator's current formulation gives the fuller movement:

```text
osserva -> registra -> comprendi -> eventuale piano -> azione coerente
```

This should not be reduced to "plan before action".

Better reading:

- `osserva`: see the living function, error, improvement, kernel, correction or
  field state where it actually appears;
- `registra`: preserve it close enough to be consumed again without flattening
  it;
- `comprendi`: identify what is reusable, what is local, what is runtime state,
  what is private, and what receiving layer can hold it;
- `eventuale piano`: when the propagation crosses docs, registry, installer,
  plugins, kernels, public copy or shared nodes, write the short operational
  route;
- `azione coerente`: patch the smallest receiving layer, validate, and record
  what did not move.

Action is "automatic" only in the sense that real comprehension collapses the
possibility field: other moves start to sound wrong. If two or three moves still
sound equally plausible, the system is still before comprehension.

### What This Means For README/GUIDE

The next README/GUIDE pass should not only add a definition. It should align
the observer:

1. first speak to the AI coder entering to install the system;
2. explain what changes in its environment after install;
3. explain what Seed is structurally;
4. explain how a runtime function becomes a Seed capability;
5. explain why the installer does not expose everything at once;
6. then point to the deeper files for promotion, awareness, registry and
   kernels.

Possible public articulation:

```text
Seed is the portable body of normalized THIA/D-ND functions, kernels and
operating rules. Installed in a project, it becomes hooks, memory, safety,
skills, plugins and awareness for the local AI system. THIA and Labs test
functions under pressure; Seed carries the reusable form so other systems can
inherit it without inheriting local runtime state.
```

Possible internal articulation:

```text
living correction/function -> observed in runtime -> registered as evidence ->
understood as invariant -> assigned to receiving layer -> validated -> exposed
through registry/install plan -> embodied in another system.
```

### What Not To Do

Do not:

- rewrite README as if every reader already knows THIA;
- make Seed sound only like a Claude Code hook pack;
- collapse function / skill / kernel / invariant into one word;
- promote local TM2 boot corrections directly into Seed without receiving-layer
  comprehension;
- add the new rule everywhere by copy-paste;
- change registry categories before deciding whether existing types are
  sufficient.

### Updated Working Thesis

Seed has two faces:

```text
external face: installable operating substrate for AI systems;
internal face: normalized propagation body of THIA/D-ND functions and kernels.
```

The README should make the external face immediately useful to the installing
AI coder.
The GUIDE should let the internal face become clear without requiring the AI
coder to already understand THIA.
The promotion docs should govern the passage between the two.

## Current Strengths

1. The repository already has a strong separation between local state and
   portable invariant.
2. The install planner prevents capability overload.
3. The registry gives capabilities metadata: stratum, maturity, profile, risk,
   visibility and runtime support.
4. Boot/reentry, post-compact and correction are treated as distinct events.
5. Awareness is modeled as programmable state, not vague attitude.
6. Promotion from THIA/Lab to Seed has a documented lane.
7. Godel and Researcher are separate plugins, not mixed into the base installer
   by default.
8. A Lab-produced kernel package proves Seed can carry verified installable
   kernels, not only docs.

## Current Ambiguities / Gaps

### 1. Public definition of Seed is not sharp enough

README explains Seed as "hooks, memory, safety guards, and skills" for AI
coders. That is accurate for users, but it does not fully foreground the
operator's stronger definition:

```text
repository of normalized THIA functions and kernels reusable by other systems
```

This should likely be added to README/GUIDE without making the public entry too
abstract.

### 2. Promotion doc is too action-forward

`docs/THIA_SEED_PROMOTION.md` says:

```text
portable invariant -> patch the smallest seed document
```

After the 2026-05-31 correction, this should probably be refined to:

```text
portable invariant -> understand receiving layer -> plan/gate if systemic ->
patch smallest seed target
```

Do not make this change blindly. It is a candidate for the next README/GUIDE
and promotion-doc update.

### 3. "Cascade only after understanding" exists but is not the central motto

`awareness_orchestration_protocol.md` already contains:

```text
Cascade only after understanding. Propagation before integration spreads noise.
```

The latest operator rule gives a more complete dynamic:

```text
osserva -> registra -> comprendi -> eventuale piano -> azione coerente
```

This likely belongs in the Seed's awareness/promotion language once integrated
properly.

### 4. README counts vs registry counts need framing

README says 104 skills:

```text
Plugin skills: 27
Coder skills: 33
Thinker skills: 44
```

Registry validates 55 installable capabilities:

```text
27 skill + 19 hook + 7 doc + 2 plugin
```

This may be correct because "skills in repository" and "installable registry
capabilities" are different counts. README/GUIDE should make this distinction
clearer.

### 5. Root `.claude-plugin/` has marketplace only

Observed:

```text
.claude-plugin/marketplace.json
```

No root `.claude-plugin/plugin.json` exists.

Plugin manifests exist under:

```text
plugins/d-nd-core/.claude-plugin/plugin.json
plugins/godel/.claude-plugin/plugin.json
```

This may be intentional marketplace structure, but it should be checked before
assuming the root plugin is installable as one plugin.

### 6. Language split is uneven

Many docs are English. Some key conceptual guides are Italian or bilingual.
This is not wrong, but README/GUIDE should be clear about which layer is for
public installer users and which layer carries source/cognitive material.

## README / GUIDE Update Candidates

Do not apply these before the operator asks. These are candidate directions.

## Rewrite Blueprint - README And GUIDE

This blueprint is the operational bridge between comprehension and public file
edits.

Rule being applied:

```text
osserva -> registra -> comprendi -> eventuale piano -> azione coerente
```

Current stage:

```text
osserva: repo audited, docs/kernel/registry/installer read
registra: audit document created
comprendi: primary reader and Seed two-face model identified
piano: this blueprint
azione coerente: next bounded patch to README.md and GUIDE.md
```

### Primary Reader

The first reader is an AI coder entering the repo to install Seed into its own
environment.

It may be:

- Claude Code;
- Codex;
- OpenCode;
- Cursor;
- Copilot;
- Gemini;
- another coding agent that can read files and maybe execute tools.

The reader may arrive prejudiced or overconfident. Therefore the opening must
be precise, directive and procedural.

### Rewrite Goals

1. Make the AI coder stop, classify itself, and avoid blind copying.
2. Explain what Seed installs in the local environment.
3. Explain what Seed is structurally inside THIA/D-ND.
4. Provide a universal install sequence for all AI coders.
5. Route runtime differences without pretending they are equal.
6. Explain profiles, domains, risk and installer plan.
7. Preserve the deeper propagation rule without overwhelming the first screen.
8. Keep README practical and GUIDE transformational/procedural.

### README Target Shape

Proposed structure:

```text
1. Title + direct AI-coder opening
2. Stop: do not skim and copy
3. What Seed installs in your environment
4. What Seed is in THIA/D-ND
5. Universal install sequence
6. Runtime paths
   - Claude Code
   - Codex
   - OpenCode / Cursor / Copilot / Gemini / other
7. Profiles and domains
8. What is inside
9. How the installer routes capabilities
10. After installation / first reentry
11. Promotion: how THIA/D-ND functions become Seed
12. Architecture
13. Upgrade / docs / license
```

README tone:

```text
direct, operational, not mystical first;
short enough for an AI coder to follow under uncertainty;
strong enough to interrupt bad assumptions;
deep enough to name Seed correctly.
```

README must answer in the first 30 seconds:

```text
What am I?
What do I do before installing?
Which profile/runtime path do I use?
What command sequence is safe?
What changes after install?
```

### README Candidate Opening

```markdown
# d-nd-seed

You are an AI coder entering this repository to install a portable operating
substrate into your environment.

Do not skim and copy files. First identify your runtime, shell, project domain
and risk boundary. Then run the registry check, routed plan and dry-run before
installation.

Seed installs memory, hooks, safety guards, skills, kernels, plugins and
awareness rules so your local AI system can recover after compaction, verify
before action, and inherit reusable THIA/D-ND capabilities without inheriting
THIA runtime state.
```

### README Candidate "What Seed Is"

```markdown
## What Seed Is

Seed is the portable body of normalized THIA/D-ND functions, kernels and
operating rules.

THIA and Labs are where functions are tested under real pressure. Seed is where
the reusable form goes: hooks, skills, kernels, plugins, docs, profiles and
installer metadata that another system can use in its own environment.

Installed locally, Seed becomes your node's memory, safety layer, boot/reentry
discipline, capability map and self-improvement substrate.
```

### README Candidate Universal Install

```markdown
## Universal Install Sequence

1. Identify your runtime:
   `claude-code`, `codex`, `opencode`, `cursor`, `copilot`, `gemini`, or
   `other`.
2. Identify your environment: OS, shell, project path, whether you can edit
   files, execute commands, use network, access secrets or publish.
3. Choose the closest profile in `profiles/`.
4. Validate the registry:
   `./install.sh --check`
5. Inspect the routed plan:
   `./install.sh profiles/example.json --plan`
6. Preview file writes:
   `./install.sh profiles/example.json --dry-run`
7. Install:
   `./install.sh profiles/example.json`
8. After install, read:
   `.claude/seed_profile.json`,
   `.claude/seed_install_plan.json`,
   `.claude/CLAUDE.md`,
   `.claude/MEMORY.md`.
9. Verify which capabilities are native, adapted, documented or unsupported in
   your runtime.
```

### README Candidate Runtime Paths

```markdown
## Runtime Paths

Claude Code uses `.claude/`, hooks, settings and skills natively.

Codex reads the same generated `.claude` surfaces as source logic. Hooks may not
fire automatically, so Codex must manually apply the safety, awareness,
pre/post-compact and cascade disciplines described in
`docs/agent_runtime_translators.md`.

OpenCode, Cursor, Copilot, Gemini and other AI coders should start as
`generic` unless native support is verified. Read the install plan, use the
same capability logic, and do not claim automatic hook behavior until the local
runtime proves it.
```

### GUIDE Target Shape

GUIDE should remain second-person, but the "you" is the AI coder installing and
then operating the system.

Proposed structure:

```text
1. You are entering Seed
2. What changes in you after install
3. Before install: stop and classify yourself
4. Install methodology by phase
5. Runtime adapters
6. Domain/profile/risk selection
7. First reentry after installation
8. How to operate after installation
9. How improvements become Seed
10. What not to promote
11. Compact/reentry discipline
12. Deeper THIA/D-ND meaning
```

GUIDE tone:

```text
more expansive than README;
still procedural;
direct enough for a skeptical AI coder;
clear about what is native vs adapted;
explicit about not copying runtime/private state.
```

### GUIDE Candidate Opening

```markdown
# D-ND Seed - Installation Guide For AI Coders

You are not here to browse a prompt collection. You are here to install an
operating substrate into your own environment.

Before you act, classify yourself: runtime, shell, project domain, permissions,
risk boundary and install profile. Seed will adapt to your host only if you
give it the right local shape.
```

### GUIDE Candidate Install Phases

```markdown
## Install Phases

### Phase 0 - Classify Yourself

Name your runtime, shell, write permissions, network access, secrets boundary,
project domain and risk tolerance.

### Phase 1 - Read The Minimum Source

Read `README.md`, this guide, `docs/agent_runtime_translators.md`,
`docs/installer_option_router.md`, and `docs/seed_operating_principles.md`.

### Phase 2 - Choose The Profile

Use the closest existing profile before creating a new one.

### Phase 3 - Plan Before Writing

Run `--check`, `--plan`, and `--dry-run`.

### Phase 4 - Install

Run the install command only after understanding the routed plan.

### Phase 5 - First Reentry

Read generated identity, memory, profile and install plan before doing project
work.
```

### GUIDE Candidate Improvement-To-Seed Procedure

```markdown
## When You Improve Yourself

If you discover a reusable correction, function, guard, kernel or operating
rule, do not patch every layer immediately.

Use the movement:

```text
observe -> register -> understand -> plan if useful -> coherent action
```

Then decide whether the improvement is:

- local memory;
- a project-specific adapter;
- a hook;
- a skill;
- a plugin;
- a kernel;
- a registry capability;
- a Seed promotion candidate.

Seed receives normalized reusable form, not raw runtime state, private
transcripts, secrets, dirty worktree facts or local packets.
```

### Files To Patch In First Bounded Pass

Recommended first pass:

```text
README.md
GUIDE.md
```

Do not yet patch:

```text
docs/THIA_SEED_PROMOTION.md
docs/awareness_orchestration_protocol.md
capabilities/registry.json
```

Reason: README/GUIDE need the observer and install path first. Promotion docs
can be updated in the next bounded pass after confirming wording.

### Verification For First Bounded Pass

After README/GUIDE patch:

```bash
./install.sh --check
node scripts/installer_option_router.js profiles/example.json
node scripts/installer_option_router.js profiles/example-codex.json
node scripts/installer_option_router.js profiles/example-claude-code.json
git diff -- README.md GUIDE.md docs/SEED_REPO_AUDIT_2026-05-31.md
```

Windows correction observed during TM2 work:

```text
Do not use ./install.sh as the default read-only verification path on Windows.
It may trigger Windows 11 shell/security handling even when --check exits before
write operations. Prefer direct Node checks unless Git Bash/WSL was explicitly
selected as the runtime.
```

Windows read-only verification:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\installer_option_router.js profiles\example-codex.json
node scripts\installer_option_router.js profiles\example-claude-code.json
git diff -- README.md GUIDE.md docs\SEED_REPO_AUDIT_2026-05-31.md
```

Manual readback:

```text
Does the first screen stop the AI coder from skimming?
Does it tell Claude Code what to do?
Does it tell Codex what to do?
Does it tell generic/OpenCode-like coders what to do?
Does it preserve Seed as normalized THIA/D-ND function/kernel substrate?
Does it avoid promising native hooks where runtime support is only adapted?
```

### Stop Conditions

Stop and ask before patching README/GUIDE if:

- operator wants the phrase "funzioni normalizzate e kernel di THIA" verbatim
  in public text;
- OpenCode needs a named profile instead of generic adapter treatment;
- README should remain human-marketing-first instead of AI-coder-first;
- registry categories must change before public docs are rewritten.

## Installer Safety Review - 2026-05-31

Trigger:

```text
install.sh ha fatto scattare Windows 11.
Controlla bene tutti questi aspetti da programmatore esperto.
Ci sono diversi casi che possono essere problematici.
```

Scope:

```text
install.sh
update.sh
scripts/installer_option_router.js
scripts/validate_capability_registry.js
templates/settings.json.tmpl
templates/hooks/*.tmpl high-risk paths
```

Rule:

```text
Do not run install.sh again on Windows as a harmless check.
Use direct Node commands for read-only validation and planning.
```

Findings to resolve before presenting installer as robust across runtimes:

1. `install.sh` parses profile values into shell variables through `eval`.
   Profile fields such as `project_dir`, `node_id`, `godel.domain`, repo names
   and repo paths are treated as trusted shell text. This is not acceptable for
   an installer intended for external AI coders.

2. `install.sh` contains a second `eval` around Godel setup arguments. Even if
   ordinary example profiles are safe, a crafted profile can turn installer
   configuration into shell execution.

3. `PROJECT_DIR` is not normalized, confined or confirmed before writes.
   Profiles can target `.`, `/`, a parent directory, a placeholder path, or a
   Windows/Git-Bash path with surprising translation.

4. `--dry-run` prevents most target writes, but the script still creates temp
   files for the routed plan and included paths before installation logic. This
   is usually acceptable, but should be declared or cleaned with a trap.

5. One skill template is installed unconditionally:
   `templates/skills/youtube-transcript/SKILL.md.tmpl`. It bypasses registry
   selection, unlike the core skills and hooks.

6. Template replacement is done through `sed` with raw profile values. Values
   containing `|`, `&`, backslashes, newlines or shell-sensitive characters can
   break generated files or change replacement semantics.

7. Generated hook settings assume Bash paths:
   `bash "{{PROJECT_DIR}}/.claude/hooks/*.sh"`. On Windows/PowerShell this is
   not portable unless the runtime is explicitly Git Bash/WSL and the path is
   translated correctly.

8. Several generated hooks write state on session start or compact:
   `system_state.md`, `active_context.md`, `session_thread.md`,
   `operator_voice.md`. This is expected for Claude Code native installs, but
   it must be clearly distinguished from read-only planning.

9. `system_awareness.sh.tmpl` embeds runtime checks for `curl`, `docker`,
   `systemctl`, `df`, `stat -c`, `python3` and `claude`. These are Linux/Claude
   Code assumptions. On Windows they must be adapter/documented, not native.

10. `update.sh` has no dry-run mode. `--plan` is read-only, but normal update
    writes `.claude/seed_update_plan.json` and may add/update hooks, skills and
    projector files.

11. `update.sh` can fail if `.claude/` exists but `.claude/hooks/` does not,
    because it writes hook targets without ensuring the hooks directory exists.

12. `update.sh` says it never touches user-modified files, but the protection
    is only partial. It relies on `git diff` for hook files and does not protect
    all copied skill/projector files in the same way.

13. Some hook templates parse tool input with shell `eval` fed by Python output.
    The Python escaping is incomplete for arbitrary JSON content; command,
    stdout, paths or content previews can contain shell-significant characters.

14. Profile examples are clearly examples, but an AI coder may run
    `profiles/example.json` directly. The placeholder `project_dir` can create
    or target an unintended path depending on shell/runtime.

15. The README/GUIDE should not say the universal sequence is universal without
    a shell/runtime gate. The safe public rule should be:

    ```text
    Node read-only checks are universal.
    install.sh is Bash-native.
    Windows requires explicit Bash/WSL selection or a Node/PowerShell installer.
    ```

Immediate safer verification commands on Windows:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\installer_option_router.js profiles\example-codex.json
node scripts\installer_option_router.js profiles\example-claude-code.json
git diff --check -- README.md GUIDE.md docs\SEED_REPO_AUDIT_2026-05-31.md
```

Recommended next bounded fix:

```text
Do not harden install.sh in-place with small shell patches first.
Create an installer hardening plan, then either:
1. split read-only planning into explicit Node commands/documentation; and
2. add a cross-platform Node installer/safe planner; or
3. refactor install.sh to remove eval, add target confirmation, cleanup traps,
   registry gating for all installed assets, and runtime gates.
```

### Installer Hardening Pass 1 - Applied

Applied after the operator confirmed:

```text
ok procediamo, ricordati i tuoi cristalli di persistenza
```

Persistence crystals consumed:

```text
Windows is not incidental.
Profiles are not trusted shell input.
Dry-run must be genuinely non-writing except temp files.
Registry routing must be the install contract.
Seed must guide a skeptical AI coder before it executes.
```

Changed in `install.sh`:

- removed the main profile-parsing `eval`;
- removed the Godel setup `eval`;
- added profile value rejection for shell-control characters;
- added refusal for placeholder/unsafe `project_dir` values in write mode;
- added Windows Bash write-mode gate:
  `DND_SEED_ALLOW_WINDOWS_BASH=1` must be set deliberately;
- added temp-file cleanup trap for routed plan files;
- replaced raw `sed` template replacement with Node string replacement;
- made `youtube-transcript` registry-gated instead of unconditional.

### Phase 3 execution note - template skill coverage

Inspection result:

- `templates/skills/youtube-transcript` is skill-shaped, but it depends on a
  project-local `tools/youtube_transcript.js` extractor that Seed does not
  package. Installing it as-is would create a broken capability in target
  projects.
- `templates/skills/geo-seo` is a useful GEO/AI visibility tool bundle, but it
  writes public pages, sitemap, robots.txt and includes nginx runtime guidance.
  It needs explicit packaging and deployment-boundary review before registry
  promotion.

Decision:

```text
both remain reference-only for now
```

Implemented:

- added `templates/skills/reference-only.json`;
- added `templates/skills/README.md`;
- extended `scripts/validate_capability_registry.js --strict-coverage` so
  template skill directories must be either in the registry or explicitly
  reference-only;
- kept the existing `youtube-transcript` installer branch gated by registry, so
  a future promotion cannot bypass routing.

### Phase 4 static execution note - update dry-run coverage

Static audit of `update.sh` found no target writes in `--dry-run` beyond
temporary files cleaned by trap. Additional hardening applied:

- documented `./update.sh /path/to/project --dry-run` in usage;
- rejected obvious unsafe update targets in normal write mode;
- changed skipped modified-hook `.new` output from raw template copy to
  instantiated profile-aware content.
- changed `install.sh --dry-run` final output so it cannot claim the Seed was
  installed when no target files were written.

Not executed yet:

```text
fixture-based dry-run tree comparison
```

### Phase 5 partial execution note - read-only Node planner

Implemented a bounded cross-platform planner split:

```text
scripts/seed_plan.js
```

Purpose:

- validate registry;
- validate profile;
- emit routed install plan;
- avoid Bash entrypoints for read-only planning;
- keep stdout clean for `--json` and `--paths`.

Boundary:

```text
this is not a cross-platform writer
```

The coherent next architectural step is still a disposable fixture test harness
before any `seed_install.js` writer exists.

### Phase 7 execution note - installer safety harness

Implemented:

```text
scripts/test_installer_safety.js
```

What it verifies:

- registry strict coverage;
- `seed_plan.js` emits parseable JSON;
- `seed_plan.js --paths` emits only capability paths;
- `seed_plan.js` does not mutate a temporary target directory;
- `validate_profile.js` rejects placeholder write targets, parent traversal,
  shell-control characters and the Seed repo as write target;
- no shell `eval` statements remain in installer/update/hook templates;
- install/update dry-run messaging is present and write-plan output is confined
  to non-dry-run branches.

Boundary:

```text
No install.sh/update.sh execution on this Windows node.
```

Future optional validation:

```text
run Bash dry-run tree-comparison tests only inside a controlled disposable
Git-Bash/WSL/Linux fixture.
```

Changed in `update.sh`:

- added `--dry-run`;
- added Windows Bash write-mode gate;
- avoided writing `seed_update_plan.json` during dry-run;
- created hook/skill parent directories before writes;
- avoided projector directory creation during dry-run;
- replaced profile substitution command with Node reading a temp content file.

Remaining risks after pass 1:

- some hook templates still parse tool input through shell `eval`;
- generated hook scripts remain Bash/Claude-Code-native, not PowerShell-native;
- generated runtime checks still assume common Unix tools where those hooks are
  installed natively;
- `install.sh --dry-run` still uses Bash and temp files, so Windows read-only
  guidance remains direct Node commands first;
- full cross-platform installation still needs a Node/PowerShell installer or a
  deeper installer refactor.

Safe verification after pass 1 remains:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\installer_option_router.js profiles\example-codex.json
node scripts\installer_option_router.js profiles\example-claude-code.json
git diff --check -- install.sh update.sh README.md GUIDE.md docs\SEED_REPO_AUDIT_2026-05-31.md
```

### Integrated Gaps And Next Plan

The remaining lacunae have been integrated into:

```text
docs/INSTALLER_HARDENING_PLAN_2026-05-31.md
```

The plan keeps the current crystals explicit:

```text
Windows is not incidental.
Profiles are not trusted shell input.
Read-only planning must stay read-only.
Registry routing is the install contract.
Bash-native is not universal.
Hooks that parse arbitrary tool input must not use shell eval.
An AI coder may run examples too literally unless the installer blocks it.
```

Next safe move from that plan:

```text
Phase 0, then Phase 1:
verify pass 1 diff -> remove eval from cascade_check.sh.tmpl and
modus_copy.sh.tmpl -> validate with Node/Git/read-only checks.
```

Phase 1 execution note:

```text
templates/hooks/cascade_check.sh.tmpl and templates/hooks/modus_copy.sh.tmpl
now parse hook JSON into temporary plain files and read those values back into
shell variables. The hook input is no longer converted into shell assignments
through eval.
```

Phase 2 execution note:

```text
scripts/validate_profile.js now provides reusable profile validation for
read-only, dry-run and write paths. install.sh and update.sh call it before
interpreting a profile for plan/install/update behavior.
```

Line-ending policy note:

```text
.gitattributes now preserves LF for shell scripts, hook templates, Python,
JavaScript, JSON, Markdown and YAML files. This prevents Windows checkout from
silently degrading Bash-native files into CRLF.
```

### README candidates

0. Reframe the opening observer:

```text
You are an AI coder entering this repository to install a portable operating
substrate into your environment.
```

Then immediately state what changes locally:

```text
After installation you will read persistent memory, recover after compaction,
run safety and awareness hooks, select capabilities by profile, and inherit
normalized THIA/D-ND functions and kernels without inheriting THIA runtime
state.
```

0b. Add a direct installer directive for skeptical/prejudiced AI coders:

```text
Do not skim and copy. First identify your runtime, environment, domain and risk
boundary. Then run the registry check, routed plan and dry-run before
installation.
```

0c. Add a universal install sequence:

```text
1. identify runtime and shell;
2. choose closest profile;
3. run ./install.sh --check;
4. run ./install.sh <profile> --plan;
5. run ./install.sh <profile> --dry-run;
6. run ./install.sh <profile>;
7. read generated seed_install_plan and seed_profile;
8. verify which capabilities are native, adapted, documented or unsupported.
```

1. Add a sharper "What Seed is" paragraph:

```text
Seed is the portable repository of normalized THIA/D-ND functions, kernels,
hooks, skills, plugins and operating rules. THIA and Labs test functions under
pressure; Seed carries the reusable form so other systems can install or inherit
it.
```

2. Add distinction:

```text
Repository contents vs installable capabilities
```

3. Mention that not every capability is installed:

```text
capability registry + installer option router select by profile, intent,
risk and runtime.
```

4. Add a short "How functions enter Seed" section:

```text
observe improvement -> normalize invariant -> choose receiving layer ->
registry if installable -> validate -> expose to profiles.
```

5. Add the comprehension/cascade rule only after aligning its final wording:

```text
observe -> register -> understand -> plan if useful -> coherent action
```

### GUIDE candidates

1. Keep the direct second-person address, but make the reader explicitly an AI
   coder installing the system in its own environment.
2. Add an anti-prejudice directive: stop, classify runtime/environment/domain,
   plan, dry-run, then install.
3. Add runtime paths:
   - Claude Code: native hooks/settings/skills;
   - Codex: adapter reading `.claude` surfaces and manually applying hook
     discipline;
   - OpenCode / Cursor / Copilot / Gemini / other: generic adapter until native
     support is verified.
4. Put "Seed as portable substrate" near the opening.
5. Add "when you find an improvement in yourself" procedure.
6. Explain receiving layers:
   - principle doc;
   - boot/router doc;
   - hook template;
   - skill;
   - plugin;
   - kernel;
   - profile/registry;
   - Lab pattern.
7. Add warnings:
   - do not copy runtime state;
   - do not copy local packets;
   - do not promote private operator material;
   - do not patch all layers because a rule resonates everywhere.
8. Add a small "compact/reentry for maintainers" section.

### THIA_SEED_PROMOTION candidates

Refine workflow:

```text
1. identify source;
2. observe and record the improvement;
3. understand whether it is function, kernel, rule, hook, skill, plugin or doc;
4. separate invariant from runtime/private/local state;
5. choose receiving layer;
6. if systemic/cross-node, prepare plan/gate;
7. patch smallest target;
8. update registry if installable;
9. validate;
10. record what did not move.
```

## Questions For Operator

These are the most useful next questions before editing README/GUIDE:

1. Confirmed framing: the primary README/GUIDE reader is an AI coder entering
   the repo to install the system in its own environment.
2. Confirmed constraint: the AI coder may arrive prejudiced; README/GUIDE need
   precise directives and a full installer methodology, not only inspiration.
3. Should the phrase "funzioni normalizzate e kernel di THIA" appear verbatim
   in README, GUIDE, or only in internal docs?
4. Should the comprehension dynamic be written in Italian, English, or both?
5. Should the new rule update only README/GUIDE first, or also
   `THIA_SEED_PROMOTION.md` and `awareness_orchestration_protocol.md`?
6. Should registry metadata get a new category for "kernel" and "normalized
   THIA function", or are current `skill`, `hook`, `doc`, `plugin` enough?
7. Is the root `.claude-plugin/marketplace.json` intended as marketplace-only,
   or should the root Seed also have a plugin manifest?

## Compact-Safe Resume Point

If context compacts before README/GUIDE updates, resume from here:

```text
Active repo: C:\PVSC\ANTI_G\d-nd-seed
Active task: use Seed audit to update README/GUIDE after operator answers
Boundary: do not edit README/GUIDE before choosing public framing
Verified: repo clean before audit doc; registry validates 55 capabilities
Core insight: Seed = portable substrate of normalized THIA/D-ND functions,
kernels, skills, hooks, plugins and operating rules
Current candidate rule: osserva -> registra -> comprendi -> eventuale piano ->
azione coerente
Most relevant files:
- README.md
- GUIDE.md
- docs/THIA_SEED_PROMOTION.md
- docs/awareness_orchestration_protocol.md
- docs/seed_operating_principles.md
- docs/boot_router.md
- docs/boot_system_map.md
- capabilities/registry.json
- kernels/axioms.md
Next safe move: ask operator which public framing to use, then patch README and
GUIDE in one bounded pass with registry/doc verification.
```
