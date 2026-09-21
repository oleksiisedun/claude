# Unit tests

The always-on rules (use the existing setup, run tests without asking, never add a framework unprompted) live in [CLAUDE.md](../CLAUDE.md). This doc covers where tests are worth writing. Framework picks per language: [javascript.md](javascript.md), [python.md](python.md), [shell.md](shell.md). For UI flows use Playwright instead: [playwright-tests.md](playwright-tests.md).

### Where tests pay off

While working in a project, when you spot untested code in these categories, say so — name the function and the bug a test would catch:

- Pure logic with branches: parsers, formatters, validators, date/time/money math, state machines, data transforms.
- Boundary-heavy code: empty/null input, off-by-one, timezones, encodings, rounding.
- Code that is slow or awkward to verify any other way (needs auth, network, or a full UI flow to reach).
- Code about to be refactored — write characterization tests first so the refactor has a safety net.
- Anything that has already broken once. For a bug fix, write the failing test first when practical.

### Skip tests that don't earn their keep

Thin glue and wrappers, layout and styling (Playwright covers UI flows), throwaway scripts, and tests that mock everything and just restate the implementation. A few tests on real logic beat shallow coverage everywhere. Test behavior through the public interface, not private helpers.

### Design for testability

Keep pure logic separate from I/O and runtime APIs (DOM, Apps Script globals, network) so it can be tested without mocks.

### Unit tests vs Playwright

Unit tests cover logic; Playwright covers UI flows. Unit tests are fast and deterministic — run them without asking. The ask-before-running rule applies to Playwright only.

### E2E-only projects

A project with Playwright and no unit runner already has a test setup. Don't suggest adding a unit framework by default — a second runner brings its own config, scripts, CI step and a competing tests directory.

Suggest one only when both hold:
- There is substantial pure logic (parsers, money/date math, state machines) that E2E covers badly — name the function and the bug a unit test would catch.
- It can share the layout cleanly: unit tests in `tests/unit/`, E2E in `tests/e2e/`, one aggregate `test` script. If that can't be done without a mess, skip it.

Never suggest it for thin glue, small UIs, or static sites.
