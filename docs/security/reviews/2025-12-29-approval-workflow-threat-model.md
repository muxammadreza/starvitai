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

---

# Threat model: de-identified pipeline scaffold (2025-12-29)

## Dataflow summary
Actors: backend service (stub), developer/test runner.  
Boundaries: PHI zone (Medplum) → De-ID transformer → De-ID analytics sink (proposal).  
Stores: none in stub; proposed BigQuery dataset for de-ID outputs.

## STRIDE
- Spoofing: non-synthetic input injected into stub.
  - Mitigation: `source_kind` allowlist; env guardrails; tests.
- Tampering: altering run metadata or output records.
  - Mitigation: versioned output + run_id lineage; future signed run metadata.
- Repudiation: inability to trace output to code/policy.
  - Mitigation: `transform_version` + `policy_version` + `run_id`.
- Information disclosure: PHI included in logs or de-ID output.
  - Mitigation: allowlist-only transform; no PHI in logging; policy review before prod IO.
- DoS: large synthetic input in dev/test.
  - Mitigation: test fixtures only; production runner to enforce quotas.
- Elevation of privilege: non-authorized service runs export.
  - Mitigation: stub blocked outside dev/test/local; production RBAC and access policies required.

## Privacy (LINDDUN)
- Linkability: stable patient_key across datasets.
  - Mitigation: rotation strategy required before production; document acceptable linkage.
- Identifiability: residual quasi-identifiers in outputs.
  - Mitigation: policy tags + DLP review before export.

## Top risks + tests
1) Stub runs in prod/staging → guardrail tests and CI checks.
2) PHI fields emitted → schema/field assertion tests.
