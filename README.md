# Claude Code Global Config

Personal configuration for [Claude Code](https://claude.ai/code) — the Anthropic CLI. Tracked files are applied globally across every project session.

## What's in this repo

| File / Directory | Purpose |
|---|---|
| `CLAUDE.md` | Global coding conventions loaded by Claude at the start of every session |
| `settings.json` | Claude Code CLI settings — model, plugins, UI, permissions |
| `.gitignore` | Deny-all with explicit allowlist — only the files above are tracked |

## CLAUDE.md

| Section | Summary |
|---|---|
| [Code conventions (all JS projects)](CLAUDE.md#code-conventions-all-js-projects) | ES2020+ syntax only; full `@param`/`@returns` JSDoc on plain `.js`, sparse JSDoc on `.ts`/`.tsx` only when the signature leaves a real question unanswered |
| [Playwright Tests (E2E only)](CLAUDE.md#playwright-tests-e2e-only--no-other-test-frameworks-in-use) | Ask before running new tests; fix broken tests by inspecting the UI/code first, not by running them |
| [data-testid (front-end repos only)](CLAUDE.md#data-testid-front-end-repos-only) | Naming/structure rules live in [docs/data-testid.md](docs/data-testid.md) |
| [CSS design system (front-end repos only)](CLAUDE.md#css-design-system-front-end-repos-only) | Define `:root` tokens and shared classes (`.btn-primary`, `.overlay`) before writing one-off component rules |
| [Code duplication (all software projects)](CLAUDE.md#code-duplication-all-software-projects) | Extract a helper on the second duplicate, not the third; centralize config and magic values |
| [README conventions (all software projects)](CLAUDE.md#readme-conventions-all-software-projects) | New/rewritten Architecture sections get a Mermaid diagram, not just prose |
| [After edits (all software projects)](CLAUDE.md#after-edits-all-software-projects) | Keep README/CLAUDE.md in sync with real changes; split growth into `/docs` |
| [Git Commits](CLAUDE.md#git-commits) | Split unrelated changes into separate commits; never commit or push without explicit instruction |
| [Google Apps Script (clasp) projects](CLAUDE.md#google-apps-script-clasp-projects) | Never run `clasp push` without explicit go-ahead, even though editing code is fine |
| [Working directory boundaries (all projects)](CLAUDE.md#working-directory-boundaries-all-projects) | Never read/search outside the current project's directory without explicit permission |
