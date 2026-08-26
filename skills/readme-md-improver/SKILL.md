---
name: readme-md-improver
description: Audit and improve README.md files in repositories. Use when user asks to check, audit, update, improve, or fix README.md files. Scans for README files, evaluates quality against templates, outputs a quality report, then makes targeted updates. Also use when the user mentions "README maintenance" or "documentation audit".
tools: Read, Glob, Grep, Bash, Edit
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
| Contribution/dev workflow | Low–Medium | If the project takes contributions, is the dev loop documented? |

**Quality Scores:**
- **A (90-100)**: A stranger could clone, run, and understand the project from this alone
- **B (70-89)**: Good coverage, minor gaps
- **C (50-69)**: Gets the basics across but missing key sections
- **D (30-49)**: Sparse, outdated, or mostly boilerplate
- **F (0-29)**: Missing, or so stale it would mislead a new reader

### Phase 3: Quality Report Output

**ALWAYS output the quality report BEFORE making any updates.**

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
- [List specific problems]

**Recommended additions:**
- [List what should be added]

#### 2. ./packages/api/README.md (Package-specific)
...
```

### Phase 4: Targeted Updates

After outputting the quality report, ask the user for confirmation before updating.

**Update Guidelines (Critical):** see [references/update-guidelines.md](references/update-guidelines.md) for full detail. In short:

1. **Propose targeted additions only** — missing install steps, a stale command, an out-of-date architecture description, a missing usage example, an unlisted required env var.
2. **Verify before writing** — check that commands, file paths, and dependency names discovered during analysis are actually still real (grep/`ls`/`package.json`, etc.) rather than assumed.
3. **Architecture sections get a diagram** — if the project has more than one real module/service and the README's Architecture section is prose-only (or missing), propose adding a short paragraph plus a ` ```mermaid ` `graph TD` diagram of the same modules and data flow. This is a standing convention for this user's projects, not optional polish — see [references/templates.md](references/templates.md) for the pattern.
4. **Show diffs** — for each change, show which file, the specific addition (diff or quoted block), and a one-line reason.

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

## What Makes a Great README.md

**Key principles:**
- Answers "what is this and why would I use it" in the first paragraph
- Getting-started commands are copy-paste ready and actually work
- At least one concrete usage example, not just a reference link
- Architecture explained in prose *and* a Mermaid diagram when the project has real internal structure
- Reflects the current state of the repo, not an earlier version of it

**Recommended sections** (use only what's relevant):
- Title + one-line description (+ badges if applicable)
- Getting Started / Installation
- Usage (with example)
- Architecture (prose + Mermaid `graph TD` for multi-module projects)
- Configuration (env vars, config files)
- Development / Contributing
- Testing
- License
