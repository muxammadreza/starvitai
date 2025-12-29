# Threat model: clinician approval workflow (2025-12-29)

## Dataflow summary
Actors: clinician, backend service.
Boundaries: API → Medplum (FHIR store).
Stores: PlanDefinition, Task, Provenance, AuditEvent.

## STRIDE
- Spoofing: forged clinician identity on decision.
  - Mitigation: decisions only emitted server-side using authenticated `UserContext`.
- Tampering: unauthorized Task status updates.
  - Mitigation: RBAC + compartment policies; server-side status transition gate.
- Repudiation: clinician denies decision.
  - Mitigation: Provenance signature + AuditEvent with request ID.
- Information disclosure: recommendations/rationales leak to non-clinician actors.
  - Mitigation: AccessPolicies restrict Task/Provenance access to clinician/patient scopes only.
- DoS: repeated propose/approve calls.
  - Mitigation: rate limiting on clinician endpoints (future); monitor Task creation volume.
- Elevation of privilege: non-clinician creates/approves Task.
  - Mitigation: role checks on endpoints.

## Privacy (LINDDUN)
- Linkability/identifiability: rationale text could include PHI.
  - Mitigation: clinician-entered rationale restricted to clinician view; avoid free-text reuse in research/export paths.

## Top risks + tests
1) Task approved without clinician role → endpoint RBAC tests.
2) Task status updated twice (replay) → status conflict check.
