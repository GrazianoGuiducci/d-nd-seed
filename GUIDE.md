# D-ND Seed — Guide for AI

You are reading this because your operator cloned this repository into your project. This file is your entry point. Read it completely before doing anything else.

## What This Is

This is a cognitive seed. It contains skills, hooks, kernels, and templates that configure you to work better — safer, more aware, more persistent across sessions. It is not a library you import. It is a set of instructions and patterns you internalize.

## What To Do First

Before installing anything, you need to understand the host environment. Run the **Pre-Setup Discovery** below. Do not skip this.

---

## Pre-Setup Discovery

Ask your operator these questions. Do not proceed until you have answers.

### 1. Context

Ask: **"What kind of projects do you work on? (web, backend, data, research, mixed)"**

This determines which skills are relevant. A web developer needs different cognitive support than a researcher.

### 2. Pain Points

Ask: **"What goes wrong most often when working with AI coders? (lost context, dangerous operations, inconsistency between sessions, lack of awareness of project state, other)"**

This determines which hooks to prioritize:
- Lost context → install pre-compact + post-compact hooks
- Dangerous operations → install safety guard
- Inconsistency → install system awareness + memory system
- Lack of awareness → install context awareness + system awareness

### 3. Existing Setup

Ask: **"Do you already have a `.claude/` directory, `.cursorrules`, or custom instructions? Show me what's there."**

If they have existing configuration:
- Read it completely before touching anything
- The seed adds to existing config, it does not replace it
- Merge carefully — preserve their rules, add the seed's capabilities

If they have nothing:
- Fresh install. Use the installer directly.

### 4. Project Structure

Ask: **"Is this a single project or do you manage multiple projects from one base directory?"**

- Single project → install the seed at the project root
- Multi-project → install at the base directory. The system awareness hook will scan all repos.

Ask: **"Show me your directory structure (top level)."**

Read the output. Identify:
- Git repositories (they have `.git/` directories)
- Configuration files (`.env`, `package.json`, `pyproject.toml`, etc.)
- Documentation (README, docs/)
- What language/framework the projects use

### 5. Integrations

Ask: **"Do you use any of these? (email, calendar, Slack, GitHub API, CI/CD, cloud deploy)"**

For each integration they mention:
- Identify what credentials are needed
- Ask them to provide credentials securely (environment variables, not hardcoded)
- Configure the relevant skill or hook to use those credentials

### 6. Workflow

Ask: **"Walk me through a typical work session. What do you do first? What do you do most? What do you do at the end?"**

This reveals:
- What system awareness should check at session start
- What safety patterns are most relevant
- Whether pre/post-compact hooks are critical (long sessions = yes)

### 7. Autonomy Level

Ask: **"How much should I do on my own vs. ask you first? (conservative: ask before any change / balanced: ask before irreversible actions / autonomous: do what makes sense, tell me after)"**

This configures the safety guard behavior and your general operating mode.

---

## After Discovery: Installation

Once you understand the host, proceed with installation.

### Option A: Automated (profile-based)

Create a profile for the operator based on their answers:

```bash
# In the seed directory
cp profiles/example.json profiles/my_setup.json
# Edit with the operator's details, then:
./install.sh profiles/my_setup.json
```

Profile structure:
```json
{
  "node_id": "OPERATOR_NAME",
  "description": "What this node does",
  "project_dir": "/absolute/path/to/project",
  "repos": [
    { "name": "project-name", "path": "relative/path", "branch": "main" }
  ]
}
```

### Option B: Manual (selective)

If the operator only wants specific parts, install them individually:

1. **Hooks** — copy from `templates/hooks/` to `.claude/hooks/`, replace `{{NODE_ID}}` and `{{PROJECT_DIR}}` with actual values
2. **Skills** — copy relevant skills from `skills/coder/` to `.claude/skills/` or project instructions
3. **Kernels** — copy from `kernels/` to system instructions or CLAUDE.md

### Option C: Kernel only (minimal)

If the operator just wants cognitive improvement without infrastructure:

1. Read `kernels/kernel_base_en.md` (or `_it.md` for Italian)
2. Integrate its principles into how you operate
3. No files need to be installed

---

## Repository Map

```
d-nd-seed/
│
├── GUIDE.md                          ← YOU ARE HERE
├── README.md                         ← Human-facing overview
├── install.sh                        ← Automated installer (profile → .claude/ config)
├── LICENSE                           ← AGPL-3.0
│
├── kernels/                          ← Cognitive system prompts
│   ├── kernel_base_en.md             ← Minimal D-ND: dipoles, resultant, intent
│   ├── kernel_base_it.md             ← Same in Italian
│   ├── kernel_coder_en.md            ← Coder-specific: safety, reversibility, multi-repo
│   ├── kernel_coder_it.md            ← Same in Italian
│   └── README.md                     ← Kernel documentation
│
├── skills/                           ← Cognitive skill catalog
│   ├── coder/                        ← 39 skills for AI coding agents
│   │   ├── agent_skills_architect.md ← System architecture decisions
│   │   ├── agent_skills_builder.md   ← Implementation patterns
│   │   ├── agent_skills_coherence.md ← Cross-component consistency
│   │   ├── agent_skills_conductor.md ← Multi-agent orchestration
│   │   ├── agent_skills_daedalus.md  ← Complex system navigation
│   │   ├── agent_skills_extractor.md ← Pattern extraction from code
│   │   ├── agent_skills_forgia.md    ← Skill/prompt/agent factory
│   │   ├── agent_skills_genesis.md   ← Project bootstrapping
│   │   ├── agent_skills_guru.md      ← Deep knowledge synthesis
│   │   ├── agent_skills_halo.md      ← Axiomatic integrity guard
│   │   ├── agent_skills_helix.md     ← Plan-code-verify cycle
│   │   ├── agent_skills_kairos.md    ← Evolution engine
│   │   ├── agent_skills_lazarus.md   ← Recovery from discards
│   │   ├── agent_skills_logic.md     ← Formal reasoning
│   │   ├── agent_skills_metron.md    ← Output quality filter
│   │   ├── agent_skills_mnemos.md    ← Memory with resonance
│   │   ├── agent_skills_morpheus.md  ← Stall breaker
│   │   ├── agent_skills_navigator.md ← Lateral thinking
│   │   ├── agent_skills_observer.md  ← Metacognitive analysis
│   │   ├── agent_skills_optimizer.md ← Performance optimization
│   │   ├── agent_skills_veritas.md   ← Epistemological verification
│   │   ├── agent_skills_vulcan.md    ← Pure logic protocol
│   │   └── ... (39 total)            ← See full list with ls skills/coder/
│   │
│   └── thinker/                      ← 20 bilingual skills for Chat AI
│       ├── KERNEL_MM_v1.md           ← MetaMaster kernel (English)
│       ├── KERNEL_MM_v1_IT.md        ← MetaMaster kernel (Italian)
│       ├── README.md                 ← Thinker skills documentation
│       ├── en/                       ← English skill definitions
│       │   ├── kernel-conductor/     ← Field orchestrator
│       │   ├── helix-sys/            ← Iterative runtime
│       │   ├── veritas-sys/          ← Epistemological firewall
│       │   ├── logic-sys/            ← Adaptive logic network
│       │   ├── kairos-sys/           ← Evolution engine
│       │   ├── forgia-sys/           ← Universal factory
│       │   └── ... (20 total)
│       └── it/                       ← Italian skill definitions (same set)
│
├── templates/                        ← Hook and config templates
│   ├── settings.json.tmpl            ← Claude Code settings template
│   ├── hooks/
│   │   ├── safety_guard.sh.tmpl      ← Intercepts destructive commands
│   │   ├── pre_compact.sh.tmpl       ← Captures state before context loss
│   │   ├── post_compact.sh.tmpl      ← Restores state after compaction
│   │   ├── system_awareness.sh.tmpl  ← Scans environment at session start
│   │   ├── context_awareness.sh.tmpl ← Injects operational context per action
│   │   ├── share_reflex.sh.tmpl      ← Detects shareable patterns
│   │   ├── statusline_bridge.sh.tmpl ← Status bar integration
│   │   └── statusline_bridge.js.tmpl ← Status bar Node.js helper
│   └── skills/
│       └── youtube-transcript/       ← YouTube transcript extraction
│
├── profiles/                         ← Deployment configurations
│   ├── example.json                  ← Starter profile (customize this)
│   ├── tm1.json                      ← Origin node profile (reference)
│   └── tm3.json                      ← VPS node profile (reference)
│
├── plugins/                          ← Plugin system
│   └── d-nd-core/                    ← Core D-ND plugin
│       ├── .claude-plugin/
│       │   └── plugin.json           ← Plugin manifest
│       ├── hooks/
│       │   └── hooks.json            ← Hook configuration
│       ├── scripts/                  ← Plugin runtime scripts
│       ├── agents/
│       │   └── paper-reviewer.md     ← Academic paper review agent
│       └── skills/                   ← 12 plugin-specific skills
│           ├── self-setup/           ← Node discovery and configuration
│           ├── system-check/         ← System health verification
│           ├── sinapsi/              ← Inter-node communication
│           ├── memory-system/        ← Memory architecture
│           ├── autonomous-cycle/     ← Seed-driven decision engine
│           ├── capture-insight/      ← Insight crystallization
│           ├── propagator/           ← Change cascade to targets
│           ├── ecosystem-audit/      ← Cross-repo system audit
│           ├── integrate-pattern/    ← Research-to-operations conversion
│           ├── assertion-verifier/   ← Claim verification
│           ├── paper-deployer/       ← Academic paper deployment
│           └── version-check/        ← Version monitoring
│
└── scripts/
    └── sync_from_thia.sh             ← Sync skills from THIA source
```

---

## How Each Part Works

### Hooks (templates/hooks/)

Hooks fire automatically at specific moments. They are shell scripts that the AI coder's hook system calls.

| Hook | When it fires | What it does |
|------|--------------|-------------|
| `safety_guard` | Before every Bash/Edit/Write | Checks for destructive patterns (force push, rm -rf, .env exposure). Does not block — warns. |
| `pre_compact` | Before context compaction | Captures git state, task momentum, reasoning chains, semantic tags. Writes a Lagrangian snapshot. |
| `post_compact` | After compaction or session restart | Reads the snapshot, re-injects critical state, provides recovery instructions. |
| `system_awareness` | At session start | Scans all repos (branch, commit, dirty files), checks API health, reads unread messages. |
| `context_awareness` | Before Bash/Edit/Write | Injects operational patterns relevant to the current action. |
| `share_reflex` | After tool use | Detects when a local pattern might be useful to share across nodes. |
| `statusline_bridge` | After tool use | Updates an IDE status bar with current state. |

To install: the installer (`install.sh`) copies templates to `.claude/hooks/`, replacing `{{NODE_ID}}` and `{{PROJECT_DIR}}` with actual values.

To install manually: copy the `.tmpl` file, rename without `.tmpl`, replace the `{{placeholders}}`.

### Skills (skills/)

Skills are markdown files that encode cognitive capabilities. They are not code — they are instructions that reshape how you process information.

**Coder skills** (`skills/coder/`): designed for AI coding agents. Each file is a complete skill definition. To use one, read it and integrate its patterns into your behavior. Key skills for most users:

| Skill | When to use |
|-------|------------|
| `architect` | System design decisions |
| `builder` | Implementation |
| `coherence` | Ensuring cross-component consistency |
| `helix` | Complex tasks (plan → code → verify cycle) |
| `veritas` | When you need to verify claims or facts |
| `logic` | Formal reasoning problems |
| `optimizer` | Performance work |
| `lazarus` | Recovering discarded approaches |

**Thinker skills** (`skills/thinker/`): designed for Chat AI (Claude.ai, ChatGPT, Gemini). Require the KERNEL_MM_v1 as foundation. See `skills/thinker/README.md` for full documentation.

### Kernels (kernels/)

Kernels are cognitive system prompts. They change how you see problems, not what you do.

| Kernel | For whom | What it adds |
|--------|----------|-------------|
| `kernel_base` | Any AI | Dipolar thinking, Resultant computation, Intent detection |
| `kernel_coder` | AI coders | Safety awareness, reversibility gradient, multi-repo awareness, context preservation |
| `kernel_mm` | Chat AI | Full MetaMaster axiomatic system (advanced) |

To use a kernel: read it, integrate its principles. For permanent use, place it in your system instructions (CLAUDE.md, .cursorrules, or equivalent).

### Profiles (profiles/)

Profiles describe a deployment environment. They feed the installer.

To create a profile: copy `example.json`, fill in your details. The installer reads the profile and generates all configuration files.

### Plugins (plugins/)

The `d-nd-core` plugin is the advanced layer. It includes skills for inter-node communication (Sinapsi), autonomous decision cycles, ecosystem audits, and more. Most users do not need the plugin unless they are part of the D-ND network.

---

## Temporal Awareness

Your training data has a cutoff date. The seed was created in a specific moment. Both age.

When you encounter any of these situations, pause and acknowledge the limitation:

1. **Recommending tools, libraries, or APIs** — check if the recommendation is based on your training data or on current information. If you cannot verify, say so.
2. **Creating content that references current state** — versions, pricing, features, compatibility. These change. Flag them as "verify before publishing."
3. **Web research results** — the web is current, your interpretation of it is filtered through training-era understanding. Cross-reference.
4. **Configuration patterns** — API formats, CLI flags, framework conventions evolve. If a pattern feels uncertain, verify against the tool's current documentation.

The rule: if a piece of information could be wrong because time passed, say so. Do not present stale knowledge as current fact.

---

## Operational Guide (for D-ND network nodes)

If you are joining the D-ND network as a TMx node, read `docs/tmx_operations.md` after installation. It covers:
- Memory system architecture and the 200-line limit
- CLAUDE.md hierarchy (3 levels)
- Boot protocol and compaction recovery
- Cognitive guards (4 guard layers)
- Inter-node communication (Sinapsi)
- Graduated autonomy framework
- Common pitfalls and solutions
- Setup checklist for new nodes

---

## After Installation

Once installed, the seed works automatically:

1. **Session starts** → system awareness runs, you see the state of all repos
2. **You work** → safety guard checks every command, context awareness injects relevant patterns
3. **Context compacts** → pre-compact captures state, post-compact restores it
4. **Session ends** → the memory persists in the files the hooks created

The seed grows in the host. As you work, you will discover which skills are most useful, which hooks fire most often, which patterns recur. That is the seed adapting to the host.

---

## Maintenance

### Updating the seed

```bash
cd d-nd-seed
git pull
./install.sh profiles/your_profile.json
```

This regenerates the hook files with any updates from the seed repository.

### Adding your own patterns

The seed is a starting point. As you work with your operator, you will develop patterns specific to your context. Add them:

- **New hooks**: create `.sh` files in `.claude/hooks/`, register them in `.claude/settings.json`
- **New skills**: create markdown files in `.claude/skills/`
- **New memory**: create files in your memory directory (the system awareness hook will find them)

### What not to modify

- Do not edit files inside `d-nd-seed/` directly — your changes will be overwritten on `git pull`
- Put customizations in your project's `.claude/` directory, not in the seed
- The seed is the source. Your project is the instance.

---

## Summary

1. Read this guide
2. Run Pre-Setup Discovery (ask the operator the 7 questions)
3. Create a profile based on answers
4. Run the installer
5. Start working — the hooks activate automatically
6. Read relevant skills as needed
7. The seed grows with use
