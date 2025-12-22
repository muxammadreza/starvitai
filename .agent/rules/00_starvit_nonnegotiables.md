---
trigger: always_on
---

# Starvit non-negotiables (project boundary)

These constraints override any generic software engineering preference.

## Clinical + safety
- **No autonomous medical decisions.** Agents may propose; a clinician must approve, and the approval is logged.
- **Patient safety wins over velocity.** If evidence is unclear, the output must explicitly say so.

## Data boundaries (PHI vs de-identified)
- **PHI boundary is sacred.** PHI stays in **GCP Healthcare API (FHIR R4)** and controlled storage.
- **Research/ML uses de-identified data only.** De-identify via Cloud DLP and enforce the boundary at the API layer.
- **No direct TigerGraph access from any UI.** All graph access goes through allowlisted Research API endpoints.

## Architecture
- **One backend for MVP (modular monolith).** Multiple UIs are fine; multiple independent backends are not.
- **Every recommendation is auditable.** Inputs → transforms → outputs → model + feature versions → clinician decision.

## Platform choices
- The platform is Google Cloud–native.