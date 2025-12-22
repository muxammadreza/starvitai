# FHIR integration (GCP Healthcare API)

## System of record
The PHI system of record is the GCP Healthcare API FHIR store (FHIR R4).

## Integration principles
- All PHI read/write flows through a single integration module (adapter).
- Never copy PHI into logs, analytics stores, caches, or message queues.
- Prefer **idempotent** operations.

## Patterns
- For multi-resource operations, prefer a FHIR transaction/batch bundle.
- Use conditional writes or optimistic concurrency (ETag / versionId) when appropriate.
- Use FHIR `Provenance` or equivalent for application-level audit trails when the action affects clinical workflows.

## Audit-friendly headers
When adding custom headers for troubleshooting, never include PHI. Only include correlation metadata.

## Validation
- Validate units, code systems, and terminologies for Observations.
- Where feasible, validate resources against profiles.
