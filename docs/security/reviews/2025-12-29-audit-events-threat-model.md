# Threat model: AuditEvent logging (2025-12-29)

## Dataflow summary
Actors: patient, clinician, backend service.
Boundaries: API → Medplum (FHIR store).
Stores: Medplum Observation/Task/Provenance/AuditEvent.

## STRIDE
- Spoofing: forged actor identity in AuditEvent.
  - Mitigation: audit events emitted server-side using authenticated `UserContext`.
- Tampering: attacker modifies AuditEvent/Provenance.
  - Mitigation: Medplum access controls; backend service writes only with valid token.
- Repudiation: actor denies action.
  - Mitigation: AuditEvent includes actor identity + request ID.
- Information disclosure: AuditEvent leaks PHI.
  - Mitigation: audit payload contains references only; no PHI in logs.
- DoS: repeated audit writes degrade FHIR store.
  - Mitigation: audit writes follow existing write paths; monitor latency.
- Elevation of privilege: unauthorized writes to AuditEvent.
  - Mitigation: server-side creation only; role-based access enforced.

## Privacy (LINDDUN)
- Linkability/identifiability: request IDs could be linked to PHI if non-opaque.
  - Mitigation: request IDs are UUIDs or provided by caller; do not encode PHI.

## Top risks + tests
1) Missing AuditEvent on write path → add tests per endpoint.
2) Actor mismatch → include actor reference/identifier in tests.

