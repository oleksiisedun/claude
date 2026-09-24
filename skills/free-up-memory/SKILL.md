---
name: free-up-memory
description: Diagnose high system memory (RAM/swap) usage and reclaim it by stopping processes. Use when the user wants to check or free up memory, find what is using it, or recover after something was OOM-killed. Semi-automatic: it only ever analyzes and suggests — it kills a process solely on the user's direct, explicit command naming that process or PID.
tools: Bash
---

# Free Up Memory

Diagnose what's consuming system memory, present objective candidates for the user to consider stopping, and kill a process **only** when the user gives a direct, explicit command identifying it (by PID or an unambiguous process name). This skill never decides on its own that something is "safe" to kill — that judgment call belongs to the user, since only they know which browser tab, editor buffer, or running job holds work they care about.

## Procedure

1. **Get the overall picture first.**
   ```
   free -h
   ```
   Report total/used/free/available and swap usage in plain terms before doing anything else. If `available` is already comfortably high relative to what the user is trying to do, say so — there may be nothing worth killing.

2. **List memory consumers with objective signals, not verdicts.** Run something like:
   ```
   ps aux --sort=-%mem | head -25
   ```
   For each notable entry, surface facts the user can judge for themselves, not a "safe to kill" label:
   - RSS / %MEM
   - Process name and enough of the command line to identify *which* window/tab/job it is
   - CPU time vs. wall-clock age (a process with ~0 CPU time over a long elapsed time is idle; use `ps -o pid,etime,time,cmd -p <pid>` for this) — idle-and-heavy is a more useful signal than heavy-alone
   - State: zombie (`Z`), duplicate instances of the same app, orphaned processes (parent is `init`/PID 1 or a dead shell)

3. **Call out zombies separately and correctly.** A zombie (`Z` state, e.g. `ps aux | awk '$8 ~ /Z/'`) already released its real memory when it exited — only its exit-status entry remains. Killing it frees nothing; only its original parent reaping it (or the parent dying) clears the entry. Don't present zombies as memory-saving candidates — mention them only as harmless clutter if the user asks.

4. **Flag off-limits processes explicitly, don't just omit them.** Never suggest killing, and refuse to kill even on request without pushing back once:
   - Anything not owned by the invoking user (check the `USER` column) — needs elevated privileges and is out of scope for this skill.
   - System/session-critical processes: `init`/PID 1, kernel threads (`[bracketed]` names), `systemd*`, display server (`Xorg`, `wayland` compositors), `NetworkManager`, `sshd`, `dbus-daemon`, `pulseaudio`/`pipewire`.
   - The Claude Code session currently running this skill and its own subprocesses/MCP servers (e.g. `claude`, the shell process hosting this conversation, `playwright-mcp` or other `*-mcp` helper processes tied to this session) — killing these would cut off the very session helping with cleanup.
   - A process that is a live, actively-progressing job the user or this conversation started on purpose (e.g. a test run currently in flight) — check CPU time is advancing across two quick checks before assuming something is "just sitting there."

5. **Present the findings as a short, scannable list**, grouped roughly as "heavy + idle" / "heavy + duplicated" / "heavy + active (probably not a target)", each with PID, RSS, and identifying detail. End with a plain question: which of these (if any) should be stopped?

6. **Wait for an explicit, specific command.** Acceptable: "kill 12345", "kill the gnome-system-monitor process", "close the second Chrome window". Not acceptable as authorization to kill: a general "yes", "go ahead", or "do what you think is best" in response to the candidate list alone — if the user's reply doesn't clearly name which process(es), ask them to confirm which PID(s) before running `kill`.

7. **Re-validate the named target right before killing it, even if it was already on the candidate list.** Run `ps -p <pid> -o pid,user,etime,cmd` and confirm: it's still running, it's owned by the invoking user, its command line still matches what the user meant to target, and it doesn't match any off-limits criteria from step 4. Do this for *every* kill, not just ones for PIDs the user typed without seeing them in the list — PIDs get reused, and a stale or mistyped PID can silently point at a different (possibly critical) process by the time the kill runs. If the check fails or the process no longer matches, stop and tell the user rather than killing anyway.

8. **Kill gracefully first.** Use plain `kill <pid>` (SIGTERM) by default so the process can shut down cleanly (flush buffers, prompt to save, etc.). Only use `kill -9` (SIGKILL) if the user explicitly asks for a force-kill, or the graceful kill didn't take effect after a few seconds and the user confirms escalating.

9. **Verify and report.** Re-run `free -h` after killing and tell the user how much was actually reclaimed (or that the process didn't die and what to try next) — don't assume the kill worked just because the command returned success.

## Notes

- This skill is a diagnostic + confirmed-execution tool, not an automated memory manager — there is no mode where it kills something without a same-turn, specific human instruction to do so.
- If the user asks it to "just handle it" repeatedly, still surface the specific candidate(s) you're about to kill in that same response before running `kill`, so there's always a concrete, checkable record of what was targeted and why.
- Killing a multi-process app (e.g. one Chrome tab's renderer) may only close that tab/window rather than the whole app, or may occasionally destabilize the parent — mention this uncertainty when the target is a subprocess of a larger app rather than the app's main process.
