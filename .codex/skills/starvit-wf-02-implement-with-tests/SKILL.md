---
name: starvit-wf-02-implement-with-tests
description: Ship changes that are correct, reviewable, and safe.
---

## Goal
Ship changes that are correct, reviewable, and safe.

## Steps
1) Create/adjust the contract first (schemas/OpenAPI/interfaces) when needed.
2) Add/adjust tests:
   - unit tests for pure logic
   - integration tests for boundaries (DB/FHIR adapters/auth)
   - contract tests for API consumers
3) Implement the smallest working slice.
4) Instrument the new code path (logs/metrics/traces) without PHI.
5) Update docs/runbooks if operability changed.

## Deliverables
- code + tests
- minimal observability
- updated docs if needed

---

**Codex usage notes:**
- Use this workflow skill to execute the step sequence as written.
- Produce the specified deliverables explicitly (plans, ADRs, checklists, etc.).
