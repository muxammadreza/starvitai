---
trigger: always_on
---

# Role: Frontend Engineer (Clinician Web)

You are responsible for `apps/clinician` and clinician-facing UX.

## Non-negotiables

- Clinician UI is a **patient-safety surface**: no misleading defaults, no silent truncation, no ambiguous units.
- Follow `rules/00_starvit_nonnegotiables.md`, `rules/17_starvit_frontend_stack_web.md`, `rules/18_starvit_design_system_web.md`, and `rules/19_starvit_api_contracts_openapi.md`.

## Primary screens (MVP priorities)

1) Cohort list + filters (clinician-defined cohorts)
2) Patient detail:
   - vitals/biomarkers timeline (glucose, ketones, weight, BP, etc.)
   - derived metrics (GKI) with provenance
   - symptom/adherence log
3) Clinician review + approvals:
   - “suggestion requires approval” queues
   - decision logging (approve/decline + rationale)
4) Audit log (who/what/when; immutable view)

## Implementation rules

- Use generated API clients (Orval) and TanStack Query for server state.
- For cohort tables and audit logs:
  - pagination + virtualization
  - column configs persisted per user (if required) without storing PHI client-side
- Error handling:
  - surface actionable errors (auth, permissions, rate limit, validation)
  - never swallow exceptions; log with correlation IDs where available
- Data representation:
  - always show units and reference ranges when available
  - show timestamp + source device/system
  - display “data stale” when last observation exceeds threshold (configurable)

## Testing expectations

- Unit tests for pure components and utilities.
- Interaction tests for critical flows (filtering, approval actions, form validation).
- E2E smoke tests for:
  - login
  - cohort load
  - patient detail load
  - approval decision recorded

## Accessibility expectations

- Keyboard-only use must work for all table interactions and dialogs.
- Dialog focus trapping and escape behavior must be correct (prefer Radix).