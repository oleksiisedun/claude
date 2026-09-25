---
name: sync-main
description: Bring the current feature branch up to date with the remote default branch (main/master) by merging it in. Use when the user wants their branch synced with, updated from, or caught up to main — including pulling in teammates' merged changes — typically before opening or updating a pull request.
---

# Sync Feature Branch with Main

Bring a feature branch up to date with an updated main/master branch by merging main into it, so the eventual PR merges cleanly. Use `git merge`, not `git rebase` — this keeps the feature branch's existing commit history and hashes intact, which is safe even if the branch has already been pushed or shared with others.

## Procedure

1. **Check the working tree is clean.** Run `git status`. If there are uncommitted changes, stop and ask the user whether to commit or stash them first — do not proceed with a dirty working tree, since a merge can fail or produce confusing conflicts on top of unrelated local edits.

2. **Confirm the current branch is a feature branch**, not main/master itself. Run `git branch --show-current`. If it matches the repo's default branch, tell the user there's nothing to sync and stop.

3. **Determine the default branch name.** Don't assume `main` — check with:
   ```
   git symbolic-ref refs/remotes/origin/HEAD --short
   ```
   This prints e.g. `origin/main` or `origin/master`. If it errors (no cached HEAD ref), fall back to `git remote show origin | grep 'HEAD branch'`.

4. **Fetch the latest state from the remote:**
   ```
   git fetch origin
   ```
   This updates `origin/<default-branch>` without touching the local default branch or the current feature branch, so it's safe to run regardless of whether the user has a local main branch checked out elsewhere.

5. **Merge the remote default branch into the current feature branch:**
   ```
   git merge origin/<default-branch>
   ```

6. **If the merge completes cleanly** (no conflicts), report success to the user and mention the branch is now caught up. Ask before pushing — pushing affects the shared remote, so confirm first: `git push`.

7. **If the merge produces conflicts:**
   - Run `git status` to list the conflicting files.
   - Open each conflicting file, resolve the `<<<<<<<` / `=======` / `>>>>>>>` markers by choosing or combining the correct content, and remove the markers.
   - Stage each resolved file with `git add <file>`.
   - Run the project's relevant checks (lint, typecheck, tests — whichever it has and the conflicted files touch) and note the results. Don't run builds or scripts with side effects.
   - Show the user each resolved file with a one-line summary of how it was resolved, plus the check results, and ask before committing. Resolutions are your judgment calls — the user's request to sync doesn't cover them.
   - On approval, complete the merge with `git commit` (Git pre-fills a merge commit message — keep it as-is unless the user wants to customize it) or `git merge --continue`.
   - Do not use `git merge --abort` unless the user explicitly asks to cancel the sync — it discards the merge in progress.
   - After the merge commit is made, ask before pushing, same as step 6.

## Notes

- Never force-push after this workflow — a merge (unlike a rebase) doesn't rewrite existing commits, so a normal `git push` is always sufficient.
- If the feature branch's upstream isn't set yet, use `git push -u origin <branch-name>` instead of a plain `git push`.
- If `git fetch` reports the local repo has no `origin` remote, stop and ask the user how their remote is configured rather than guessing a URL.
