# d-nd-seed

A cognitive system for AI coders. Open source.

## What it contains

A repository with hooks, skills, safety guards, and context persistence templates. You install it in your project. The AI coder reads it and configures itself.

Works with Claude Code, Cursor, Copilot, Gemini, or any AI coder that reads project files.

**Hooks:**
- **Safety Guard** — intercepts destructive operations before execution
- **Pre-Compact Capture** — saves critical state before context compaction
- **Post-Compact Restore** — re-injects state after compaction or session restart
- **System Awareness** — scans repos, API health, messages at session start

**Cognitive Skills:**
- 38 skills for AI coding agents, organized by the D-ND 3-plane taxonomy
- 18 bilingual skills for Chat AI (Claude.ai, ChatGPT, Gemini)

## Architecture

```
d-nd-seed/
├── install.sh                    # Parametric installer
├── profiles/                     # Deployment configurations
│   └── example.json              #   Starter profile
├── templates/                    # Hook & skill templates
│   ├── hooks/                    #   4 hook templates (.sh.tmpl)
│   └── skills/                   #   Installable skill templates
├── skills/                       # Cognitive catalog
│   ├── coder/                    #   38 skills for AI coding agents
│   └── thinker/                  #   18 bilingual skills for Chat AI
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

## Part of the D-ND ecosystem

- [seed.d-nd.com](https://seed.d-nd.com) — Overview and documentation
- [d-nd.com](https://d-nd.com) — D-ND framework
- [MM_D-ND](https://github.com/GrazianoGuiducci/MM_D-ND) — Mathematical framework (9 axioms)
- [EXAMINA](https://github.com/GrazianoGuiducci/EXAMINA) — Evolutionary evaluation
- [anamnesis](https://github.com/GrazianoGuiducci/anamnesis) — Context persistence specification

## License

AGPL-3.0 — see [LICENSE](LICENSE)
