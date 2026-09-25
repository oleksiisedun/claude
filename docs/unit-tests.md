# Unit tests

The always-on rules (use the existing setup, run tests without asking — the ask-first rule is Playwright-only — never add a framework unprompted) live in [CLAUDE.md](../CLAUDE.md). This doc covers where tests are worth writing. Framework picks per language: [javascript.md](javascript.md), [python.md](python.md), [shell.md](shell.md). Unit tests cover logic; UI flows belong in Playwright: [playwright-tests.md](playwright-tests.md).

## Where tests pay off

While working in a project, when you spot untested code in these categories, say so — name the function and the bug a test would catch:

- Pure logic with branches: parsers, formatters, validators, date/time/money math, state machines, data transforms.
- Boundary-heavy code: empty/null input, off-by-one, timezones, encodings, rounding.
- Code that is slow or awkward to verify any other way (needs auth, network, or a full UI flow to reach).
- Code about to be refactored — write characterization tests first so the refactor has a safety net.
- Anything that has already broken once. For a bug fix, write the failing test first when practical.

## Skip tests that don't earn their keep

Thin glue and wrappers, layout and styling, throwaway scripts, and tests that mock everything and just restate the implementation. A few tests on real logic beat shallow coverage everywhere. Test behavior through the public interface, not private helpers.

## Design for testability

Keep pure logic in functions that take plain values, and confine I/O and runtime APIs (DOM, network, Apps Script's `SpreadsheetApp`/`DriveApp`) to thin wrappers, so the logic runs under the test runner without mocks.

## E2E-only projects

A project with Playwright and no unit runner already has a test setup. Don't suggest adding a unit framework by default — a second runner brings its own config, scripts, CI step and a competing tests directory.

Suggest one only when both hold:
- There is substantial pure logic (parsers, money/date math, state machines) that E2E covers badly — name the function and the bug a unit test would catch.
- It can share the layout cleanly: unit tests in `tests/unit/`, E2E in `tests/e2e/`, one aggregate `test` script. If that can't be done without a mess, skip it.

Never suggest it for thin glue, small UIs, or static sites.
