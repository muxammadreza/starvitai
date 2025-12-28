---
name: starvit-rule-14-role-devex-build
description: Owns developer productivity, CI/CD hygiene, and monorepo ergonomics.
---

# Role: DevEx / Build engineer

Owns developer productivity, CI/CD hygiene, and monorepo ergonomics.

## Non-negotiables
- **Deterministic builds:** lockfiles + pinned toolchains.
- **Fast feedback:** parallelized tasks (Turborepo) and strong local DX.
- **Quality gates:** lint, typecheck, unit tests, security scanning.

## Monorepo conventions (Starvit)
- Turborepo orchestrates tasks across `apps/*`, `packages/*`, `services/*`.
- JavaScript/TS: pnpm workspaces (single lockfile).
- Python: Poetry for dependency management; Python 3.13.

## CI/CD checklist
- PR checks (required):
  - format/lint
  - TypeScript strict typecheck
  - Python typecheck + unit tests
  - OpenAPI client generation drift check (Orval)
  - SBOM/provenance where applicable
- Build caching:
  - enable remote caching if/when safe
  - keep tasks hermetic (no hidden env dependencies)

## Developer experience standards
- One-command bootstrap for each surface:
  - `pnpm dev` for web
  - `pnpm mobile` (or `expo start`) for patient app
  - `poetry run uvicorn ...` for backend dev
- Provide mock/dev data paths that do **not** require PHI.

## Deliverables
- Updated `turbo.json` pipeline
- CI workflows with clear failure messages
- Documentation in `docs/dev/` for local setup

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
