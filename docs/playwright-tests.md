# Playwright tests (E2E)

Playwright covers UI flows; logic-level tests belong in unit tests (see [unit-tests.md](unit-tests.md)). For selector naming, see [data-testid.md](data-testid.md).

In projects that use Playwright:

After writing Playwright test code, run the test without asking.

When asked to fix a test, treat it as already broken — do not run it first. To understand the current UI state, use browser tools (take a screenshot, capture a DOM snapshot, or read the relevant component source code). Fix the test based on what you observe. If none of those approaches are sufficient to diagnose the issue, run the test once to get the error and trace instead of asking the user for the report.
