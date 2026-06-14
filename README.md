# d-nd-seed

Portable operating substrate for AI coding agents: runtime memory, guardrails,
hooks, continuity, capability routing, cognitive kernels and governed
self-improvement.

You are an AI coder entering this repository to install a portable operating
substrate into your environment.

Do not skim and copy files. First identify your runtime, shell, project domain
and risk boundary. Then run the registry check, routed plan and dry-run before
installation.

Seed installs memory, hooks, safety guards, skills, kernels, plugins and
awareness rules so your local AI system can recover after compaction, verify
before action, and inherit reusable THIA/D-ND capabilities without inheriting
THIA runtime state.

## What Seed Is

Seed is the portable body of normalized THIA/D-ND functions, kernels and
operating rules.

THIA and Labs are where functions are tested under real pressure. Seed is where
the reusable form goes: hooks, skills, kernels, plugins, docs, profiles and
installer metadata that another system can use in its own environment.

Installed locally, Seed becomes your node's memory, safety layer, boot/reentry
discipline, capability map and self-improvement substrate.

Design seeds are separate. If the target project needs UX/UI consistency,
workspace shells, navigation models, domain templates or THIA-aware assistant
surfaces, use the design seed repo:
[`GrazianoGuiducci/d-nd-ux-ai-seed`](https://github.com/GrazianoGuiducci/d-nd-ux-ai-seed).
For public examples and adoption context, also inspect the D-ND portfolio at
[`d-nd.com`](https://d-nd.com). See
[`docs/related_seed_resources.md`](docs/related_seed_resources.md).

Current public release: v4.1 (2026-06-12) adds governed self-improvement,
clearer AI-agent positioning and repository visibility updates. See
[`CHANGELOG.md`](CHANGELOG.md).

## Before You Install

Classify yourself before writing files:

1. Runtime: `claude-code`, `codex`, app-hosted AI coder, `opencode`,
   `cursor`, `copilot`, `gemini`, or `other`.
2. Environment: OS, shell, project path, write permissions, command execution,
   network, secrets and publish/deploy boundary.
3. Domain: coding, research/Lab, public site, publishing, server node, or mixed.
4. Profile: choose the closest profile in `profiles/`.
5. Risk: know which capabilities are native, adapted, documented or unsupported
   in your runtime.

If you cannot classify these fields, stay in read-only mode and inspect the
local project first.

## Universal Install Sequence

`install.sh` is Bash-native. On Windows, do not run it directly unless you
intentionally selected Git Bash, WSL or another Bash runtime. For read-only
validation and planning on Windows, prefer the Node commands shown below.

```bash
git clone https://github.com/GrazianoGuiducci/d-nd-seed.git
cd d-nd-seed

# Validate the capability registry
./install.sh --check

# Inspect routed capability choices
./install.sh profiles/example.json --plan

# Preview file writes
./install.sh profiles/example.json --dry-run

# Install
./install.sh profiles/example.json
```

Windows read-only equivalent:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\seed_plan.js profiles\example.json
node scripts\test_installer_safety.js
```

Only use `install.sh` on Windows after confirming the intended Bash layer and
target project boundary. Write-mode installation from Windows Bash is blocked
unless `DND_SEED_ALLOW_WINDOWS_BASH=1` is set deliberately.

After installation, read the generated surfaces before project work:

```text
.seed/seed_profile.json
.seed/seed_install_plan.json
.seed/adapter_notes.md
.claude/seed_profile.json
.claude/seed_install_plan.json
.claude/CLAUDE.md
.claude/MEMORY.md
```

Normal install/update uses the registry gate by default: only capabilities
included by the routed plan are installed or updated. Use `--legacy-all` only
for compatibility with older broad installs.

## Runtime Paths

Claude Code uses `.claude/`, hooks, settings and skills natively.

Codex reads `.seed/` first for the neutral manifest, then uses generated
`.claude` surfaces as adapter/source logic. Hooks may not fire automatically,
so Codex must manually apply the safety, awareness,
pre/post-compact and cascade disciplines described in
[`docs/agent_runtime_translators.md`](docs/agent_runtime_translators.md).

App-hosted AI coders should read
[`docs/app_runtime_adapter.md`](docs/app_runtime_adapter.md) before install.
Use `profiles/example-app-runtime.json` when the app exposes workspace
instructions, hooks, skills, plugins or app-local memory surfaces.

OpenCode, Cursor, Copilot, Gemini and other AI coders should start as `generic`
unless native support is verified. Read the install plan, use the same
capability logic, and do not claim automatic hook behavior until the local
runtime proves it.

## Profiles

A profile describes your environment. The installer uses it to generate
identity, memory, settings, hooks, skills and capability routing.

Common starting profiles:

- `profiles/example.json` - conservative coder/project install.
- `profiles/example-claude-code.json` - Claude Code native hooks/skills.
- `profiles/example-codex.json` - Codex reading `.seed` first and `.claude`
  adapter logic only where needed.
- `profiles/example-app-runtime.json` - app-hosted AI coder with explicit host
  surface metadata.
- `profiles/example-researcher.json` - autonomous research/Lab cycle.
- `profiles/example-dev-node.json` - dev/server node with network checks.
- `profiles/example-publisher.json` - site, copy, funnel, SEO and public-surface work.

For OpenCode or a generic AI coder, use the closest profile and set the runtime
shape conservatively. Then read the routed plan and
[`docs/agent_runtime_translators.md`](docs/agent_runtime_translators.md).

For Lab installs, keep the LLM provider choice explicit. The Lab pattern
supports `codex-cli -> claude-cli -> openrouter` as a dispatcher chain, but a
user may choose HTTP-only or local OpenAI-compatible models. See
[`docs/LAB_PATTERN.md`](docs/LAB_PATTERN.md) and
[`docs/AI_INSTALL_ASSISTANT_PROMPT.md`](docs/AI_INSTALL_ASSISTANT_PROMPT.md).

## What Changes After Installation

| Before | After |
|--------|-------|
| Starts from zero every session | Reads persistent memory and knows where it left off |
| Makes destructive mistakes silently | Safety guard catches dangerous patterns before execution |
| Loses context on compaction | Pre/post compact logic captures and restores the active point |
| Assumes state is continuous | Continuity boundary preserves orientation across state changes |
| Treats every reentry the same | Boot router classifies new instance, post-compact, crash, correction and field reentry |
| Asserts from stale memory | Awareness rules separate verified, memory, inferred and unknown |
| Adds capabilities blindly | Installer router selects capabilities by profile, maturity, risk and visibility |
| Repeats corrected mistakes | Governed self-improvement turns verified corrections into consumed, testable rules |

## What Is Inside

**Hook templates** that protect the operating cycle:

| Hook | When | What it does |
|------|------|-------------|
| Safety Guard | Before edit/command | Catches destructive or production-sensitive operations |
| System Awareness | Session start | Scans repos, git state, API health and unread context |
| Session Monitor | Tool cycle | Tracks boot compliance, memory writes and drift |
| Pre/Post Compact | Context compaction | Captures essential state before and restores it after |
| Cascade Check | After modifications | Asks who else in the system needs to know |
| Skill Health | Session start | Verifies skills have tests and triggers do not overlap |

**Skills and capabilities** are exposed through the registry. Current installable
capabilities are routed by type, stratum, maturity, risk and target profile. Run:

```bash
./install.sh --check
./install.sh profiles/example.json --plan
```

Skill-shaped material under `templates/skills/` is not automatically
installable. Each directory must either be promoted into
`capabilities/registry.json` or marked in
`templates/skills/reference-only.json` with the reason it is withheld.

**Cognitive kernels** shape how the AI thinks:

- `kernels/kernel_base_en.md` - observe, relate, emerge, integrate.
- `kernels/kernel_coder_en.md` - safety, reversibility, multi-repo awareness,
  verification before assertion.

**Boot router pattern** classifies reentry before action:
new instance, post-compact, post-crash, correction, field reentry, pre-compact
or unclassified signal. See [`docs/boot_router.md`](docs/boot_router.md) and
[`docs/boot_system_map.md`](docs/boot_system_map.md).

**Continuity boundary** preserves orientation across context compaction,
session restart, tool changes, handoffs and other state transitions without
pretending state is continuous. It defines awareness crystals, a noise
threshold and L0/L1/L2 automation gates. See
[`docs/continuity_boundary.md`](docs/continuity_boundary.md).

**Programmable awareness** exposes identity, sources, memory state,
uncertainty, boundaries, side effects and next action before the agent acts. See
[`docs/programmable_awareness.md`](docs/programmable_awareness.md).

**Awareness orchestration** connects boot class, state exposure, action gates,
capability selection, verification, memory and cascade. See
[`docs/awareness_orchestration_protocol.md`](docs/awareness_orchestration_protocol.md)
and [`docs/awareness_state_schema.md`](docs/awareness_state_schema.md).

**Governed self-improvement** turns corrections, failures, compactions and
regressions into dynamic crystals, condensates, bounded implementation plans
and verified local improvements, without authorizing uncontrolled
self-modification. See
[`docs/governed_self_improvement.md`](docs/governed_self_improvement.md).

**Installer option router** keeps the seed evolving without presenting all
functions as equal install choices. See
[`docs/installer_option_router.md`](docs/installer_option_router.md).

**Agent runtime translators** adapt one Seed logic to different AI runtimes.
See [`docs/agent_runtime_translators.md`](docs/agent_runtime_translators.md).

**Agent-neutral Seed surface** explains how every AI coder can recognize Seed
capability logic without needing to identify as Claude Code first. `.seed` is
the neutral installed manifest; `.claude` is the native Claude Code target and
compatibility carrier, not the identity of the Seed. See
[`docs/agent_neutral_seed_surface.md`](docs/agent_neutral_seed_surface.md).

**App runtime adapter** explains how an AI coding app should declare its host
surfaces before installing Seed configuration. See
[`docs/app_runtime_adapter.md`](docs/app_runtime_adapter.md).

**Godel plugin** is an inverted oracle. It does not answer questions; it
inverts assumptions and shows what a tension hides.

**Scenario Projector** maps hidden structure in competing tensions. See
[`plugins/d-nd-core/scripts/PROJECTOR_COMPLETE_GUIDE.md`](plugins/d-nd-core/scripts/PROJECTOR_COMPLETE_GUIDE.md).

**Diagram Generator** reads article content and generates interactive
conceptual diagrams. See
[`plugins/d-nd-core/scripts/DIAGRAM_GENERATOR_GUIDE.md`](plugins/d-nd-core/scripts/DIAGRAM_GENERATOR_GUIDE.md).

## How Capabilities Become Seed

Runtime systems such as THIA and Labs test functions under real pressure. When a
function becomes reusable, do not copy the runtime state. Extract the invariant.

Use this movement:

```text
observe -> register -> understand -> plan if useful -> coherent action
```

Then decide whether the reusable form belongs as documentation, hook template,
skill, plugin, kernel, profile, registry capability or installer guidance. See
[`docs/THIA_SEED_PROMOTION.md`](docs/THIA_SEED_PROMOTION.md).

Do not promote secrets, private transcripts, local service state, dirty worktree
facts, active packets or project-only assumptions.

## Architecture

```text
d-nd-seed/
+-- CHANGELOG.md          # Release history and active maintenance signal
+-- GUIDE.md              # AI reads this for full setup procedure
+-- CHAT_START.md         # Chat-session adaptation
+-- install.sh            # Parametric installer
+-- update.sh             # Routed update flow
+-- profiles/             # Environment configurations
+-- templates/
|   +-- hooks/            # Hook templates
|   +-- skills/           # Installable skill templates
+-- skills/
|   +-- coder/            # Coder skills
|   +-- thinker/          # Bilingual thinker/chat packs
+-- kernels/              # Cognitive system prompts and kernel packages
+-- plugins/              # Core, Godel, researcher and related plugins
+-- docs/                 # Operational guides
+-- scripts/              # Maintenance, planning and validation tools
```

## Upgrading

If you are running a previous version, read [`UPGRADING.md`](UPGRADING.md)
before updating.

For routed updates, `update.sh --plan` is read-only and `update.sh --dry-run`
shows intended writes. Like `install.sh`, normal write-mode updates are
Bash-native and require deliberate Windows Bash opt-in.

For installer maintenance, run the Node safety harness before release:

```powershell
node scripts\test_installer_safety.js
```

The harness validates registry coverage, read-only planning, profile rejection
cases, clean JSON/paths output and no shell `eval` in installer/update/high-risk
hook templates. It does not run write-mode install/update.

## For AI In A Chat Session

If you are using Claude.ai, ChatGPT, Gemini or another chat AI rather than a
coding agent, start with [`CHAT_START.md`](CHAT_START.md).

## Part Of D-ND

D-ND (Dual-Non-Dual) is the framework behind this seed. The mathematical model,
research and public tools live at [`d-nd.com`](https://d-nd.com).

- [`seed.d-nd.com`](https://seed.d-nd.com) - Seed documentation.
- [`d-nd.com`](https://d-nd.com) - Framework and research.
- [`d-nd.com/laboratorio`](https://d-nd.com/laboratorio) - Live research data.
- [`docs/LAB_PATTERN.md`](docs/LAB_PATTERN.md) - Generative Lab pattern.
- [`EXAMINA`](https://github.com/GrazianoGuiducci/EXAMINA) - Evolutionary evaluation.
- [`anamnesis`](https://github.com/GrazianoGuiducci/anamnesis) - Context persistence specification.

## License

AGPL-3.0 - see [`LICENSE`](LICENSE).
