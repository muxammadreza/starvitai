---
trigger: always_on
---

# Starvit non-negotiables (project boundary)

These constraints override any generic software engineering preference.

## Clinical + safety
- **No autonomous medical decisions.** Agents may propose; a clinician must approve, and the approval is logged.
- **Patient safety wins over velocity.** If evidence is unclear, the output must explicitly say so.

## Data boundaries (PHI vs de-identified)
- **PHI boundary is sacred.** PHI stays in the **Medplum FHIR R4 store** (system of record) and any explicitly-designated controlled PHI storage.
- **Derived metrics are still PHI.** Example: **GKI** stored as an `Observation` is PHI and must remain in the PHI zone.
- **Research/ML uses de-identified data only.** De-identify before leaving the PHI zone; enforce the boundary at the API layer.
- **No direct TigerGraph access from any UI.** All graph access goes through allowlisted Research API endpoints.

## Architecture
- **One backend for MVP (modular monolith).** Multiple UIs are fine; multiple independent backends are not.
- **Every recommendation is auditable.** Inputs → transforms → outputs → model + feature versions → clinician decision.

## Platform posture
- **Do not reinvent compliance plumbing.** Prefer using Medplum capabilities for:
  - FHIR storage + access controls
  - OAuth2 / SMART-on-FHIR auth
  - audit logging (FHIR `AuditEvent`)
  - subscriptions + bots for server-side automations

## Environment note
- Current dev/test Medplum endpoints:
  - API: https://api.medplum.starvit.ca/
  - App: https://app.medplum.starvit.ca/

## Safety note (legal/compliance)
- Self-hosted Medplum on a VPS is acceptable for **development with synthetic/test data only**.
- Treat production PHI hosting as a separate, explicitly approved workstream with a formal security review and Canadian jurisdiction analysis.
