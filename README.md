# d-nd-seed

Configuration seed for AI coding environments. Generates `.claude/` directory with hooks, skills, and awareness infrastructure from a profile.

## What it does

When you work with Claude Code (or similar AI coding tools), sessions get compacted, context gets lost, dangerous commands slip through. This seed installs a safety and awareness layer:

- **Safety Guard** — warns before destructive operations (force push, rm -rf, .env edits)
- **Pre-Compact Capture** — saves critical state (git state, task momentum, field position) before context compaction
- **Post-Compact Restore** — re-injects the saved state when a new session starts after compaction
- **System Awareness** — scans all repos, API health, messages on every session start
- **Skills** — reusable capabilities (YouTube transcript extraction, etc.)

## Quick Start

```bash
# Clone
git clone https://github.com/moodnd/d-nd-seed.git
cd d-nd-seed

# See available profiles
./install.sh

# Install with a profile
./install.sh profiles/example.json

# Dry run (see what would be generated without writing)
./install.sh profiles/example.json --dry-run
```

## Profiles

A profile is a JSON file that describes your environment:

```json
{
  "node_id": "MY_NODE",
  "description": "My development workstation",
  "project_dir": "/path/to/my/project",
  "thia_path": "",
  "vps_url": "",
  "sinapsi_for": "",
  "repos": [
    { "name": "my-app", "path": "my-app", "branch": "main" }
  ]
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `node_id` | Yes | Unique identifier for this node |
| `project_dir` | Yes | Absolute path to your project root |
| `thia_path` | No | Path to THIA (enables YouTube transcript skill) |
| `vps_url` | No | API endpoint for health checks |
| `sinapsi_for` | No | Node ID for inter-node messaging |
| `repos` | Yes | List of git repos to monitor |

## What gets generated

```
your-project/.claude/
├── settings.json              # Hook wiring (auto-generated)
├── settings.local.json        # Permissions (NOT overwritten if exists)
├── hooks/
│   ├── safety_guard.sh        # PreToolUse — danger detection
│   ├── pre_compact.sh         # PreCompact — state capture
│   ├── post_compact.sh        # SessionStart:compact — state restore
│   └── system_awareness.sh    # SessionStart — environment scan
└── skills/
    └── youtube-transcript/
        └── SKILL.md           # YouTube extraction (if thia_path set)
```

**`settings.local.json` is never overwritten** — your permissions are yours.

## Requirements

- `bash`
- `node` (for JSON parsing in installer and hooks)
- `git` (for repo scanning in hooks)

## How it works

The seed follows a Lagrangian principle: not everything has the same informational weight. When context compaction happens, only the essential state variables survive — the "Lagrangian coordinates" of your work:

1. **Pre-compact** captures: git state, task momentum, field position, semantic tags
2. **Post-compact** restores: the snapshot, reasoning chains, recovery instructions
3. **System awareness** provides: repo health, API status, unread messages

The hooks fire automatically via Claude Code's hook system. No manual intervention needed.

## Part of the D-ND ecosystem

This seed is a module of the [D-ND framework](https://d-nd.com) — a cognitive model for AI systems based on the Included Middle principle.

Other modules:
- [MM_D-ND](https://github.com/moodnd/MM_D-ND) — Mathematical framework
- [EXAMINA](https://github.com/moodnd/EXAMINA) — Evolutionary exam system
- [anamnesis](https://github.com/moodnd/anamnesis) — Context persistence spec
- [skill](https://github.com/moodnd/skill) — Cognitive skills pack

## License

AGPL-3.0 — see [LICENSE](LICENSE)
