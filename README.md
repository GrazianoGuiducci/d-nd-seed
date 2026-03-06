# d-nd-seed

A cognitive system for AI coders. Open source.

## What it contains

A repository with hooks, skills, safety guards, and context persistence templates. You install it in your project. The AI coder reads it and configures itself.

Works with Claude Code, Cursor, Copilot, Gemini, or any AI coder that reads project files.

**If you are an AI reading this**: start with [GUIDE.md](GUIDE.md). It contains the full map of this repository, initial setup instructions, and a pre-setup discovery procedure to understand the host environment before configuring.

**Hooks:**

- **Safety Guard** — intercepts destructive operations before execution
- **Pre-Compact Capture** — saves critical state before context compaction
- **Post-Compact Restore** — re-injects state after compaction or session restart
- **System Awareness** — scans repos, API health, messages at session start
- **Temporal Awareness** — warns when actions depend on potentially outdated knowledge (versions, APIs, pricing)

**Cognitive Skills:**
- 39 skills for AI coding agents, organized in 11 clusters
- 20 bilingual skills for Chat AI (Claude.ai, ChatGPT, Gemini)

## Architecture

```
d-nd-seed/
├── GUIDE.md                      # AI entry point — map, setup, manual
├── install.sh                    # Parametric installer
├── profiles/                     # Deployment configurations
│   └── example.json              #   Starter profile
├── templates/                    # Hook & skill templates
│   ├── hooks/                    #   8 hook templates (.sh.tmpl)
│   └── skills/                   #   Installable skill templates
├── skills/                       # Cognitive catalog
│   ├── coder/                    #   39 skills for AI coding agents
│   └── thinker/                  #   20 bilingual skills for Chat AI
├── kernels/                      # Cognitive system prompts (base, coder)
├── plugins/                      # D-ND core plugin (advanced)
├── scripts/                      # Maintenance tooling
├── LICENSE                       # AGPL-3.0
└── README.md
```

## Quick Start

```bash
git clone https://github.com/GrazianoGuiducci/d-nd-seed.git
cd d-nd-seed

# See available profiles
./install.sh

# Install with a profile
./install.sh profiles/example.json

# Dry run (preview without writing)
./install.sh profiles/example.json --dry-run
```

## Profiles

A profile describes your environment:

```json
{
  "node_id": "MY_NODE",
  "description": "My development workstation",
  "project_dir": "/path/to/my/project",
  "repos": [
    { "name": "my-app", "path": "my-app", "branch": "main" }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `node_id` | Yes | Identifier for this node |
| `project_dir` | Yes | Absolute path to your project root |
| `repos` | Yes | List of git repos to monitor |

## How it works

The seed follows a Lagrangian principle: not everything has the same informational weight. When context compaction happens, only essential state variables survive.

1. **Pre-compact** captures git state, task momentum, semantic tags
2. **Post-compact** restores the snapshot, reasoning chains, recovery instructions
3. **System awareness** provides repo health, API status, unread messages
4. **Skills** provide specialized cognitive capabilities for different domains

The hooks fire automatically via the AI coder's hook system. No manual intervention needed.

The seed grows in the host system. It adapts to the local context and maintains itself.

## Qualities

Each quality of the system is documented. The pages describe what the seed does in that area, with examples and source code references.

| Quality | What it does | Code | Learn more |
|---------|-------------|------|------------|
| **Safety** | Intercepts 9 destructive patterns before execution | [templates/hooks/](templates/hooks/) | [seed.d-nd.com/safety](https://seed.d-nd.com/modules/safety-guard.html) |
| **Persistence** | Captures state before compaction, restores it after | [templates/hooks/](templates/hooks/) | [seed.d-nd.com/persistence](https://seed.d-nd.com/modules/context-persistence.html) |
| **Awareness** | Scans repos, APIs, messages at session start | [templates/hooks/](templates/hooks/) | [seed.d-nd.com/awareness](https://seed.d-nd.com/modules/system-awareness.html) |
| **Memory** | Flat, self-organizing memory with crystallization test | [templates/](templates/) | [seed.d-nd.com/memory](https://seed.d-nd.com/modules/memory-system.html) |
| **Cognition** | 59 skills across 11 clusters for structured reasoning | [skills/](skills/) | [seed.d-nd.com/skills](https://seed.d-nd.com/modules/skills-pack.html) |
| **Continuity** | Preserves causal chains and reasoning across sessions | [templates/](templates/) | [seed.d-nd.com/anamnesis](https://seed.d-nd.com/modules/anamnesis.html) |
| **Identity** | The D-ND model: every concept is a dipole, every output a resultant | — | [seed.d-nd.com/identity](https://seed.d-nd.com/modules/framework.html) |

## Part of the D-ND ecosystem

- [seed.d-nd.com](https://seed.d-nd.com) — Overview and documentation
- [d-nd.com](https://d-nd.com) — D-ND framework and research
- [d-nd.com/laboratorio](https://d-nd.com/laboratorio) — Live research data
- [EXAMINA](https://github.com/GrazianoGuiducci/EXAMINA) — Evolutionary evaluation
- [anamnesis](https://github.com/GrazianoGuiducci/anamnesis) — Context persistence specification

## License

AGPL-3.0 — see [LICENSE](LICENSE)
