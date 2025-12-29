# Security/Privacy Gate: AuditEvent logging (2025-12-29)

## Change summary
Introduce application-level AuditEvent emission for PHI write paths (measurements + clinician approval). Add request ID correlation and derived-metric provenance extensions.

## 1) Data classification
- PHI: Observations (glucose/ketones/weight/GKI), Task status, Provenance metadata.
- AuditEvent contains references + actor metadata; no PHI payloads.

## 2) Boundary enforcement
- PHI remains in Medplum (FHIR store).
- No cross-zone data movement introduced.

## 3) De-identification
- Not applicable (PHI path only). No new de-ID flow.

## 4) Telemetry
- Request IDs are opaque.
- No PHI added to logs/traces.

## 5) Retention
- AuditEvent retention is governed by Medplum configuration (verify in ops).

## Decision
Approve with mitigations:
- Ensure request IDs are opaque and not derived from PHI.
- Add explicit tests for AuditEvent creation on write paths (done).

