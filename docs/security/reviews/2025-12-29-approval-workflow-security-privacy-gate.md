# Security/Privacy Gate: clinician approval workflow (2025-12-29)

## Change summary
Introduce versioned PlanDefinition resources with approval-required steps, create clinician approval Tasks, and record decisions via Task status transitions + Provenance + AuditEvent.

## 1) Data classification
- PHI: Task references patient, decision rationale, provenance signatures.
- PlanDefinition contains no PHI but is stored in Medplum.
- AuditEvent contains references + actor metadata; no PHI payloads.

## 2) Boundary enforcement
- PHI remains in Medplum (FHIR Task/Provenance/AuditEvent).
- No cross-zone data movement introduced.

## 3) De-identification
- Not applicable in this change (no export or analytics flow).

## 4) Telemetry
- Request IDs are opaque.
- No PHI added to logs/traces.

## 5) Retention
- Retention governed by Medplum configuration.

## Decision
Approve with mitigations:
- Ensure Task `for` references are patient-scoped and AccessPolicies enforce clinician compartment access.
- Confirm audit events are emitted for proposal creation + decision transitions (tests added).
