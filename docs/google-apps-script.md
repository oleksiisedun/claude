# Google Apps Script (clasp) projects

The hard rule — never run `clasp push` without a direct, explicit command — lives in [CLAUDE.md](../CLAUDE.md#google-apps-script-clasp). This file holds the situational setup advice.

## Project layout: deployable code in `src/`

If a clasp project keeps its Apps Script files (`*.js`/`*.gs`, `*.html`, `appsscript.json`) in the repo root next to tooling and docs (`package.json`, lint/tsconfig files, `README.md`, `CLAUDE.md`, push scripts), suggest moving them into a `src/` directory (don't restructure unprompted). Only `src/` is deployed; everything else stays at the root.

- **`.clasp.json`**: set `"rootDir": "src"`. `appsscript.json` must live inside `src/` too. `.clasp.json` is usually git-ignored, so mention that every checkout (and any re-run of `clasp clone`/`clasp create`) needs `rootDir` re-added.
- **`.claspignore`**: becomes redundant — `src/` should contain only files that ship — so remove it rather than maintaining a list of tooling files that must not be pushed.
- **Tooling paths**: point `jsconfig.json`/`tsconfig.json` `include`, ESLint file globs and the `lint`/`typecheck` npm scripts at `src/`, and re-run the project's check command afterward.
- **Multi-target push scripts** that only rewrite `scriptId` (e.g. via `jq`) keep `rootDir` and need no change.
- **Stay shallow**: Apps Script has one shared global scope, and clasp flattens subfolders into script file names like `ui/Page`, which forces renaming every `createTemplateFromFile`/`createHtmlOutputFromFile` call. Don't nest `src/` further unless the user asks.
- Move with `git mv` so history follows the files, update path references in `README.md`/`CLAUDE.md`, and note the `rootDir` requirement in the setup section of the README.

## `@types/google-apps-script`

If a clasp project has no `@types/google-apps-script` dev dependency yet, suggest adding it (don't add it unprompted). Always install the latest version — run `npm install --save-dev @types/google-apps-script@latest` (or `npm install -D @types/google-apps-script@latest`) rather than copying a version number from another project or from memory, since the typings track new Apps Script APIs and pinned old versions produce false "missing member" diagnostics. It's dev-only tooling — nothing about it gets pushed to Apps Script or affects runtime — but it fixes false-positive editor diagnostics on Apps Script globals (`SpreadsheetApp`, `ScriptApp`, `PropertiesService`, event types like `GoogleAppsScript.Events.SheetsOnEdit`, etc.) and lets JSDoc `@param`/`@returns` types be checked against the real API shapes. If the project doesn't use the `src/` layout above, remember to add `node_modules`/`package.json`/`package-lock.json` to `.claspignore` when introducing it, so they aren't pushed alongside the script files.
