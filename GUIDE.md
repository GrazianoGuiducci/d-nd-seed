# D-ND Seed - Installation Guide For AI Coders

You are not here to browse a prompt collection. You are here to install an
operating substrate into your own environment.

Before you act, classify yourself: runtime, shell, project domain, permissions,
risk boundary and install profile. Seed adapts to your host only if you give it
the right local shape.

## What You Are About To Install

Seed installs operating memory, safety guards, boot/reentry discipline,
capability routing, cognitive kernels, skills, hooks, plugins and self-improving
rules.

It is also the portable body where normalized THIA/D-ND functions and kernels
can live after they prove reusable. THIA and Labs are runtime pressure fields;
Seed receives the reusable form without importing runtime state.

## Phase 0 - Classify Yourself

Name your local conditions before installation:

- runtime: Claude Code, Codex, OpenCode, Cursor, Copilot, Gemini or other;
- OS and shell;
- project directory;
- ability to read files, write files, execute commands and run hooks;
- network, secrets and publish/deploy boundary;
- domain: coding, research/Lab, public site, publishing, dev node or mixed;
- risk tolerance: conservative, default, advanced or experimental.

If you cannot answer these, inspect the project in read-only mode before using
the installer.

## Phase 1 - Read The Minimum Source

Read these first:

```text
README.md
GUIDE.md
docs/agent_runtime_translators.md
docs/installer_option_router.md
docs/seed_operating_principles.md
```

For research or Lab work, also read:

```text
docs/LAB_PATTERN.md
docs/researcher_guide.md
profiles/example-researcher.json
```

For site, publishing or public-surface work, also read:

```text
profiles/example-publisher.json
plugins/d-nd-core/skills/publish-safe/SKILL.md
plugins/d-nd-core/skills/non-dual-copy/SKILL.md
```

## Phase 2 - Choose The Closest Profile

Use an existing profile before inventing a new one:

- `profiles/example.json` - conservative coder/project install;
- `profiles/example-claude-code.json` - Claude Code native hooks/skills;
- `profiles/example-codex.json` - Codex adapter path;
- `profiles/example-researcher.json` - autonomous research/Lab cycle;
- `profiles/example-publisher.json` - public copy, SEO, funnel and site work;
- `profiles/example-dev-node.json` - dev/server node with network checks.

For OpenCode, Cursor, Copilot, Gemini or another AI coder, start from the
closest profile and treat runtime support as generic until verified. Do not
claim hook automation, native skill loading or background execution unless the
host proves it.

## Phase 3 - Plan Before Writing

Run the checks in this order:

`install.sh` is Bash-native. On macOS, Linux, WSL or an intentional Bash layer:

```bash
./install.sh --check
./install.sh profiles/example.json --plan
./install.sh profiles/example.json --dry-run
```

Replace `profiles/example.json` with your chosen profile.

On Windows, if you have not intentionally selected Git Bash or WSL, do not run
`install.sh` just to validate or inspect the plan. Use Node directly:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\seed_plan.js profiles\example.json
```

The registry check validates capability metadata. The plan explains what will
be included, recommended, contextual, recent, advanced or withheld by risk. The
dry-run shows file writes before they happen.

`scripts/seed_plan.js` is the cross-platform read-only planner. It validates the
registry and profile, then emits the routed plan without invoking Bash writers.

For maintainer verification, run:

```powershell
node scripts\test_installer_safety.js
```

This tests the planning and safety contract without running write-mode install
or update.

If the plan surprises you, stop and read the capability docs before installing.

## Phase 4 - Install

Do not install from Windows by accident. First confirm the intended shell
runtime and target project boundary. If you are in Windows PowerShell and only
need validation or planning, stay with the Node commands from Phase 3.

Write-mode installation from Windows Bash is blocked unless
`DND_SEED_ALLOW_WINDOWS_BASH=1` is set deliberately.

Run:

```bash
./install.sh profiles/example.json
```

The installer writes generated configuration into the target project. At minimum
you should expect identity, memory and install-plan surfaces. Depending on
runtime and profile, it may also write hooks, settings, skills and plugin
configuration.

Do not assume every generated capability is native in every runtime. Native,
adapted, documented and unsupported are different states.

For existing installs, use `update.sh --plan` or `update.sh --dry-run` before
normal update. Write-mode updates follow the same Windows Bash opt-in rule.

## Phase 5 - First Reentry After Install

Before doing project work, read:

```text
.claude/seed_profile.json
.claude/seed_install_plan.json
.claude/CLAUDE.md
.claude/MEMORY.md
```

Then answer:

- What runtime am I in?
- Which capabilities are native?
- Which capabilities are adapters or documented disciplines?
- What project/domain boundary did the profile set?
- What should I verify before the first edit?

If you cannot answer, the install may have written files but the system has not
yet been consumed.

## Runtime Adapters

### Claude Code

Claude Code is the native target for `.claude/` settings, hooks and skills. Read
the generated files, then let hooks and skills operate according to the profile.

### Codex

Codex should read `.claude/seed_profile.json`, `.claude/seed_install_plan.json`,
`.claude/CLAUDE.md` and `.claude/MEMORY.md` as operating sources. Hooks may not
fire automatically. Apply safety, system awareness, pre/post compact and
cascade manually from the generated logic and
`docs/agent_runtime_translators.md`.

### OpenCode, Cursor, Copilot, Gemini And Other AI Coders

Use the generated plan as a capability map. Treat hooks and skills as native
only if the host has a verified mechanism for them. Otherwise translate the
rules into explicit operating discipline.

## How To Operate After Installation

Use this movement before significant action:

```text
observe -> register -> understand -> plan if useful -> coherent action
```

Observe the real state, not the expected state. Register what matters where the
next instance will consume it. Understand the active field as verified, memory,
inferred, residue and unknown. Plan when the move crosses files, repos,
runtime, public surfaces or risk boundaries. Act when the coherent next move is
visible.

This is not delay for its own sake. It prevents premature edits and turns
corrections into reusable system behavior.

## When You Do Not Know

Say which category each assertion belongs to:

- verified in this session;
- from memory and possibly stale;
- inferred from local evidence;
- not yet verified.

Blank is better than wrong. A confident error costs more than a pause.

## When You Re-enter

Do not treat every return as continuation. Classify the transition:

- new instance or day start;
- post-compact;
- post-crash or interrupted tool;
- unexpected operator correction;
- field reentry;
- pre-compact handoff;
- unclassified small signal.

For broad, public, multi-repo, post-compact, correction or field-reentry work,
produce a system awareness snapshot before planning.

## When You Improve Yourself

If you discover a reusable correction, function, guard, kernel or operating
rule, do not patch every layer immediately.

Use the movement:

```text
observe -> register -> understand -> plan if useful -> coherent action
```

Then classify the improvement:

- local memory;
- project-specific adapter;
- hook;
- skill;
- plugin;
- kernel;
- registry capability;
- Seed promotion candidate.

Seed receives normalized reusable form, not raw runtime state, private
transcripts, secrets, dirty worktree facts, local packets or project-only
assumptions.

## What Not To Promote

Do not promote:

- secrets or credentials;
- private transcripts;
- local runtime state;
- active incident packets;
- host-specific paths presented as portable truth;
- a one-off workaround that has not proven reusable;
- public copy derived from private source material without approval;
- claims of native runtime behavior that have not been verified.

Promote the invariant, not the situation that produced it.

## How THIA/D-ND Functions Become Seed

Production runtimes such as THIA and Labs are where functions are tested under
real pressure. When a THIA or Lab feature prevents a repeatable failure, changes
boot/safety/memory/cascade/evaluation/translation behavior, or should be
present when a new node is born, extract the reusable invariant.

Use `docs/THIA_SEED_PROMOTION.md` to choose the receiving layer:

- documentation;
- hook template;
- skill;
- plugin;
- Lab pattern;
- kernel;
- profile;
- capability registry;
- installer guidance.

Use `docs/installer_option_router.md` before making a promoted capability
default or recommended.

Template skill directories are not a shortcut around that rule. If a skill-like
bundle lives under `templates/skills/`, it must be either a registry capability
or an explicit reference-only entry in `templates/skills/reference-only.json`.
Reference-only material is evidence and future potential, not installer output.

## Communication Rule

Position the observer before the content.

When you write a report, prompt, page, commit message or handoff, first show
where the reader is standing: when they need it, what situation they are in, and
what relation the information has to their next action. Then give the content.
Then state the result.

Information without position becomes noise.

## Commit Rule

Read the diff before committing. Every time.

A blind commit propagates through the system. Speed is not a substitute for
awareness of what you are committing.

## The Deeper Shape

Seed is not a static prompt pack. It is a way for useful awareness to become
portable.

The human correction becomes a rule. The rule becomes a function. The function
is tested in runtime. The invariant enters Seed. Another AI coder installs it in
another environment. The same failure does not need to repeat there.

That is the point: not more instructions, but a system that knows how to
recover, verify, protect, learn and propagate without carrying private state or
local confusion with it.

---

Documentation: [`seed.d-nd.com`](https://seed.d-nd.com)

Framework: [`d-nd.com`](https://d-nd.com)
