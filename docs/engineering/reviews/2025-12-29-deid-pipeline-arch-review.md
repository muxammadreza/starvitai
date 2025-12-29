# Architecture review: de-identified pipeline scaffold (2025-12-29)

## Inputs
- Design docs: `docs/deid/boundary-contract.md`, `docs/data/deid-dataset-contract.md`, `docs/data/deid-provenance-model.md`
- Components: Medplum (PHI), De-ID transformer (stub), BigQuery analytics sink (proposal)

## Review axes
1) Boundaries and data zones
- PHI remains in Medplum; stub does not connect to Medplum.
- Explicit guardrails to prevent prod/staging execution.

2) Interfaces and versioning
- Contract defined for `analytics.deid_observations` and `analytics.deid_run_metadata`.
- Version fields (`transform_version`, `policy_version`) included for lineage.

3) Failure modes and resilience
- Stub is in-memory; no retries/timeouts yet.
- Future production runner should add idempotent run IDs and retry safety.

4) Security posture
- Synthetic-only input enforced.
- Logging expectations explicitly forbid PHI.

5) Operability
- Run metadata model defined; runbooks still required for production.

6) Complexity and maintainability
- Stub is modular and isolated under `modules/deid`.

## Top risks + mitigations
- Risk: accidental prod execution.
  - Mitigation: `APP_ENV` allowlist + `STARVIT_MODE=stub` requirement + tests.
- Risk: silent schema drift when moving to production.
  - Mitigation: contract docs + versioned transforms.

## Recommended refactors (future)
- Add explicit de-id config registry and policy tag mapping.
- Implement pipeline orchestration with retries and audit trail.
