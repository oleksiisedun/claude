# Python conventions

Static checks only — no new unit-test framework (see the E2E-only rule in [CLAUDE.md](../CLAUDE.md)).

### Tooling

- **Project setup**: `uv` with a `pyproject.toml` (set `requires-python`) and a committed `uv.lock`; no `requirements.txt` for new projects. Run things via `uv run`.
- **Single-file scripts**: declare dependencies inline with PEP 723 (`# /// script` block) and run with `uv run script.py` — no project scaffolding needed.
- **Lint + format**: `ruff check` and `ruff format`. Ruff's default rule set is tiny, so in `pyproject.toml` enable `[tool.ruff.lint] select = ["E", "F", "I", "B", "UP", "SIM"]` (pycodestyle, pyflakes, import sorting, bugbear, pyupgrade, simplify).
- **Types**: `pyright` in its default `standard` mode (`strict` is too noisy to adopt by default). Use `mypy` only if the project already does. Don't switch to `ty` until it leaves beta.
- **One entry point**: if the project has no aggregate check, suggest one (`make check` or a `uv run` script) running `ruff check`, `ruff format --check` and the type checker — suggest it, don't add it unprompted. Document it in the project's CLAUDE.md.

### Style

- Type hints on every function signature.
- Docstrings follow the TypeScript rule: add one only when the signature leaves a real question (intent, invariant, gotcha). Never restate types in the docstring.
- `pathlib` over `os.path`, f-strings over `%`/`.format()`.
- Guard script entry points with `if __name__ == "__main__":`.
- No bare `except:` (catch the narrowest exception), no mutable default arguments.
- Keep docstrings in sync when a signature or behavior changes — same rule as JSDoc.
