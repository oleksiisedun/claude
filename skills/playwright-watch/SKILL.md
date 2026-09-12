---
name: playwright-watch
description: Use when the user wants updates on a Playwright test run they started themselves in a terminal (not via Claude's Bash tool) — "check my test run", "how's the run going", "watch this run and tell me when it's done", "let me know if anything fails". Especially useful with Remote Control, since it can push status to the user's phone. Gives coarse process-alive status with zero setup; real pass/fail detail requires the run's output to be piped to a log file.
---

# Playwright Run Watcher

Claude Code cannot read a terminal you started outside of Claude Code — there's no
process handle, no stdout stream, nothing to attach to. That's an OS-level boundary,
not a missing feature. Two tiers of visibility follow from that:

- **Coarse status, zero setup** — check whether the process is still alive and how
  long it's been running, via the process list. No action needed from the user.
- **Real pass/fail detail** — only possible if the run's output was piped to a file
  Claude can read. Requires the user to have started the run with `tee`.

Don't imply real per-test detail is available when only the coarse check was done —
say "still running, ~4m so far" rather than making up or extrapolating a pass count.

## Tier 1: coarse check (always available)

Find the running Playwright process and how long it's been going:

```bash
ps -eo pid,etimes,cmd | grep -i "[p]laywright test"
```

- `etimes` is elapsed seconds since the process started — report it as minutes.
- No matching process means the run has finished or was never started this way;
  say so plainly rather than guessing at a result.
- Optionally note worker/browser activity as a rough "it's actively doing
  something" signal: `pgrep -c -f "(chrome|headless_shell)"`. This is not a
  progress percentage — don't present it as one.

This is what to fall back on when no log file exists. It cannot report pass/fail
counts, which test is running, or catch failures — say so if the user asks for
that level of detail, and offer the Tier 2 setup below instead of fabricating it.

## Tier 2: detailed watch (requires a log file)

### Starting a watchable run

The user pipes output through `tee` to a path keyed by the project directory name:

```bash
npx playwright test <your usual args> \
  2>&1 | tee "/tmp/claude-pw-run-$(basename "$PWD").log"
```

If the user wants failure detail or push notifications and no matching log file
exists (or it's stale — last modified more than ~20 minutes ago with no matching
process from the Tier 1 check still running), give them this exact command to
(re)run instead of falling back silently to Tier 1 without saying so.

### Finding the log

1. Default path: `/tmp/claude-pw-run-<basename of cwd>.log`.
2. If missing, check for other recent candidates:
   `ls -t /tmp/claude-pw-run-*.log 2>/dev/null | head -5`
   If more than one is recent enough to plausibly be "the" run, ask the user
   which one before proceeding — never silently pick among several fresh logs.

### 2a. On-demand status check
("how's it going", "check my run", "any failures yet")

One-shot, not `Monitor` — just read the current state of the log:

```bash
grep -c '✓' <log>   # passed so far
grep -c '✘' <log>   # failed so far
tail -20 <log>       # currently-running test / recent activity
```

Look for a final summary line (Playwright prints something like
`46 passed (3m)` or `2 failed`) to tell whether the run has finished. Report
counts, the currently-running test if still in progress, and whether it's
done — in plain text, not by dumping the log.

### 2b. Background watch with phone notification
("watch it", "let me know when it's done", "ping me if anything fails")

Arm a `Monitor`:

```bash
tail -f "<log>" | grep -E --line-buffered '✘|✗|^[[:space:]]*[0-9]+ (passed|failed)'
```

- `persistent: true`
- `description`: name the project/run, e.g. `"sportsbook_ui_tests playwright run"`

Behavior on events:
- A line containing `✘`/`✗` is a single test failure — note which test, but
  don't push-notify on every one (that's noisy and Monitor will auto-stop a
  chatty watch). Mention it in your own running context; save the push for
  something the user would act on right now if they're away.
- A line matching the summary pattern (`NN passed`, `NN failed`) means the
  run has reached its final summary block — but Playwright prints failed
  and passed counts as **separate lines**, e.g. a `2 failed` line followed
  by `44 passed (45s)` a moment later. The matched line's text alone is not
  the full result: don't push on the first match. Instead, re-read the log
  (`tail -5 <log>`, or the `grep -c '✓'/'✘'` counts from Tier 2a) to get
  both tallies, and only treat the run as actually finished once you see
  the line carrying the duration (`... passed (Xs)`) — that one is always
  last. Then call `PushNotification` with a concise result, e.g.
  `"PW run (sportsbook): 46 passed, 2 failed"`, and stop the watch
  (`TaskStop`, or let the underlying command exit on its own if it naturally
  ends after the summary line appears).

## Notes

- `PushNotification` already skips itself when the user is actively in this
  session — no need to check that yourself.
- Don't notify on routine progress. Failures-in-progress and the final
  result are the only push-worthy events.
- The log path is keyed by `basename "$PWD"`, so concurrent runs in different
  repos don't collide on the same file.
