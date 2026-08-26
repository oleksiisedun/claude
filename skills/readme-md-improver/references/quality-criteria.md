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

## Red Flags

- Install/run commands that would fail (renamed scripts, wrong package manager)
- References to deleted files/folders or removed features
- Outdated tech stack description (e.g. still describes a framework that's been migrated away from)
- Boilerplate left over from a template (`<Project Name>`, placeholder badges, Lorem ipsum)
- Architecture section that's just a raw `tree` dump with no explanation
- Multi-module/service project with an Architecture section but no diagram
- Broken relative links to docs that have moved
- "Coming soon" sections that have clearly been stale for a long time
