---
name: starvit-wf-backend-fhir-resource-change
description: Add/change a FHIR resource mapping or adapter operation
---

# Add/change a FHIR resource mapping or adapter operation

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

