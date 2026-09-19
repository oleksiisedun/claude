# README.md Quality Criteria

## Scoring Rubric

### 1. Project Description (20 points)

**20 points**: First few lines clearly state what the project is, who it's for, and why it exists
- One-line summary immediately visible
- Value proposition or problem being solved is clear
- Not just a repeated repo name

**15 points**: Description present but vague or buried

**10 points**: Minimal description, no context on purpose

**5 points**: Title only, reader has to infer purpose from code

**0 points**: No description at all

### 2. Installation / Getting Started (20 points)

**20 points**: A new person can go from clone to running in copy-paste steps
- Prerequisites listed (runtime versions, system deps, accounts/API keys)
- Install command present and correct
- Run/start command present and correct

**15 points**: Steps present, minor gaps (e.g. missing a prerequisite)

**10 points**: Steps present but incomplete or assume prior knowledge

**5 points**: Vague instructions ("see package.json")

**0 points**: No setup instructions

### 3. Usage Examples (15 points)

**15 points**: At least one concrete, runnable example showing real usage
- Shows realistic input/output, not just a stub
- Covers the primary use case

**10 points**: Example present but trivial or incomplete

**5 points**: Only an API/CLI reference, no worked example

**0 points**: No usage example

### 4. Architecture (15 points)

**15 points**: Clear picture of how pieces fit together
- Key modules/services named and their relationships explained in prose
- For multi-module projects: a Mermaid diagram accompanies the prose (per this user's README convention)
- Entry points identified

**10 points**: Prose description present but no diagram for a project that would benefit from one

**5 points**: Vague or partial structure description

**0 points**: No architecture info, or purely a raw directory listing with no explanation

### 5. Configuration (10 points)

**10 points**: All required env vars/config documented with purpose

**5 points**: Some config documented, gaps remain

**0 points**: Config required to run but undocumented

### 6. Currency (10 points)

**10 points**: Everything checks out against the current repo
- Commands work as documented
- Referenced files/paths exist
- Described structure matches actual layout

**5 points**: Mostly current, one or two stale references

**0 points**: Severely outdated (renamed commands, deleted files, old stack described)

### 7. Contribution / Dev Workflow (10 points)

**10 points**: Dev loop documented (tests, lint, branch/PR conventions) where the project takes contributions

**5 points**: Partial (e.g. test command only)

**0 points**: Missing where clearly needed, or N/A for a project that doesn't take contributions (score as 10 if genuinely not applicable — don't penalize a private/personal repo for lacking a CONTRIBUTING flow)

## Assessment Process

1. Read the README.md file completely
2. Cross-reference with the actual codebase:
   - Check that install/run/test commands exist in `package.json`, `Makefile`, etc.
   - Check that referenced files/directories exist
   - Verify the architecture description against actual module structure
   - Check LICENSE file presence vs. README's license claim
3. Score each criterion
4. Calculate total and assign grade
5. List specific issues found
6. Propose concrete improvements

### Verification recipes

Every README claim you report as stale or correct should have been checked, not assumed:

| Claim in README | Check |
|-----------------|-------|
| A CLI command (`tool sub-cmd`) | `<tool> --version`, then `<tool> --help` / `<tool> <cmd> --help` for the **installed** version. An unknown subcommand prints top-level help instead of erroring — read the output. Never run push/deploy/publish to test. |
| A file the reader must have (`.env`, `.clasp.json`, a targets/config file) | `git check-ignore -v <file>` / read `.gitignore`. If it's ignored, a fresh clone lacks it — the README must say how to create it and what it must contain. Confirm a minimal version works with a read-only command (e.g. `clasp status` against a scratch config) before documenting it. |
| Setup steps | List what scripts in the repo shell out to (`jq`, `curl`, …) and confirm each is a stated prerequisite. |
| Dev workflow | Read `package.json` `scripts` / `Makefile` targets; every check, lint, typecheck script should appear. Run the aggregate command once (it must be fast, local and non-destructive) and report the result. |
| A function/file/constant named in prose | `grep`/`ls` for it. |
| Config tables | Diff the documented constants against the config file; ignore purely internal regexes/helpers. |
| Relative links and anchors | `python3 ~/.claude/skills/readme-md-improver/scripts/check_md_links.py` |
| Declared license | `ls LICENSE*` vs. the `license` field in `package.json`; flag a mismatch, don't create the file. |

## Red Flags

- Install/run commands that would fail (renamed scripts, wrong package manager)
- References to deleted files/folders or removed features
- Outdated tech stack description (e.g. still describes a framework that's been migrated away from)
- Boilerplate left over from a template (`<Project Name>`, placeholder badges, Lorem ipsum)
- Architecture section that's just a raw `tree` dump with no explanation
- Multi-module/service project with an Architecture section but no diagram
- Broken relative links to docs that have moved
- "Coming soon" sections that have clearly been stale for a long time
- Getting-started steps that need a git-ignored file the README never tells the reader to create
- Documented commands that don't exist in the installed CLI version
- Changelog-style prose ("now…", "previously…", "used to…") describing history instead of current behavior
- 250+ lines mixing onboarding with per-feature reference (schema tables, config tables, algorithm notes) — recommend a split per [splitting-guidelines.md](splitting-guidelines.md); not scored, but report line count and per-section sizes
- README duplicating `docs/architecture-*.md` content — flag only, since the audiences differ
