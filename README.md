# Claude Code Global Config

Personal configuration for [Claude Code](https://claude.ai/code) — the Anthropic CLI. Tracked files are applied globally across every project session.

## What's in this repo

| File / Directory | Purpose |
|---|---|
| `CLAUDE.md` | Global coding conventions loaded by Claude at the start of every session |
| `settings.json` | Claude Code CLI settings — model, plugins, UI, permissions |
| `statusline-command.sh` | Status line script — model, effort level, session (5h) usage bar, context usage bar |
| `docs/` | Situational convention detail linked from `CLAUDE.md` and read on demand: `javascript.md`, `python.md`, `shell.md`, `data-testid.md`, `playwright-tests.md`, `css-design-system.md`, `readme-mermaid.md`, `google-apps-script.md` |
| `skills/` | Personal skills (`SKILL.md` per subdirectory), available across every project |
| `.gitignore` | Deny-all with explicit allowlist — only the files above are tracked |

## skills/

| Skill | Summary |
|---|---|
| [sync-main](skills/sync-main/SKILL.md) | Merges an updated main/master into the current feature branch so a PR merges cleanly |
| [readme-md-improver](skills/readme-md-improver/SKILL.md) | Audits README.md files against a quality template and applies targeted fixes |
| [project-improver](skills/project-improver/SKILL.md) | Audits the whole current project against the global `CLAUDE.md` (read fresh at run time), reports graded findings by section, and applies only approved fixes |
| [free-up-memory](skills/free-up-memory/SKILL.md) | Diagnoses memory usage and kills a process only on the user's explicit, named confirmation |
| [setup-vscode-locked-group-fix](skills/setup-vscode-locked-group-fix/SKILL.md) | One-time setup: merges a user-level VS Code task into `tasks.json` that unlocks and joins editor groups on folder open, working around the empty locked group on startup |

## CLAUDE.md

| Section | Summary |
|---|---|
| [Language conventions](CLAUDE.md#language-conventions) | Read-before-editing pointers: [docs/javascript.md](docs/javascript.md) (ES2020+ only; full `@param`/`@returns` JSDoc on plain `.js`, sparse on `.ts`/`.tsx`), [docs/python.md](docs/python.md) (uv, ruff, type hints, docstring only when non-obvious), [docs/shell.md](docs/shell.md) (bash strict mode, quoting, shellcheck/shfmt) |
| [Code duplication (all software projects)](CLAUDE.md#code-duplication-all-software-projects) | Extract a helper on the second duplicate, not the third; centralize config and magic values; prefer a clear duplicate over a confusing abstraction |
| [Playwright Tests (E2E only)](CLAUDE.md#playwright-tests-e2e-only--no-other-test-frameworks-in-use) | Ask before running new tests; fix broken tests by inspecting the UI/code first, not by running them; full rules in [docs/playwright-tests.md](docs/playwright-tests.md) |
| [Front-end repos only](CLAUDE.md#front-end-repos-only) | `data-testid` naming rules in [docs/data-testid.md](docs/data-testid.md); CSS tokens and shared classes before one-off rules, full rules in [docs/css-design-system.md](docs/css-design-system.md) |
| [Making the project better for AI-assisted development](CLAUDE.md#making-the-project-better-for-ai-assisted-development-all-software-projects) | Suggest machine-checkable guardrails (lint, types, build); keep README/CLAUDE.md in sync; split growth into `/docs` and record re-litigated choices as ADRs; keep files single-purpose; Mermaid architecture diagrams per [docs/readme-mermaid.md](docs/readme-mermaid.md) |
| [Agent behavior and safety](CLAUDE.md#agent-behavior-and-safety) | Split unrelated changes into separate commits and never commit or push without explicit instruction; never read outside the project directory without permission; never run `clasp push` without explicit go-ahead (setup advice in [docs/google-apps-script.md](docs/google-apps-script.md)) |
