# Code conventions (all JS projects)

### JavaScript — modern JS only

Use ES2020+ everywhere — `const`/`let`, arrow functions, template literals, optional chaining (`?.`), nullish coalescing (`??`), `Array.includes()`, `element.remove()`. Never use `var` or old-style `function()` callbacks. Closure-capturing IIFEs (`(function(x){...})(x)`) are never needed — arrow functions in `forEach` close over `const`/`let` correctly.

### JSDoc — plain JS vs TypeScript

**Plain `.js` files** — every function must have a JSDoc comment with typed `@param` and `@returns` tags, since there's no other source of type information. One-line description is enough.

```js
/**
 * Fetches a Drive file and returns its base64-encoded content.
 * @param {string} fileId
 * @returns {{ type: string, data: string }|{ type: 'no-access' }}
 */
function getImageAsBase64(fileId) { ... }
```

**TypeScript (`.ts`/`.tsx`)** — JSDoc is added only when the signature leaves a real question unanswered: intent, a non-obvious invariant, a gotcha, or a usage example. No `@param`/`@returns` type annotations — TS already owns that. Skip JSDoc entirely when the name + signature are self-explanatory. Litmus test: if hovering the function in an IDE still leaves you wondering "why does this work this way," add one or two sentences; otherwise don't.

**Keeping JSDoc in sync** — whenever a function's signature or behavior changes, updating its JSDoc is mandatory, not optional. This includes: added/removed/renamed parameters, changed types, changed return value, or a changed description of what it does. Never leave a stale JSDoc comment describing the old behavior.

### Code duplication (all software projects)

**Before writing new code, check what already exists.** Search for functions, patterns, or constants that do the same thing. Three similar lines copy-pasted is worse than one named helper — each copy is a future bug waiting to diverge.

**Extract when a pattern appears twice.** The threshold is two: the second copy is the signal to extract, not the third. Name the helper after what it does, not where it's used.

**During development** — when adding code that resembles something nearby, stop and extract the shared logic into a helper before continuing.

**During review / refactoring** — when touching a file, note any patterns that appear more than once and flag them. If the scope of the task allows, extract them in the same PR; if not, mention them explicitly so they aren't forgotten.

**Configuration and magic values belong in one place.** Constants, regex patterns, type definitions, and tuning parameters should be declared once (in a config or constants file) and referenced everywhere. Never inline a value that appears — or could appear — in more than one location.

**The bar for extraction is low; the bar for a new abstraction is high.** A two-line helper that eliminates duplication is always worth it. A new layer of indirection that trades duplication for complexity is not — prefer a clear duplicate over a confusing abstraction.

# Playwright Tests (E2E only — no other test frameworks in use)

In projects that use Playwright:

After finishing Playwright test code, always ask the user if they want to actually run the test before proceeding.

When asked to fix a test, treat it as already broken — do not run it first. To understand the current UI state, use browser tools (take a screenshot, capture a DOM snapshot, or read the relevant component source code). Fix the test based on what you observe. Only ask the user for the test report if none of those approaches are sufficient to diagnose the issue.

# Front-end repos only

### data-testid

In front-end projects that use `data-testid` attributes, follow the naming and structure conventions in [docs/data-testid.md](docs/data-testid.md).

### CSS design system

When starting a new HTML/CSS project or touching a stylesheet for the first time, define `:root` tokens (colors, radius) and shared classes (`.btn-primary`, `.overlay`) **before** writing one-off component rules, with one broad rule per interaction state (disabled, focus, hover). Check existing rules before adding a new one. Full rules: [docs/css-design-system.md](docs/css-design-system.md).

# Making the project better for AI-assisted development (all software projects)

The goal is a repo where an agent can orient quickly, verify its own work, and not repeat past mistakes. When working in any project, look for gaps in the areas below and suggest fixes — never add tooling, hooks, or config unprompted.

### Machine-checkable guardrails

When working in a project, check whether it has commands an agent can run to verify its own work — a linter, a type checker, a formatter check, a build, a dependency/import-boundary check. If some are missing, suggest adding them (don't add them unprompted), and say which mistakes each would catch. Prefer a check that fails loudly with a non-zero exit code over a convention that only lives in prose.

- **One entry point**: expose the checks as named scripts (e.g. `npm run lint`, `npm run typecheck`, `make check`) and, if there are several, a single aggregate command, so an agent doesn't have to guess the invocation.
- **Fast and deterministic**: guardrails an agent runs after every edit should finish in seconds and never depend on network or flaky state. Slower checks belong in CI, not in the edit loop.
- **Turn recurring review comments into rules**: if the same mistake keeps getting corrected by hand (a banned pattern, a naming convention, a forbidden import), suggest encoding it as a lint rule or a small script rather than restating it in CLAUDE.md.
- **Enforce at the edges too**: suggest wiring the aggregate command into a pre-commit hook or CI so the guardrail can't be skipped — but never install hooks or CI config unprompted.
- **Document the commands** in the project's CLAUDE.md so future sessions know what to run and when.
- **Stay within existing tooling**: this doesn't override the E2E-only testing rule above — suggest static checks (lint, types, format, build), not new unit-test frameworks.

### Keep CLAUDE.md and README current

After completing any code edits, check whether the changes affect the README or CLAUDE.md — update them if the architecture, conventions, or project setup have changed. Don't update them for routine bug fixes or small internal changes that don't affect how the project is used or understood.

If the project has no CLAUDE.md or no README, suggest adding one — don't add it unprompted.

When creating a new README, or adding/rewriting an "Architecture" section, suggest a short prose paragraph plus a Mermaid `graph TD` diagram (in README.md, never CLAUDE.md). Check every label against Mermaid's grammar pitfalls before finalizing: [docs/readme-mermaid.md](docs/readme-mermaid.md).

### Docs, splitting and ADRs

If CLAUDE.md or README has grown large enough that a section would read better on its own (a lengthy convention writeup, detailed setup steps, etc.), suggest splitting it into a `/docs` directory and linking to it, rather than letting the root file keep growing.

When linking to a split-out doc from CLAUDE.md, choose the reference form deliberately: use `@docs/file.md` (Claude Code's import syntax) only for content that must always be in effect regardless of project type — it loads unconditionally into every session. Use a plain Markdown link (`[docs/file.md](docs/file.md)`) for conditionally-scoped content (e.g. "front-end repos only," "projects that use X") — Claude reads it on demand when the task is actually relevant, so unrelated projects don't pay for content they'll never use.

If a design or architecture choice keeps getting re-derived or re-litigated across sessions (e.g. re-explaining why a library was picked over an alternative, or why a pattern that looks wrong is actually intentional), record it as a short ADR in `docs/decisions/` (e.g. `docs/decisions/0003-use-x-over-y.md`: context, decision, consequences) instead of re-explaining it each time. Link to it from CLAUDE.md or the README with a plain Markdown link, not `@import`.

### Scoped files

Small, single-purpose files are cheaper for an agent to navigate and fit in context. Keep files scoped to one responsibility. If a file grows past roughly 300-400 lines **and** contains more than one clear responsibility (e.g. a service class plus its unrelated helpers, or a component plus unrelated utility functions), split it along that responsibility boundary into separate files.

Don't split a cohesive, single-purpose file just to hit a line count — a long file that does one thing well is better than several small files that only make sense read together. The trigger is mixed responsibilities, not length alone; length is just the signal to go look.

When splitting, name each new file after the responsibility it holds, not after the file it was extracted from.

# Agent behavior and safety

### Git commits

Always split changes logically into multiple commits when appropriate.
Group related changes together and use clear, descriptive commit messages.
Never bundle unrelated changes into a single commit.
Never commit or push automatically — only do so after a direct explicit command from the user.

### Working directory boundaries (all projects)

Never read, browse, or search files outside the current project's working directory — including other project folders elsewhere on disk (e.g. to borrow ideas, styling, or patterns) — unless the user has explicitly given permission and named the path in the current conversation. This applies even if it seems like it would produce a better or faster result. If outside context would genuinely help, ask the user first and name the specific path you want to look at.

### Google Apps Script (clasp)

Never run `clasp push` (or any command that deploys/pushes code to Apps Script) unless the user gives a direct, explicit command to do so in that moment. Making the code change is fine — pushing it live is not, without asking first.

For clasp project setup (suggesting the latest `@types/google-apps-script`, `.claspignore` entries), see [docs/google-apps-script.md](docs/google-apps-script.md).
