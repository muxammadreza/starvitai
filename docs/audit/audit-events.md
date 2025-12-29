# AuditEvent logging spec (MVP)

## Purpose
Provide an auditable, FHIR-native trail for write actions (and high-risk reads) with clear actor, action, target references, and request correlation.

## System of record
- **PHI audit trail**: Medplum `AuditEvent` (FHIR R4).
- **Operational audit trail (non‑PHI)**: Starvit logs/metrics.

## When to emit
- **Always** for write actions that create or update PHI resources (Observation, Task, Provenance, etc.).
- **High‑risk reads** (e.g., clinician access to patient records, bulk export) must emit `AuditEvent` with action `R`.

MVP coverage:
- Create measurement (Observations + Provenance)
- Update measurement (Observations + Provenance)
- Clinician approval decision (Task + Provenance)

## Required fields
Each AuditEvent must include:
- `action`: one of `C`, `U`, `R`, `D`, `E`
- `recorded`: UTC timestamp
- `agent`: actor (requestor) with role and reference/identifier
- `source.observer`: system identifier (`starvit-api`)
- `entity.what`: references to all target resources touched
- `extension`: request correlation ID

## Request correlation
Store the backend request ID in a FHIR extension:
- `url`: `urn:starvit:audit:request-id`
- `valueString`: opaque request ID (from middleware)

## Subtypes
Use a Starvit subtype to clarify intent:
- `measurement-create`
- `measurement-update`
- `clinician-approval-approve`
- `clinician-approval-reject`

## Actor mapping
- `agent.who.reference` → `UserContext.profile` (e.g., `Patient/{id}`, `Practitioner/{id}`)
- If profile is absent, use `agent.who.identifier` with:
  - `system`: `urn:starvit:user-sub`
  - `value`: JWT `sub`
- `agent.role.coding.system`: `urn:starvit:role`
- `agent.role.coding.code`: `patient`, `clinician`, `research`, `backend_service`

## Examples (schematic)
```json
{
  "resourceType": "AuditEvent",
  "type": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/audit-event-type", "code": "rest"}]},
  "subtype": [{"coding": [{"system": "urn:starvit:audit-subtype", "code": "measurement-create"}]}],
  "action": "C",
  "recorded": "2025-12-29T20:05:00Z",
  "agent": [{"requestor": true, "who": {"reference": "Patient/p123"}, "role": [{"coding": [{"system": "urn:starvit:role", "code": "patient"}]}]}],
  "source": {"observer": {"identifier": {"system": "urn:starvit:system", "value": "starvit-api"}}},
  "entity": [{"what": {"reference": "Observation/obs1"}}, {"what": {"reference": "Provenance/prov1"}}],
  "extension": [{"url": "urn:starvit:audit:request-id", "valueString": "req-123"}]
}
```

## Provenance requirements (derived metrics)
When creating derived metrics (e.g., GKI), the associated `Provenance` **must include**:
- Input Observation IDs (`entity.role = source`)
- Transform/version identifier (`urn:starvit:provenance:transform-version`)
- Timestamp (`recorded`)

## Testing requirements
- Unit/integration tests must assert AuditEvent creation for each MVP write path.
- Tests must confirm the AuditEvent includes a request ID extension and target references.

