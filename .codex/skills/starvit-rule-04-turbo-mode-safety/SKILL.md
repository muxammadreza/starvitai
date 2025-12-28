---
name: starvit-rule-04-turbo-mode-safety
description: Turbo mode can auto-run terminal steps. In Starvit, turbo is **restricted**.
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

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
