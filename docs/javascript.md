# JavaScript / TypeScript conventions

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

### Testing

Where tests are worth adding, see [unit-tests.md](unit-tests.md). Use the project's existing runner; when suggesting one for a project that has none:

- **TypeScript, Vite, or bundled projects**: Vitest. **Dependency-free plain JS scripts**: the built-in `node --test`.
- **Script**: expose a single-run `test` script (`vitest run`, not watch mode) so the command exits and can be used as a check.
- **Layout**: follow the existing convention; otherwise colocate `*.test.ts` / `*.test.js` next to the source.
- **Apps Script (clasp)**: keep logic in pure functions that take plain values, and confine `SpreadsheetApp`/`DriveApp`/etc. calls to thin wrappers, so the logic runs under Node without mocks.
