# FHIR integration (Medplum)

## System of record
The PHI system of record is the **Medplum FHIR R4 server**.

Dev/test endpoints (self-hosted):
- API base: https://api.medplum.starvit.ca/
- FHIR base (expected): https://api.medplum.starvit.ca/fhir/R4
- UI: https://app.medplum.starvit.ca/

## Auth patterns
### Human users (clinicians/patients)
- OAuth2 Authorization Code flow (SMART-on-FHIR semantics). Prefer using Medplum React components/SDK.
- ClientApplication: define Redirect URI(s) and assign a least-privilege AccessPolicy.

### Machine-to-machine (Starvit backend workers)
- OAuth2 Client Credentials flow using a dedicated ClientApplication.
- Assign a dedicated AccessPolicy limiting data access strictly to the minimum resources/compartments required.

## Integration principles (non-negotiable)
- All PHI read/write flows through a single integration module (adapter).
- Never copy PHI into logs, analytics stores, caches, or message queues.
- Prefer idempotent operations; use explicit request IDs and correlation IDs.

## Recommended FHIR patterns
- Multi-resource operations: use FHIR `Bundle` transactions when atomicity is required.
- Optimistic concurrency: use ETag / `meta.versionId` checks for updates.
- Clinical workflow artifacts:
  - recommendations pending review: `Task` (status = requested/ready)
  - clinician decision + rationale: `Provenance` + `Task.status` transition
  - patient-facing messages: `Communication`

## Attachments
- Store files in FHIR `Binary` or resource `attachment` fields.
- Ensure access is gated (AccessPolicy/compartments); do not expose direct URLs without auth.

## Audit and provenance
- Rely on Medplum `AuditEvent` for access/change audit.
- Add `Provenance` for application-generated clinical actions (recommendations, protocol changes).

## Validation
- Validate units, code systems, and terminologies for Observations.
- Treat derived metrics (e.g., GKI) as PHI and store them as Observations in the PHI zone.
