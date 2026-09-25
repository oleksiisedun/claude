---
name: readme-md-improver
description: Audit and improve README.md files in repositories. Use when user asks to check, audit, update, improve, or fix README.md files. Scans for README files, evaluates quality against templates, outputs a quality report, then makes targeted updates. Also use when the user mentions "README maintenance" or "documentation audit".
---

# README.md Improver

Audit, evaluate, and improve README.md files across a codebase so human readers (contributors, users, new team members) get an accurate, useful entry point.

**This skill can write to README.md files.** After presenting a quality report and getting user approval, it updates README.md files with targeted improvements.

Unlike CLAUDE.md (written for Claude's context window), a README is written for **people**. Judge it on onboarding a new human, not on token efficiency — some redundancy with code, screenshots, and friendlier prose are fine here even though they'd be waste in CLAUDE.md.

## Workflow

### Phase 1: Discovery

Find all README files in the repository:

```bash
find . -iname "readme.md" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | head -50
```

**File Types & Locations:**

| Type | Location | Purpose |
|------|----------|---------|
| Project root | `./README.md` | Primary entry point — what the project is, how to install/run it |
| Package-specific | `./packages/*/README.md` | Module-level docs in monorepos |
| Docs directory | `./docs/*.md` | Split-out detailed docs (setup, architecture, etc.) linked from root README |
| Subdirectory | Any nested location | Feature/example-specific README |

**Note:** A repo may have zero README files. If so, treat this as a discovery finding, not an error — offer to create one (see Phase 5) rather than silently skipping.

### Phase 2: Quality Assessment

For each README.md file, evaluate against quality criteria. See [references/quality-criteria.md](references/quality-criteria.md) for detailed rubrics.

**Quick Assessment Checklist:**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Project description | High | Does it say what the project is and why it exists, in the first few lines? |
| Installation / getting started | High | Can a new person get it running by copy-pasting commands? |
| Usage examples | High | Are there concrete examples, not just an API reference link? |
| Architecture | Medium | Is there a clear picture of how the pieces fit together, with a Mermaid diagram if the project has real internal structure? |
| Configuration | Medium | Are required env vars / config documented? |
| Currency | High | Do commands, paths, and described structure match the actual repo right now? |
| Contribution/dev workflow | Low–Medium | If the project takes contributions, is the dev loop documented (every check/lint/typecheck script in `package.json`/`Makefile`)? |
| Structure / size (unscored) | Medium | Is it 250+ lines, mixing an entry-point half with a reference half? If so, propose a split into `docs/` — see [references/splitting-guidelines.md](references/splitting-guidelines.md) |

Verify claims against the repo, don't just read them: check commands against the **installed** CLI version (`<tool> --help` — a command documented for an older major version may be gone), check whether files the README tells people to use are git-ignored (`git check-ignore <file>`) and so absent on a fresh clone, look for external tools scripts depend on (e.g. `jq`), and run the project's own check command if it has one. Recipes are in [references/quality-criteria.md](references/quality-criteria.md). Never run deploy/push/publish commands to "test" a README step.

**Quality Scores:**
- **A (90-100)**: A stranger could clone, run, and understand the project from this alone
- **B (70-89)**: Good coverage, minor gaps
- **C (50-69)**: Gets the basics across but missing key sections
- **D (30-49)**: Sparse, outdated, or mostly boilerplate
- **F (0-29)**: Missing, or so stale it would mislead a new reader

### Phase 3: Quality Report Output

Output the quality report before making any updates.

Format:

```
## README.md Quality Report

### Summary
- Files found: X
- Average score: X/100
- Files needing update: X

### File-by-File Assessment

#### 1. ./README.md (Project Root)
**Score: XX/100 (Grade: X)**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Description | X/20 | ... |
| Installation/Getting started | X/20 | ... |
| Usage examples | X/15 | ... |
| Architecture | X/15 | ... |
| Configuration | X/10 | ... |
| Currency | X/10 | ... |
| Contribution/workflow | X/10 | ... |

**Issues:**
- [List specific problems, each verified against the repo]

**Structure / size:** [line count, per-section sizes if 250+ lines, and whether a split is recommended]

**Recommended additions:**
- [List what should be added]

**Flag only (no change proposed):**
- [Things the user should decide: missing LICENSE file vs. declared license, README/docs overlap, etc.]

#### 2. ./packages/api/README.md (Package-specific)
...
```

After the report, list the concrete proposed updates as numbered diffs (see Phase 4) and end by asking whether to apply all, or a subset.

### Phase 4: Targeted Updates

After outputting the quality report, ask the user for confirmation before updating.

**Update guidelines:** see [references/update-guidelines.md](references/update-guidelines.md) for full detail. In short:

1. **Propose targeted additions only** — missing install steps, a stale command, an out-of-date architecture description, a missing usage example, an unlisted required env var.
2. **Verify before writing** — check that commands, file paths, and dependency names discovered during analysis are actually still real (grep/`ls`/`package.json`, etc.) rather than assumed.
3. **Architecture sections get a diagram** — if the project has more than one real module/service and the README's Architecture section is prose-only (or missing), propose adding a short paragraph plus a ` ```mermaid ` `graph TD` diagram of the same modules and data flow. This is a standing convention for this user's projects, not optional polish — see [references/templates.md](references/templates.md) for the pattern, and check every label against the grammar pitfalls in `~/.claude/docs/readme-mermaid.md` before proposing it.
4. **Show diffs** — for each change, show which file, the specific addition (diff or quoted block), and a one-line reason.
5. **Oversized README → propose a split** — if the README is 250+ lines and mixes entry-point content with reference material, propose moving the user-facing reference into new `docs/*.md` files and linking them (same pattern as the user's CLAUDE.md → docs links). Give a table of new files with measured line counts and what the README keeps (description, architecture + diagram, file table, short Features overview, Getting started, Development, Documentation index). Keep user-facing docs separate from any contributor/agent `architecture-*.md` docs. Ask before splitting. Full method: [references/splitting-guidelines.md](references/splitting-guidelines.md).
6. **Propose a CLAUDE.md pointer** — after a split (or any change to where reference docs live), if the project's CLAUDE.md maps its docs, propose a short line pointing at the new docs and saying when to update them. Propose it; don't add it unprompted.

**Diff Format:**

```markdown
### Update: ./README.md

**Why:** No install/run instructions — a new clone can't get started without reading package.json.

```diff
+ ## Getting Started
+
+ ```bash
+ npm install
+ npm run dev  # http://localhost:3000
+ ```
```
```

### Phase 5: Apply Updates

After user approval, apply changes using the Edit tool. Preserve existing tone, structure, and any project-specific sections (badges, sponsors, etc.) — don't impose a template wholesale onto a README that already has a working structure.

**After applying, validate** — run `python3 ~/.claude/skills/readme-md-improver/scripts/check_md_links.py` from the repo root (add `--original <saved copy of the old README>` after a split, saved *before* editing). It checks every relative link and heading anchor across README.md and `docs/**/*.md` and reports any original line that disappeared. Fix anything unexpected before presenting the result, and report the counts. Do not commit unless the user asks; when they do, split logically (README + new docs, then any CLAUDE.md change).

If no README exists at all, do not create one silently — confirm with the user first, then use a template from [references/templates.md](references/templates.md) as a starting point, filled in from the actual codebase.

## Templates

See [references/templates.md](references/templates.md) for README templates by project type, including the Architecture-section Mermaid pattern.

## Common Issues to Flag

1. **Stale install/run commands**: scripts that no longer exist in `package.json`/`Makefile`/etc.
2. **Missing prerequisites**: required runtime versions, system deps, or accounts (API keys) not mentioned
3. **Outdated architecture description**: directory structure or module list that's drifted from reality
4. **No usage example**: only an install section, nothing showing the thing actually working
5. **Broken links**: relative links to docs/files that have moved or been deleted
6. **Missing license/badges**: if the repo has a LICENSE file but the README doesn't mention it
7. **Architecture section without a diagram**: prose-only description of a multi-module system (per this user's README convention)
8. **Setup dead end**: the README says to run/push/deploy but never says how to create a required config file (especially a git-ignored one such as `.clasp.json` or `.env`), or omits a key setting (e.g. clasp's `rootDir`)
9. **Command that doesn't exist in the installed version**: e.g. `clasp open` in clasp 3.x (now `open-script`) — check with `--help`
10. **Undocumented prerequisites and scripts**: external tools the repo's scripts need (`jq`, …) not listed; `package.json` check/lint/typecheck scripts missing from a Development section
11. **Changelog-style prose**: "now does X", "previously…", "made … too large" — describe current behavior, not history
12. **Oversized README** (250+ lines with a reference half): propose a split into `docs/`; **flag only** README/docs overlap and a declared-but-missing LICENSE file rather than changing them

## What Makes a Great README.md

**Key principles:**
- Answers "what is this and why would I use it" in the first paragraph
- Getting-started commands are copy-paste ready and actually work
- At least one concrete usage example, not just a reference link
- Architecture explained in prose *and* a Mermaid diagram when the project has real internal structure
- Reflects the current state of the repo, not an earlier version of it
- Stays a short entry point — reference material (schema/layout tables, per-feature detail, config tables) lives in linked `docs/` files, with a short feature overview and a Documentation index in the README

**Recommended sections** (use only what's relevant):
- Title + one-line description (+ badges if applicable)
- Getting Started / Installation
- Usage (with example)
- Architecture (prose + Mermaid `graph TD` for multi-module projects)
- Configuration (env vars, config files)
- Development / Contributing
- Testing
- License
