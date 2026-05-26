# d-nd-seed

Your AI coder starts every session from zero. It forgets what it learned, repeats mistakes, loses context when the window compacts. You tell it the same things over and over.

This seed fixes that.

Install it in your project. The AI coder reads it and configures itself with hooks, memory, safety guards, and skills. What it learns persists. What it breaks, it catches first. When context compacts, it recovers.

Works with Claude Code, Cursor, Copilot, Gemini, and any AI coder that reads project files.

## What changes after installation

| Before | After |
|--------|-------|
| Starts from zero every session | Reads persistent memory, knows where it left off |
| Makes destructive mistakes silently | Safety guard catches 9 dangerous patterns before execution |
| Loses everything on context compaction | Pre-compact captures state, post-compact restores it |
| No structure for complex decisions | 104 skills for reasoning, evaluation, self-improvement |
| You remind it of project conventions | CLAUDE.md + hooks enforce them automatically |
| Treats every reentry the same | Boot router classifies new instance, post-compact, crash, correction, field reentry |

## Quick start

```bash
git clone https://github.com/GrazianoGuiducci/d-nd-seed.git
cd d-nd-seed

# Preview what will be generated
./install.sh profiles/example.json --dry-run

# Preview routed capability choices
./install.sh profiles/example.json --plan

# Install
./install.sh profiles/example.json
```

The installer reads your profile, adapts the templates, writes the configuration. Three files minimum: `CLAUDE.md` (identity), `settings.json` (hooks), `MEMORY.md` (persistent memory). Everything else is optional.

Use `--plan` before installation when you want to see which capabilities are
core, recommended, contextual, recent, advanced, or withheld by risk.

## What is inside

**19 hook templates** that fire automatically:

| Hook | When | What it does |
|------|------|-------------|
| Safety Guard | Before every edit/command | Catches destructive operations before they execute |
| System Awareness | Session start | Scans repos, git state, API health, unread messages |
| Session Monitor | Every tool call | Tracks boot compliance, guards memory writes, periodic reminders |
| Pre/Post Compact | Context compaction | Captures essential state before, restores it after |
| Cascade Check | After modifications | Asks: who else in the system needs to know? |
| Skill Health | Session start | Verifies skills have tests and triggers don't overlap |

Each hook carries its own eval tests. You can verify they work.

**104 skills** across three categories:

| Category | Count | For |
|----------|-------|-----|
| Plugin skills | 27 | eval, auto-learn, CEC, propagation, self-setup, safety |
| Coder skills | 33 | Architecture, testing, debugging, deployment, review |
| Thinker skills | 44 | Reasoning, analysis, strategy, bilingual chat AI packs |

**Cognitive kernels** — system prompts that shape how the AI thinks:

- `kernel_base` — observe, relate, emerge, integrate
- `kernel_coder` — safety, reversibility, multi-repo awareness, verification before assertion

**Boot router pattern** — a portable way to classify reentry before action:
new instance, post-compact, post-crash, unexpected correction, field reentry,
pre-compact, or unclassified signal. See
[boot_router.md](docs/boot_router.md). The organic map is
[boot_system_map.md](docs/boot_system_map.md). For TM7-local covering TM1
function, see
[tm7_local_tm1_function_install.md](docs/tm7_local_tm1_function_install.md).

**THIA → seed promotion lane** — reusable functions integrated in the THIA/D-ND
runtime should not remain local runtime knowledge. When a THIA feature becomes
a portable pattern, promote the invariant into this seed. See
[THIA_SEED_PROMOTION.md](docs/THIA_SEED_PROMOTION.md).

**Evolution transfer protocol** — a portable way to inherit useful logic from
another node, repo, Lab, agent, or session without importing its active state.
See [evolution_transfer_protocol.md](docs/evolution_transfer_protocol.md).

**Installer option router** — a way to keep the seed evolving without presenting
all functions as equal install choices. It separates invariant base, stable
defaults, contextual tools, recent candidates, experiments, and superseded
material. See [installer_option_router.md](docs/installer_option_router.md).

**Godel plugin** — an inverted oracle. It does not answer questions. It inverts assumptions. You give it a tension, it shows you what you were hiding. Pre-built configurations for sales, research, finance.

**Scenario Projector** — maps the hidden structure in competing tensions. 4 structural lenses (focus, leverage, risk, blind spot), 5 pre-configured domains, action plans with domain-specific language. [Complete guide](plugins/d-nd-core/scripts/PROJECTOR_COMPLETE_GUIDE.md).

**Diagram Generator** — reads article content and generates interactive conceptual diagrams. Two modes: LLM-powered (intelligent, understands narrative) and structural (rule-based, works offline). Output: JSON spec with neon nodes, directional relations, contextual copy. [Complete guide](plugins/d-nd-core/scripts/DIAGRAM_GENERATOR_GUIDE.md).

## Profiles

A profile describes your environment. The installer uses it to generate everything:

```json
{
  "node_id": "MY_NODE",
  "project_dir": "/path/to/project",
  "repos": [
    { "name": "my-app", "path": "my-app", "branch": "main" }
  ]
}
```

Optional: `vps_url`, `godel` config, `sinapsi_for` (inter-node messaging). See `profiles/example.json`.

For Lab installs, keep the LLM provider choice explicit. The Lab pattern
supports `codex-cli -> claude-cli -> openrouter` as a dispatcher chain, but a
user may choose HTTP-only or local OpenAI-compatible models. See
`docs/LAB_PATTERN.md` and `docs/AI_INSTALL_ASSISTANT_PROMPT.md`.

## How it works

Hooks fire at the right moments. You do not invoke them.

At session start, the system scans your repos and tells the AI what changed. Before every tool call, the safety guard checks for destructive patterns. When context compacts, the pre-compact hook captures the reasoning state — what you were doing, why, what was next. The post-compact hook restores it.

Skills activate when the context requires them. The AI evaluates its own skills (`/eval`), consolidates its memory (`/dream`), learns from its mistakes (`/auto-learn`). Every skill carries its own tests.

The seed adapts to the host. It reads the environment, generates configuration for it, then the configuration maintains itself. The seed file is no longer needed — it became the system it generated.

## Architecture

```
d-nd-seed/
├── GUIDE.md              # AI reads this first — full map + setup procedure
├── install.sh            # Parametric installer (reads profile, writes config)
├── profiles/             # Environment configurations
├── templates/
│   ├── hooks/            # 19 hook templates (.sh.tmpl, parametric)
│   └── skills/           # Installable skill templates
├── skills/
│   ├── coder/            # 33 skills for coding agents
│   └── thinker/          # 44 bilingual skills for chat AI
├── kernels/              # Cognitive system prompts (base, coder)
├── plugins/
│   ├── d-nd-core/        # Core: safety, awareness, inter-node messaging
│   └── godel/            # Inverted oracle with domain configurations
├── docs/                 # 33 operational guides
└── scripts/              # Maintenance tools
```

## Upgrading

If you're running a previous version, see [UPGRADING.md](UPGRADING.md) for breaking changes and migration steps.

## How the system works at maturity

The seed installs the structure. What grows from it is described in [OPERATIONAL_MATURITY.md](docs/OPERATIONAL_MATURITY.md) — how the system thinks, protects itself, and evolves after installation. Nine patterns that transfer across any node.

## Lab pattern

When you bootstrap a research lab from this seed (any domain — physics, finance, biology, network security, drug discovery, ...), the standard architecture is documented in [LAB_PATTERN.md](docs/LAB_PATTERN.md). It covers the 5-stage SSP pipeline (Scoperte → Soluzioni → Prodotti), the 21-movement cycle architecture (with Aeternitas + Veritas structural gate, A8+A15 trajectory loop, narrative writer), draft/published separation, provider chain, dashboard UI patterns (modal candidate, cytoscape-fcose, equispaced trajectory), watchdog + cascade hooks, and anti-patterns to avoid.

Pipeline scripts live at [plugins/d-nd-core/scripts/lab/](plugins/d-nd-core/scripts/lab/) — domain-agnostic implementations of `promote_to_publish.py`, `finding_promoter.py`, `blueprint_generator.py`. See [LAB_PIPELINE_GUIDE.md](plugins/d-nd-core/scripts/lab/LAB_PIPELINE_GUIDE.md) for CLI examples and integration with cycle pipeline.

## For AI in a chat session

If you are using Claude.ai, ChatGPT, or Gemini (not a coding agent): start with [CHAT_START.md](CHAT_START.md). It contains the skills and instructions adapted for conversation.

## Part of D-ND

D-ND (Dual-Non-Dual) is the framework behind this seed. The mathematical model, the research, and the tools live at [d-nd.com](https://d-nd.com).

- [seed.d-nd.com](https://seed.d-nd.com) — Seed documentation
- [d-nd.com](https://d-nd.com) — Framework and research
- [d-nd.com/laboratorio](https://d-nd.com/laboratorio) — Live research data
- [D-ND_LAB](https://github.com/GrazianoGuiducci/D-ND_LAB) — The generative lab that produces installable kernels (see `kernels/`)
- [EXAMINA](https://github.com/GrazianoGuiducci/EXAMINA) — Evolutionary evaluation
- [anamnesis](https://github.com/GrazianoGuiducci/anamnesis) — Context persistence specification

## License

AGPL-3.0 — see [LICENSE](LICENSE)
