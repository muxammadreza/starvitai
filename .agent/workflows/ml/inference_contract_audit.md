---
description: Audit the inference contract (inputs → outputs → provenance) for serving
---

Use this before enabling or changing any model serving path.

1) Input contract:
   - schema, types, units
   - required vs optional
   - missingness behavior
2) Feature provenance:
   - feature set version, dataset snapshot, embedding version
   - point-in-time correctness guarantees
3) Output contract (required fields):
   - prediction + units
   - uncertainty/confidence
   - model version + feature version
   - rationale summary
   - clinician-approval-required flag
4) Logging:
   - structured logs with correlation ID
   - no sensitive payloads (no PHI)
   - audit log entry for each inference event
5) Backward compatibility:
   - old clients must keep working or version the endpoint

Deliverables:
- updated OpenAPI schema (if API)
- tests for schema and provenance output
- a short runbook for rollback
