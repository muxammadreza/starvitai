---
description: Add a new operation to the Healthcare API FHIR adapter
---

# Add a Healthcare API FHIR adapter operation

## Inputs
- operation type: read | search | write
- required FHIR resources and fields
- PHI scope: what is allowed to flow, where it is stored

## Steps
1) **Contract first**
   - define request/response schema and error model
   - specify audit event fields (who/what/when/why)
2) **Permissions and boundary**
   - define minimal IAM permissions for the service account
   - ensure no cross-zone leakage (PHI must not reach de-identified analytics)
3) **Implement adapter function**
   - strict input validation
   - deterministic timeouts + retries
   - propagate trace context
4) **Logging + audit**
   - structured logs, scrub/avoid PHI
   - generate an auditable event for each access
5) **Tests**
   - unit tests for validators/mappers
   - integration tests against sandbox/mock
6) **Docs**
   - update OpenAPI
   - update `docs/backend/fhir.md` (or create if missing)

## Output
- adapter operation + tests + docs
- updated contract and generated clients where applicable
