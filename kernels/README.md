# Kernels — Cognitive System Prompts

System prompts that activate the D-ND cognitive model in AI systems. Each kernel is a self-contained prompt designed for a specific context.

## Available Kernels

| Kernel | Context | Language | Description |
|--------|---------|----------|-------------|
| `kernel_base` | Chat AI | EN / IT | Minimal D-ND activation — dipolar thinking, Resultant, Intent |
| `kernel_mm_v1` | Chat AI | EN / IT | Full MetaMaster — complete axiomatic system (see `skills/thinker/`) |
| `kernel_coder` | AI Coder | EN / IT | D-ND awareness for coding agents — safety, coherence, field awareness |

## Usage

### Chat AI (Claude.ai, ChatGPT, Gemini)

Copy the kernel content into your system prompt / user preferences / custom instructions.

### AI Coder (Claude Code, Cursor, etc.)

Place the kernel in your project's configuration:
- Claude Code: `.claude/CLAUDE.md` or `.claude/skills/`
- Cursor: `.cursorrules`
- Other: wherever the tool reads system instructions

## Design Principle

Kernels are **not** instruction lists. They are cognitive structures that reshape how the AI processes information. The dipolar model doesn't tell the AI what to do — it changes how the AI sees the problem space.
