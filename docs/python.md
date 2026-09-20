# Python conventions

### Tooling

- **Project setup**: `uv` with a `pyproject.toml` (set `requires-python`) and a committed `uv.lock`; no `requirements.txt` for new projects. Run things via `uv run`.
- **Single-file scripts**: declare dependencies inline with PEP 723 (`# /// script` block) and run with `uv run script.py` — no project scaffolding needed.
- **Lint + format**: `ruff check` and `ruff format`. Ruff's default rule set is tiny, so in `pyproject.toml` enable `[tool.ruff.lint] select = ["E", "F", "I", "B", "UP", "SIM"]` (pycodestyle, pyflakes, import sorting, bugbear, pyupgrade, simplify).
- **Types**: `pyright` in its default `standard` mode (`strict` is too noisy to adopt by default). Use `mypy` only if the project already does. Don't switch to `ty` until it leaves beta.
- **One entry point**: if the project has no aggregate check, suggest one (`make check` or a `uv run` script) running `ruff check`, `ruff format --check`, the type checker and, if the project has tests, `pytest` — suggest it, don't add it unprompted. Document it in the project's CLAUDE.md.

### Testing

Where tests are worth adding, see [unit-tests.md](unit-tests.md). Use the project's existing runner; when suggesting one for a project that has none, propose `pytest`.

- **Setup**: `uv add --dev pytest`, run with `uv run pytest`. Don't add it unprompted.
- **Layout**: `tests/` mirroring the package, files `test_*.py`, functions `test_<behavior>`.
- **Edge-case tables**: `@pytest.mark.parametrize` rather than loops or copy-pasted tests.
- **Fixtures**: `tmp_path` for filesystem, `monkeypatch` over `unittest.mock` where it suffices.

### Style

- Type hints on every function signature.
- Docstrings follow the TypeScript rule: add one only when the signature leaves a real question (intent, invariant, gotcha). Never restate types in the docstring.
- `pathlib` over `os.path`, f-strings over `%`/`.format()`.
- Guard script entry points with `if __name__ == "__main__":`.
- No bare `except:` (catch the narrowest exception), no mutable default arguments.
- Keep docstrings in sync when a signature or behavior changes — same rule as JSDoc.
