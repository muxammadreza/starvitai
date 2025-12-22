---
description: Add/change a FHIR resource mapping or adapter operation
---

## Steps
1) Identify the FHIR resource(s) impacted (Observation, Condition, CarePlan, Consent, etc.).
2) Update adapter mapping:
   - validate field semantics
   - ensure PHI handling is correct
3) Add integration tests:
   - mocked FHIR store or test project
   - permission checks
4) Update analytics extract (if applicable):
   - flattened tables / event streams
5) Update docs:
   - `docs/fhir/*`
   - data contracts

## Output
FHIR adapter change with tests and documentation.
