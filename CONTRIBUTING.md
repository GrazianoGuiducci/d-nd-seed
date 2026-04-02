# Contributing to d-nd-seed

The seed grows through use. If you install it and something breaks, doesn't work as expected, or could work better — that's a contribution waiting to happen.

## How to contribute

**Report what you find.** Open an issue describing what happened, what you expected, and what environment you're using (Claude Code, Cursor, Copilot, etc.). The more specific, the better.

**Propose improvements.** If you have a fix or a new skill/hook, open a PR. Include:
- What it does and why
- Which AI coders you tested it with
- Eval tests (trigger + fidelity) if it's a hook or skill

**Share your profile.** If you created a profile for your environment that others might use, submit it to `profiles/`.

## Structure

- `templates/hooks/` — Hook templates. Parametric (use `{{PLACEHOLDERS}}`). Each must have an `## Eval` section.
- `skills/coder/` — Skills for AI coding agents. Markdown files with YAML frontmatter.
- `skills/thinker/` — Skills for chat AI. Bilingual (IT/EN).
- `plugins/` — Self-contained modules (d-nd-core, godel).
- `docs/` — Operational guides.

## Conventions

- Hooks use `.sh.tmpl` extension with `{{ENV_VAR}}` placeholders
- Skills use YAML frontmatter (`name`, `description`, `user-invocable`)
- Every hook and skill carries its own eval tests
- Code comments in English, docs in English (skills may be bilingual)
- Commits: `feat:`, `fix:`, `docs:`, `chore:`

## License

By contributing, you agree that your contributions will be licensed under AGPL-3.0.
