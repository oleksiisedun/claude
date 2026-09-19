# Splitting an oversized README into docs/

A README is an entry point. When it grows into a manual, newcomers can't find the setup steps and the reference rots. This is the user's "Docs, splitting and ADRs" convention applied to README.md: split it out to `docs/` and link, the same way CLAUDE.md links to its docs.

## When to propose a split

Flag it in the report (as a "Structure/size" finding, unscored) when **both** hold:

- The README is roughly **250+ lines** — measure it, and get per-section sizes:
  ```bash
  wc -l README.md
  awk '/^## /{if(n)printf "%4d  %s\n",NR-s,n;n=$0;s=NR} END{printf "%4d  %s\n",NR-s+1,n}' README.md
  ```
- It mixes an **entry-point half** (description, architecture, getting started, dev workflow) with a **reference half** (layout/schema tables, per-feature behavior, config tables, long algorithm notes) that a first-time reader doesn't need on the first screen.

Length alone isn't the trigger — a long README that is all onboarding is fine. Don't propose a split below ~200 lines.

## Know the audiences before choosing destinations

Look at what already exists in `docs/` and CLAUDE.md before proposing files:

- **Contributor/agent docs** (e.g. `docs/architecture-*.md` linked from CLAUDE.md): function names, ordering constraints, gotchas. Claude reads these on demand.
- **User-facing reference** (what the README's middle section usually is): how to lay out the data, what each feature does, what each config value means.

**Do not pour user-facing reference into contributor/agent docs** — it bloats files that are loaded for code changes and blurs two audiences. Create new user-facing files beside them instead. Overlap between the two sets is normal; separating the audiences doesn't remove it, so flag the overlap as a follow-up rather than silently deleting from either side.

## What to propose

Present a table with measured line counts, then what stays:

| New file | Moves from the README | Lines |
|---|---|---|
| `docs/<topic>.md` | `<section>`, `<section>` | ~N |

Group by reader question, not by README order (e.g. setup/schema, features, exports, configuration). Name files after the responsibility they hold. Aim for files of roughly 50–150 lines.

**The README keeps:** title + description, the architecture paragraph + Mermaid diagram + file table, a **short Features overview** (5–6 bullets — otherwise a reader who never opens `docs/` can't learn what the tool does), Getting started, Development, and a **Documentation** index (one line per doc, plus a line pointing contributors at any `architecture-*.md`). Add new docs to the file table if it lists `docs/`.

Ask before doing it; offer a coarser split (fewer files) as the alternative.

## Mechanics (do it programmatically, not by retyping)

1. Save the original: `cp README.md <scratchpad>/README.orig.md`.
2. Get section line numbers: `grep -n '^## ' README.md`.
3. Extract sections **verbatim** by line range (`sed -n 'A,Bp'`) into the new files. Each new file gets a `# Title`, a one-line intro, and a `Back to the [README](../README.md)` link; the moved `##`/`###` headings keep their levels. Squeeze doubled blank lines (`cat -s`).
4. **Retarget cross-file anchors.** A link like `(#computed-values)` that now lives in a different file than its target must become `(exports.md#computed-values)`; links whose target moved with them stay as they are. List them first: `grep -n '](#' README.md`. Links from the README into moved sections become `docs/<file>.md#anchor`.
5. Rebuild the README from the kept ranges plus the new Features and Documentation sections. Update any intro line that pointed at "docs/" as contributor-only.
6. **Verify** (next section) before showing the result.

GitHub anchors: lowercase, punctuation stripped, spaces to hyphens; Cyrillic and other Unicode letters are kept (`#photo-export-for-s-кадр`).

## Verify

```bash
python3 ~/.claude/skills/readme-md-improver/scripts/check_md_links.py --original <scratchpad>/README.orig.md
```

It checks every relative link and heading anchor across README.md and `docs/**/*.md`, and lists any original line that no longer appears anywhere. Expect "not found" only for text you deliberately reworded (the intro line, the `docs/` file-table row, a heading that became a file title); anything else is lost content — fix it. Exit code 1 means a broken link.

## Keep CLAUDE.md in sync

If the project's CLAUDE.md lists its docs or says where config/reference lives, **propose** a short pointer to the new user-facing docs and when to update them (new config constant, Handbook/schema change, new user-visible feature). Without it, future sessions keep editing a README section that no longer exists. Propose it; don't add it unprompted if the user hasn't approved CLAUDE.md edits.

## Commits

Never commit unprompted. When the user asks, split logically: README + new docs in one commit, CLAUDE.md pointer in another (and separate any unrelated README fixes if the working tree allows).
