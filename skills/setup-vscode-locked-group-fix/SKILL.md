---
name: setup-vscode-locked-group-fix
description: This skill should be used when the user explicitly asks to "set up the VS Code locked group fix", "install the empty locked editor group workaround", "fix the empty locked group on VS Code startup", or invokes /setup-vscode-locked-group-fix. One-time setup that merges a user-level VS Code task into their tasks.json.
---

# Set up the VS Code empty-locked-group workaround

VS Code with the Claude Code extension can open with an empty, locked editor group. This skill installs a user-level VS Code task that runs on every folder open: it unlocks the editor groups and joins them into one. The task and its input live in [references/tasks.json](references/tasks.json) — that file is the source of truth; never retype it from memory.

This is a one-time, per-machine setup. It edits a file outside the repo (the user's VS Code user config), so follow the steps in order and never overwrite existing content silently.

## Procedure

1. **Locate the user-level `tasks.json`** for the OS (check `uname` / platform) and the VS Code flavor in use:

   | OS | Path |
   |---|---|
   | Linux | `~/.config/Code/User/tasks.json` |
   | macOS | `~/Library/Application Support/Code/User/tasks.json` |
   | Windows | `%APPDATA%\Code\User\tasks.json` |

   For VS Code Insiders replace `Code` with `Code - Insiders`; for VSCodium use `VSCodium`. If the flavor is unclear, ask the user. Only touch that one file.

2. **Read the existing file, if any.** VS Code accepts comments and trailing commas in `tasks.json` (JSONC), so parse it by reading it, not with a strict JSON parser or `jq`.
   - **Missing file:** create it from `references/tasks.json` as-is (after step 4).
   - **Present:** merge, per step 3.

3. **Merge, never replace.**
   - Add the task from `references/tasks.json` to the existing `tasks` array, and the `unlockAll` input to the existing `inputs` array (create either array if absent). Keep every existing task, input, comment and the existing `version`.
   - **Already installed** (a task labelled `Unlock and tidy editor groups` and an input with id `unlockAll` both exist): compare them with the reference. If identical, say so and stop. If they differ, show the difference and ask before changing anything.
   - **Conflicting id or label** that is a different task: stop and ask the user how to resolve it.

4. **Platform check on the `command`.** The task runs a no-op process purely to trigger the `${input:unlockAll}` command input. `/usr/bin/true` exists on Linux and macOS. On Windows it does not — substitute an equivalent no-op such as `"command": "cmd"` with `"args": ["/c", "exit", "0", "${input:unlockAll}"]`, and tell the user this variant is untested.

5. **Show the user what will change** (the added entries, or the new file) and get a go-ahead before writing.

6. **Back up, then write.** If the file exists, copy it to `tasks.json.bak` next to it, then write the merged result, preserving the file's indentation and comments.

7. **Tell the user** to reload VS Code (`Developer: Reload Window`) and, on first run, to accept VS Code's prompt if it asks to allow automatic tasks (`task.allowAutomaticTasks` — a user-level setting; do not change it without asking). Mention the backup path.

## Notes

- Do not run `code` or start VS Code from the shell to test; the fix can only be confirmed by the user reopening a folder.
- To remove the workaround, delete the task labelled `Unlock and tidy editor groups` and the `unlockAll` input from the same file (or restore `tasks.json.bak`).
