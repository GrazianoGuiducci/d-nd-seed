# d-nd-seed

The DNA of cognitive AI coding environments. A single repo that contains everything needed to transform a generic AI coder into a D-ND aware system.

## What it does

AI coders forget context, lose state between sessions, and let dangerous commands slip through. This seed installs a complete cognitive layer:

**Infrastructure (hooks):**
- **Safety Guard** — warns before destructive operations (force push, rm -rf, .env edits)
- **Pre-Compact Capture** — saves critical state before context compaction
- **Post-Compact Restore** — re-injects state when a new session starts
- **System Awareness** — scans repos, API health, messages on every session start

**Cognitive Skills (coder):**
- 37 specialized skills for AI coding agents (architecture, testing, deployment, memory, observability...)
- Organized by the D-ND 3-plane taxonomy: Cognitive (P1), Operative (P2), Systemic (P3)

**Cognitive Skills (thinker):**
- 18 bilingual skills for Chat AI (Claude.ai, ChatGPT, Gemini)
- Kernel MM (Meta-Model) — the cognitive core for chat interactions
- Pack builder script for easy deployment

## Architecture

```
d-nd-seed/
├── install.sh                    # Parametric installer
├── profiles/                     # Deployment configurations
│   ├── example.json              #   Minimal starter
│   ├── tm1.json                  #   Origin Node (reference)
│   └── tm3.json                  #   Dev Node (reference)
├── templates/                    # Hook & skill templates
│   ├── hooks/                    #   4 hook templates (.sh.tmpl)
│   └── skills/                   #   Installable skill templates
├── skills/                       # Full cognitive catalog
│   ├── coder/                    #   37 skills for AI coding agents
│   └── thinker/                  #   18 bilingual skills for Chat AI
├── scripts/                      # Maintenance tooling
│   └── sync_from_thia.sh         #   Sync skills from THIA source
├── LICENSE                       # AGPL-3.0
└── README.md
```

## Base vs Premium

### Base (free, open source)

Everything you need to work safely:

| Component | What it does |
|-----------|-------------|
| `install.sh` + `profiles/` | Generate `.claude/` config for your environment |
| `templates/hooks/safety_guard` | Prevent destructive operations |
| `templates/hooks/system_awareness` | Environment scan at session start |
| `skills/coder/agent_skills_conductor.md` | Skill routing (demo) |
| `skills/coder/agent_skills_field-awareness.md` | D-ND awareness (demo) |
| `skills/coder/agent_skills_coherence.md` | Consistency checking (demo) |

### Premium (subscription)

The full cognitive catalog + evolution:

| Component | What it does |
|-----------|-------------|
| `templates/hooks/pre_compact` | Lagrangian state capture before compaction |
| `templates/hooks/post_compact` | State restoration after compaction |
| `skills/coder/*` (37 skills) | Full cognitive skill catalog for AI coders |
| `skills/thinker/*` (18 skills) | Bilingual skills for Chat AI |
| `skills/thinker/KERNEL_MM_v1.md` | Meta-Model cognitive kernel |
| Evolution updates | Continuous improvements from THIA R&D |

Premium = access to this private repo. `git pull` to evolve.

## Quick Start

```bash
# Clone (requires access)
git clone https://github.com/moodnd/d-nd-seed.git
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
| `node_id` | Yes | Unique identifier for this node |
| `project_dir` | Yes | Absolute path to your project root |
| `thia_path` | No | Path to THIA (enables advanced skills) |
| `vps_url` | No | API endpoint for health checks |
| `sinapsi_for` | No | Node ID for inter-node messaging |
| `repos` | Yes | List of git repos to monitor |

## How it works

The seed follows a **Lagrangian principle**: not everything has the same informational weight. When context compaction happens, only essential state variables survive:

1. **Pre-compact** captures: git state, task momentum, field position, semantic tags
2. **Post-compact** restores: the snapshot, reasoning chains, recovery instructions
3. **System awareness** provides: repo health, API status, unread messages
4. **Skills** provide: specialized cognitive capabilities for different domains

The hooks fire automatically via Claude Code's hook system. No manual intervention needed.

## Propagation cycle

```
THIA (R&D) → export-to-seed (neutralize) → d-nd-seed (commit) → client (git pull)
```

Every improvement to THIA becomes a new capability for subscribers. You don't pay for access — you subscribe to evolution.

## Part of the D-ND ecosystem

This seed is the distribution channel of the [D-ND framework](https://d-nd.com) — a cognitive model for AI systems.

- [seed.d-nd.com](https://seed.d-nd.com) — Public landing, free base download
- [d-nd.com](https://d-nd.com) — Framework overview
- [MM_D-ND](https://github.com/moodnd/MM_D-ND) — Mathematical framework (9 axioms)
- [EXAMINA](https://github.com/moodnd/EXAMINA) — Evolutionary evaluation
- [anamnesis](https://github.com/moodnd/anamnesis) — Context persistence spec

## License

AGPL-3.0 — see [LICENSE](LICENSE)
