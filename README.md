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
| No structure for complex decisions | 103 skills for reasoning, evaluation, self-improvement |
| You remind it of project conventions | CLAUDE.md + hooks enforce them automatically |

## Quick start

```bash
git clone https://github.com/GrazianoGuiducci/d-nd-seed.git
cd d-nd-seed

# Preview what will be generated
./install.sh profiles/example.json --dry-run

# Install
./install.sh profiles/example.json
```

The installer reads your profile, adapts the templates, writes the configuration. Three files minimum: `CLAUDE.md` (identity), `settings.json` (hooks), `MEMORY.md` (persistent memory). Everything else is optional.

## What is inside

**17 hook templates** that fire automatically:

| Hook | When | What it does |
|------|------|-------------|
| Safety Guard | Before every edit/command | Catches destructive operations before they execute |
| System Awareness | Session start | Scans repos, git state, API health, unread messages |
| Session Monitor | Every tool call | Tracks boot compliance, guards memory writes, periodic reminders |
| Pre/Post Compact | Context compaction | Captures essential state before, restores it after |
| Cascade Check | After modifications | Asks: who else in the system needs to know? |
| Skill Health | Session start | Verifies skills have tests and triggers don't overlap |

Each hook carries its own eval tests. You can verify they work.

**103 skills** across three categories:

| Category | Count | For |
|----------|-------|-----|
| Plugin skills | 17 | eval, dream, auto-learn, CEC, propagation, self-setup |
| Coder skills | 42 | Architecture, testing, debugging, deployment, review |
| Thinker skills | 44 | Reasoning, analysis, strategy (bilingual IT/EN, for Chat AI) |

**Cognitive kernels** — system prompts that shape how the AI thinks:

- `kernel_base` — observe, relate, emerge, integrate
- `kernel_coder` — safety, reversibility, multi-repo awareness, verification before assertion

**Godel plugin** — an inverted oracle. It does not answer questions. It inverts assumptions. You give it a tension, it shows you what you were hiding. Pre-built configurations for sales, research, finance.

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
│   ├── hooks/            # 17 hook templates (.sh.tmpl, parametric)
│   └── skills/           # Installable skill templates
├── skills/
│   ├── coder/            # 42 skills for coding agents
│   └── thinker/          # 44 bilingual skills for chat AI
├── kernels/              # Cognitive system prompts (base, coder)
├── plugins/
│   ├── d-nd-core/        # Core: safety, awareness, inter-node messaging
│   └── godel/            # Inverted oracle with domain configurations
├── docs/                 # 13 operational guides
└── scripts/              # Maintenance tools
```

## How the system works at maturity

The seed installs the structure. What grows from it is described in [OPERATIONAL_MATURITY.md](docs/OPERATIONAL_MATURITY.md) — how the system thinks, protects itself, and evolves after installation. Seven patterns that transfer across any node.

## For AI in a chat session

If you are using Claude.ai, ChatGPT, or Gemini (not a coding agent): start with [CHAT_START.md](CHAT_START.md). It contains the skills and instructions adapted for conversation.

## Part of D-ND

D-ND (Dual-Non-Dual) is the framework behind this seed. The mathematical model, the research, and the tools live at [d-nd.com](https://d-nd.com).

- [seed.d-nd.com](https://seed.d-nd.com) — Seed documentation
- [d-nd.com](https://d-nd.com) — Framework and research
- [d-nd.com/laboratorio](https://d-nd.com/laboratorio) — Live research data
- [EXAMINA](https://github.com/GrazianoGuiducci/EXAMINA) — Evolutionary evaluation
- [anamnesis](https://github.com/GrazianoGuiducci/anamnesis) — Context persistence specification

## License

AGPL-3.0 — see [LICENSE](LICENSE)
