---
name: starvit-rule-02-engineering-standards
description: Architecture decisions MUST be written as ADRs for any cross-cutting change.
---

# 02_engineering_standards

- Architecture decisions MUST be written as ADRs for any cross-cutting change.
- Testing strategy MUST follow the test pyramid: more unit tests than integration; integration more than end-to-end.
- Reliability MUST be driven by SLOs and golden signals (latency/traffic/errors/saturation).
- Delivery MUST track DORA metrics (lead time, deployment frequency, change fail %, time to restore).
- Supply chain:
  - Produce SBOM (SPDX) for releases.
  - Aim for SLSA-aligned provenance for builds.
- Observability MUST prefer OpenTelemetry-compatible instrumentation and structured logs.
- ML governance:
  - Datasets documented (Datasheets); models documented (Model Cards).
  - Risk management aligned to NIST AI RMF (Govern/Map/Measure/Manage).
- Engineering discipline:
  - Prefer small, reversible PRs. Every PR includes verification evidence.
  - No new dependency without a justification (what it replaces, why needed, maintenance risk).
  - Python discipline (backend):
    - Use `ruff` for formatting/linting and keep a green type check (pyright/mypy).
    - Keep dependencies pinned via Poetry lock; no unpinned transitive surprises.
    - Run dependency auditing in CI where configured (e.g., pip-audit).


---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
