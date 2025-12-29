# Clinical safety review: measurement ingestion + derived GKI

Date: 2025-12-29
Reviewer role: Clinical informatics & safety
Scope: patient-submitted glucose/ketone/weight measurements; server-side GKI computation; patient endpoints.

## Required fixes (blocking)
- None.

## Nice-to-haves (non-blocking)
- Add explicit clinician-facing labels in UI that GKI is a monitoring metric and not a treatment target.
- Add cachexia risk flags in clinician surfaces when available.

## Safety sign-off checklist
1) Clinician supervision
- Feature is monitoring-only; no autonomous recommendations: ✅

2) Safety gates
- No bypass of clinician approvals (no approvals introduced): ✅

3) Unit correctness
- Glucose + ketones enforced in mmol/L; GKI computed server-side: ✅

4) Host fragility safeguards
- No UX to "optimize GKI" introduced: ✅ (UI not in scope)

5) Adverse event escalation
- No escalation UX changed: N/A

6) Auditability
- Provenance recorded for derived metric; Medplum AuditEvent expected: ✅

Reviewer: Clinical informatics & safety (Codex)
Version identifiers: API measurement endpoints, 2025-12-29
