# Playwright tests (E2E only)

E2E only — no other test frameworks in use. For selector naming, see [data-testid.md](data-testid.md).

In projects that use Playwright:

After finishing Playwright test code, always ask the user if they want to actually run the test before proceeding.

When asked to fix a test, treat it as already broken — do not run it first. To understand the current UI state, use browser tools (take a screenshot, capture a DOM snapshot, or read the relevant component source code). Fix the test based on what you observe. Only ask the user for the test report if none of those approaches are sufficient to diagnose the issue.
