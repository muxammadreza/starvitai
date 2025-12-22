---
trigger: always_on
---

# Turbo Mode Safety (Antigravity)

Turbo mode can auto-run terminal steps. In Starvit, turbo is **restricted**.

## Allowed turbo commands (examples)

Read-only or non-destructive commands only, such as:
- `git status`, `git diff`, `git log`
- `ls`, `pwd`, `find` (within workspace), `rg`
- `pnpm -v`, `python --version`
- `pytest -q` (read-only test execution)
- `pnpm lint`, `pnpm test` (no installs unless already locked)

## Forbidden in turbo

- Any delete/overwrite: `rm`, `del`, `rmdir`, `unlink`, `mv`/`ren` across dirs
- Anything with elevated privileges: `sudo`, `runas`
- Infra changes: `terraform apply`, `gcloud ... delete`, `kubectl delete`
- Network install/execution: `curl | bash`, `pip install`, `pnpm add`, etc.
- Anything that targets paths outside the workspace (home dir, mounted drives).

## Policy

- Do not use `// turbo-all`.
- If a workflow includes terminal steps, default to *non-turbo* and request review for any state-changing command.
