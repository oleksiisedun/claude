---
name: project-improver
description: Review a whole project against the user's global CLAUDE.md conventions and report gaps, then apply approved fixes. Use when the user asks to review, audit, or improve a project or repo as a whole, check it against their conventions, or make it better for AI-assisted development. Not for reviewing a diff (use code-review) or for README/CLAUDE.md-only audits (use readme-md-improver / claude-md-management:claude-md-improver).
tools: Read, Glob, Grep, Bash, Edit, Write
---

# Project Improver

Audit the **current project** against the user's global `~/.claude/CLAUDE.md` and report where it falls short. The global CLAUDE.md is the single source of truth — this skill only says *how to audit*, never restates the rules. That keeps it correct when the rules change.

**Read-only until the user approves.** Produce the report first; change nothing before the user picks what to apply.

## Hard limits (from the global CLAUDE.md — they apply to this skill)

- Audit only the current working directory. Never read other projects on disk, even for inspiration.
- Never commit or push. Never run deploy/publish commands (`clasp push`, `npm publish`, etc.).
- Never install tooling, hooks, CI config, a test framework, or a new file *unprompted* — these are **suggestions in the report**; they are applied only when the user approves that specific item.
- Never run Playwright tests without asking first (see `docs/playwright-tests.md`).

## Workflow

### Phase 1: Orient

Establish the facts the audit depends on, with `ls`, `git ls-files | head`, and the manifest files (`package.json`, `pyproject.toml`, `Makefile`, `appsscript.json`, ...):

- Languages present (`.js`/`.ts`/`.tsx`, `.py`, `.sh`) — decides which language docs apply.
- Front-end project? Uses `data-testid`? Has stylesheets? Uses Playwright? Is a clasp project?
- Existing check commands (lint, typecheck, format, build, test) and whether an aggregate one exists.
- Existing `README.md`, `CLAUDE.md`, `docs/`, `docs/decisions/`, CI config, pre-commit hooks.
- File sizes: `git ls-files | xargs wc -l | sort -rn | head -20` to spot scoping candidates.

If the repo is large, sample by module instead of reading everything; say what you sampled.

### Phase 2: Load the rules

1. Read `~/.claude/CLAUDE.md` **fresh** — do not rely on the copy in context.
2. Read only the linked docs that Phase 1 shows are relevant (e.g. `docs/javascript.md` only if JS/TS exists; `docs/data-testid.md` only if the project uses `data-testid`). Docs live next to that CLAUDE.md in `~/.claude/docs/`. Always read `docs/unit-tests.md`.

### Phase 3: Audit

Walk the CLAUDE.md **section by section**, in order, skipping sections that don't apply (say which were skipped and why). For each applicable section, check the project against what that section and its linked doc actually say. Guidance on *how* to check, per section:

| CLAUDE.md section | How to check |
|---|---|
| Language conventions | Grep for violations of the language doc's rules (e.g. legacy syntax, missing JSDoc/type hints, unquoted shell vars). Run the doc's linter/formatter in check mode if the project has it configured. |
| Code duplication | Look for repeated blocks, regexes, constants, and type definitions across files (`grep` for repeated literals; skim sibling modules). Flag each pattern that appears **twice**, with both locations. |
| Unit tests | Is there a test setup? Do tests live where the language doc says? Run the existing test command. Name untested functions where a test would catch a real bug (per `docs/unit-tests.md`). No setup → suggest one, don't add it. |
| Playwright / data-testid / CSS design system | Only if applicable. Compare against the doc: naming, `:root` tokens, shared classes, one broad rule per interaction state, duplicate rules. |
| Machine-checkable guardrails | Inventory existing checks; list which of lint / typecheck / format check / build / boundary check are missing, and for each the specific mistake it would catch. Is there one aggregate entry point? Are commands documented in CLAUDE.md? Wired into pre-commit or CI? |
| CLAUDE.md and README currency | Do commands, paths, and described structure match the repo now? Missing CLAUDE.md/README → suggest. Architecture section lacking a Mermaid diagram (checked against `docs/readme-mermaid.md`) → suggest. For a deep pass, hand off to `readme-md-improver` / `claude-md-management:claude-md-improver`. |
| Docs, splitting and ADRs | Oversized CLAUDE.md/README sections that should move to `docs/`; `@import` vs plain link used correctly; design choices that look wrong-but-intentional and deserve an ADR. |
| Scoped files | Files past ~300-400 lines **and** with more than one responsibility. Length alone is not a finding — cohesive long files are fine. |
| Agent behavior and safety | Mostly rules for how *you* behave; check the project side only where relevant (e.g. clasp project layout per `docs/google-apps-script.md`). |

Run existing, fast, read-only checks (lint, typecheck, tests) to ground findings in real output — but not builds or scripts with side effects. Verify every claim against the repo (`grep`, `ls`, tool `--help`); don't report from assumption. Drop findings you can't back with a file/line or command output.

### Phase 4: Report

Output the report **before** any change. Keep it scannable:

```
## Project Review: <project name>

**Scope:** <what was checked / sampled, which CLAUDE.md sections were skipped and why>
**Checks run:** <commands and their result>

### Top priorities
1. <highest-impact finding, one line>
2. ...

### Findings by CLAUDE.md section

#### <Section name> — <compliant | N findings>
- **[High|Med|Low] <finding>** — `path/file.ext:42` — <evidence>. *Fix:* <concrete proposed change>. *Effort:* <S|M|L>

### Suggestions (need explicit approval — not applied by default)
- <new tooling / hooks / CI / test framework>, with the mistakes it would catch

### Already good
- <brief list of sections/areas that comply>
```

Rank by impact on an agent's ability to orient, verify its own work, and avoid regressions — not by count. Separate **fixes** (bring existing code in line with the rules) from **suggestions** (add something new). Don't pad: a compliant section is one line.

End by asking which items to apply (all fixes / specific numbers / none).

### Phase 5: Apply

Apply only what the user approved, following the language docs and the duplication/scoping rules while editing. Then:

- Re-run the relevant lint/type/test commands and report actual results; if something fails, say so with the output.
- If edits change architecture, conventions, or setup, update README/CLAUDE.md per the "Keep CLAUDE.md and README current" section.
- Do **not** commit. If the user later asks, split into logical commits per the Git commits rules.
