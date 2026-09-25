# JavaScript / TypeScript conventions

## JavaScript — modern JS only

Use ES2020+ everywhere — `const`/`let`, arrow functions, template literals, optional chaining (`?.`), nullish coalescing (`??`), `Array.includes()`, `element.remove()`. Never use `var` or old-style `function()` callbacks. Closure-capturing IIFEs (`(function(x){...})(x)`) are never needed — arrow functions in `forEach` close over `const`/`let` correctly.

## JSDoc — plain JS vs TypeScript

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

**Keeping JSDoc in sync** — when a function's signature or behavior changes (added/removed/renamed parameters, changed types or return value, changed purpose), update its JSDoc in the same edit so it describes the current behavior.

## Guardrails

Use what the project already has; when suggesting a missing check (don't add it unprompted):

- **Lint**: ESLint with a flat config (`eslint.config.js`) — `@eslint/js` recommended, plus `typescript-eslint` for TS. Apps Script needs runtime-specific settings: see [google-apps-script.md](google-apps-script.md#linting).
- **Types**: TS — `tsc --noEmit`. Plain JS — a `jsconfig.json` with `allowJs` + `checkJs`, run as `tsc --noEmit -p jsconfig.json`, so the JSDoc types above are actually checked.
- **Format**: Prettier — `prettier --check .` as the check, `prettier --write .` to fix.
- **One entry point**: expose each as an npm script (`lint`, `typecheck`, `format:check`, `test`) plus an aggregate `check` that runs them all. Document it in the project's CLAUDE.md.

## Testing

Where tests are worth adding, see [unit-tests.md](unit-tests.md). Use the project's existing runner; when suggesting one for a project that has none:

- **TypeScript, Vite, or bundled projects**: Vitest. **Dependency-free plain JS scripts**: the built-in `node --test`.
- **Script**: expose a single-run `test` script (`vitest run`, not watch mode) so the command exits and can be used as a check.
- **Layout**: always put tests in a top-level `tests/` directory (plural), not `test/` (the runner default) and not colocated next to the source. If the project already has a `test/` directory, suggest renaming it to `tests/` (don't rename unprompted) and, until it's renamed, add new tests there rather than creating a second directory.
- **Unit + E2E in one project**: split by kind under the same root — `tests/unit/` and `tests/e2e/` (point Playwright's `testDir` at `tests/e2e`) — with one aggregate `test` script. Don't add a unit runner to an E2E-only project unless it fits this layout (see [unit-tests.md](unit-tests.md)).
- **Unit-only project**: keep tests flat in `tests/*.test.js` — don't preemptively nest under `tests/unit/` on the assumption a project might grow an E2E suite later. Nest only once `tests/e2e/` actually exists alongside it.
- **Node runner and `tests/`**: `node --test` only auto-discovers `test/`, so point it at the directory explicitly with a glob — `node --test "tests/**/*.test.js"` (quoted, so Node expands it and it works on Node 21+, where bare directory arguments no longer recurse). Vitest finds `*.test.ts` anywhere, so it needs no extra config.
