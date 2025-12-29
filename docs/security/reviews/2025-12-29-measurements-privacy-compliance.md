# Privacy/compliance review: patient measurements (FHIR Observations)

Date: 2025-12-29
Reviewer role: Privacy + compliance
Scope: patient-submitted glucose/ketone/weight measurements; derived GKI; Medplum FHIR storage.

## Data inventory
- Collected fields: patient ID, measuredAt timestamp, glucose (mmol/L), ketones (mmol/L), optional weight (kg), derived GKI.
- Storage location: Medplum FHIR R4 (Observation + Provenance).
- Access: Patient role (self), clinician role (patient compartment), backend service (service policy).

## Boundary enforcement
- PHI remains in Medplum (Observations + Provenance).
- No analytics/de-ID export in this change.
- Research surfaces remain blocked from PHI endpoints.

## De-identification
- Not applicable in this change (no cross-zone movement).
- If exported later, must pass DLP de-identification gate.

## Telemetry
- No PHI logged; responses return IDs only.
- Correlation IDs only (no measurement values) in logs.

## Retention
- Medplum default retention applies; derived metrics are PHI and must follow the same retention/deletion policy as source Observations.

## Decision
Approved with mitigations:
- Ensure production logging does not include request bodies for measurement endpoints.
- Confirm AccessPolicies for patient/clinician include Observation read/write in appropriate compartments.
