# Backend testing (Starvit)

## Scope
Backend tests must prove:
- correctness of protocol/metric logic
- PHI boundary enforcement
- RBAC authorization and audit logging
- stable API contracts for clients

## Required layers
1) Unit tests
- pure functions: GKI calculations, thresholds, state machine transitions
- input validation utilities

2) Integration tests
- database persistence and migrations
- FHIR adapter operations (mocked or sandbox)
- auth flows and role enforcement

3) Contract tests
- OpenAPI schema is authoritative
- ensure backward compatibility where needed

4) End-to-end smoke (minimal)
- one representative clinician journey via API + minimal UI driver

## CI expectations
- fast unit tests on PR
- integration tests on PR (can be parallelized)
- nightly longer suites (load, regression cohorts)

## Anti-patterns
- flaky tests without ownership
- tests that require PHI data
