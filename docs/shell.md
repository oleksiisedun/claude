# Shell script conventions

### Script basics

- **Shebang**: `#!/usr/bin/env bash` by default; POSIX `#!/bin/sh` only when portability is required (then avoid bashisms).
- **Header comment**: one line on what the script does plus its usage — the shell equivalent of the JSDoc rule.
- **Strict mode**: `set -euo pipefail` near the top.
- Quote every expansion (`"$var"`, `"${arr[@]}"`), use `[[ ]]` over `[ ]`, declare function variables `local`.
- Clean up with `trap ... EXIT`; create temp files with `mktemp`, never fixed `/tmp` names.
- Don't parse `ls` output; use globs or `find -print0` with `read -d ''`.

### Guardrails

- **Lint**: `shellcheck`. **Format**: `shfmt -d` (check) / `shfmt -w` (fix).
- If the project has no aggregate check, suggest one (`make check` or a `scripts/check.sh`) running both — suggest it, don't add it unprompted. Document it in the project's CLAUDE.md.
