# Threat model: measurement endpoints (STRIDE + LINDDUN)

Date: 2025-12-29
Scope: patient measurement submission + retrieval, derived GKI, Medplum FHIR access.

## Dataflow
Actors: patient app, Starvit backend, Medplum FHIR store.
Trust boundaries: client → backend, backend → Medplum.
Data stores: Medplum Observations + Provenance.

## STRIDE risks
- Spoofing: forged patientId in payload.
  - Mitigation: bind patientId to token profile in live mode.
- Tampering: malicious modification of measurement values.
  - Mitigation: authZ checks + audit events + provenance.
- Repudiation: user denies submission.
  - Mitigation: Medplum AuditEvent + Provenance.
- Information disclosure: excessive data returned by GET endpoints.
  - Mitigation: patient-scoped access only, limited response fields.
- DoS: high-frequency submissions.
  - Mitigation: rate limiting at edge (configure per env); monitor error rates.
- Elevation of privilege: patient access to other patients.
  - Mitigation: patientId bound to token profile; AccessPolicy compartment scoping.

## LINDDUN risks
- Linkability/Identifiability: measurement history linked to patient identity.
  - Mitigation: keep PHI in Medplum only; no de-ID export here.
- Detectability/Disclosure: endpoint timing reveals activity.
  - Mitigation: standard error responses; no detailed PHI in errors.

## Top risk test cases
1) POST measurement with mismatched patientId (expect 200 with server-bound patientId or 403).
2) GET recent measurements for other patient (expect 403 or empty depending on policy).
3) Inject non-canonical units (expect 422/400).
