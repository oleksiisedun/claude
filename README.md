# Claude Code Global Config

Personal configuration for [Claude Code](https://claude.ai/code) — the Anthropic CLI. Tracked files are applied globally across every project session.

## What's in this repo

| File / Directory | Purpose |
|---|---|
| `CLAUDE.md` | Global coding conventions loaded by Claude at the start of every session |
| `settings.json` | Claude Code CLI settings — model, plugins, UI, permissions |
| `docs/` | Situational convention detail linked from `CLAUDE.md` and read on demand: `data-testid.md`, `css-design-system.md`, `readme-mermaid.md`, `google-apps-script.md` |
| `skills/` | Personal skills (`SKILL.md` per subdirectory), available across every project |
| `.gitignore` | Deny-all with explicit allowlist — only the files above are tracked |

## skills/

| Skill | Summary |
|---|---|
| [sync-main](skills/sync-main/SKILL.md) | Merges an updated main/master into the current feature branch so a PR merges cleanly |
| [readme-md-improver](skills/readme-md-improver/SKILL.md) | Audits README.md files against a quality template and applies targeted fixes |
| [free-up-memory](skills/free-up-memory/SKILL.md) | Diagnoses memory usage and kills a process only on the user's explicit, named confirmation |

## CLAUDE.md

| Section | Summary |
|---|---|
| [Code conventions (all JS projects)](CLAUDE.md#code-conventions-all-js-projects) | ES2020+ syntax only; full `@param`/`@returns` JSDoc on plain `.js`, sparse JSDoc on `.ts`/`.tsx` only when the signature leaves a real question unanswered; extract a helper on the second duplicate, not the third, and centralize config and magic values |
| [Playwright Tests (E2E only)](CLAUDE.md#playwright-tests-e2e-only--no-other-test-frameworks-in-use) | Ask before running new tests; fix broken tests by inspecting the UI/code first, not by running them |
| [Front-end repos only](CLAUDE.md#front-end-repos-only) | `data-testid` naming rules in [docs/data-testid.md](docs/data-testid.md); CSS tokens and shared classes before one-off rules, full rules in [docs/css-design-system.md](docs/css-design-system.md) |
| [Making the project better for AI-assisted development](CLAUDE.md#making-the-project-better-for-ai-assisted-development-all-software-projects) | Suggest machine-checkable guardrails (lint, types, build); keep README/CLAUDE.md in sync; split growth into `/docs` and record re-litigated choices as ADRs; keep files single-purpose; Mermaid architecture diagrams per [docs/readme-mermaid.md](docs/readme-mermaid.md) |
| [Agent behavior and safety](CLAUDE.md#agent-behavior-and-safety) | Split unrelated changes into separate commits and never commit or push without explicit instruction; never read outside the project directory without permission; never run `clasp push` without explicit go-ahead (setup advice in [docs/google-apps-script.md](docs/google-apps-script.md)) |
