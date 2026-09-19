# Google Apps Script (clasp) projects

The hard rule — never run `clasp push` without a direct, explicit command — lives in [CLAUDE.md](../CLAUDE.md#google-apps-script-clasp). This file holds the situational setup advice.

## `@types/google-apps-script`

If a clasp project has no `@types/google-apps-script` dev dependency yet, suggest adding it (don't add it unprompted). Always install the latest version — run `npm install --save-dev @types/google-apps-script@latest` (or `npm install -D @types/google-apps-script@latest`) rather than copying a version number from another project or from memory, since the typings track new Apps Script APIs and pinned old versions produce false "missing member" diagnostics. It's dev-only tooling — nothing about it gets pushed to Apps Script or affects runtime — but it fixes false-positive editor diagnostics on Apps Script globals (`SpreadsheetApp`, `ScriptApp`, `PropertiesService`, event types like `GoogleAppsScript.Events.SheetsOnEdit`, etc.) and lets JSDoc `@param`/`@returns` types be checked against the real API shapes. Remember to add `node_modules`/`package.json`/`package-lock.json` to `.claspignore` when introducing it, so they aren't pushed alongside the script files.
