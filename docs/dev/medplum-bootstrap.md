# Starvit Medplum DEV bootstrap (starvit-dev)

Date: 2025-12-29
Owner: Codex (MCP-only changes)

## Objective
Bootstrap a clean DEV tenant in Medplum for backend MVP development with least-privilege access, test users, and seed data. All admin/config changes were made via Medplum MCP.

## Project
- Project name: starvit-dev
- Project ID: daead41a-9994-4c09-869f-4907ac20b2b5
- Project `superAdmin`: false (confirmed 2025-12-29).

## Medplum endpoints
- API base: https://api.medplum.starvit.ca
- FHIR base: https://api.medplum.starvit.ca/fhir/R4

## Principals and roles
Emails used (dev/test only):
- clinician.admin+dev@example.com (clinician admin)
- patient.test+dev@example.com (patient test)
- researcher.readonly+dev@example.com (researcher read-only)
- backend.service+dev@example.com (backend service account)

### IAM/RBAC matrix (Medplum layer)
| Principal | AccessPolicy | Scope summary |
| --- | --- | --- |
| Clinician admin | ClinicianPolicy | Patients assigned via `general-practitioner=%profile`; Observations/Encounters where clinician is performer/participant. |
| Patient test | PatientPortalPolicy | Own Patient + own compartment Observations/Encounters. |
| Researcher read-only | ResearcherReadOnlyPolicy | Read/search only resources tagged `dev-seed`. |
| Backend service | BackendServicePolicy | Read/search Patient; read/search/create/update Observation + Encounter (broad). |

### ProjectMemberships
- Clinician admin: ProjectMembership/ab2d8f87-aafe-4e70-800d-56b6b951acd9
  - User: User/f39be34f-3f9a-4d67-b56d-fa1d0eb75020
  - Profile: Practitioner/daa3c938-021c-447c-a233-4c1d3fdd17a4
  - AccessPolicy: AccessPolicy/18b8951a-26cf-4deb-a71a-562d54ac0623 (ClinicianPolicy)
- Patient test: ProjectMembership/9a1814bd-ef0e-4514-b16f-d44c82f7136c
  - User: User/53beb0df-d09a-4e92-8d50-90a674fe728f
  - Profile: Patient/4c60514d-f106-43d0-8590-4a219c386a81
  - AccessPolicy: AccessPolicy/2db139c1-0398-442e-adc9-fc2c51dad6ec (PatientPortalPolicy)
- Researcher read-only: ProjectMembership/1bdd0bbb-6c7f-43ef-ae10-a588a480be60
  - User: User/f0888cfb-8e96-488a-9bac-a0e448f3a301
  - Profile: Practitioner/d7a68882-0311-46e1-b4f5-372362f34f27
  - AccessPolicy: AccessPolicy/9bef92df-a988-412d-9bbf-21035c0183c0 (ResearcherReadOnlyPolicy)
- Backend service: ProjectMembership/2101d006-367b-48b2-ac8f-5dfa8d3c6b87
  - User: User/a8882cdd-3b76-479d-b65a-43820cff49fb
  - Profile: Practitioner/906ed490-7ae5-49c3-8eb7-31fc1c259ed0
  - AccessPolicy: AccessPolicy/ec90fd03-bf9d-4eab-bc1f-7f4da73c4ed7 (BackendServicePolicy)

## Access policies (least privilege)
- PatientPortalPolicy (AccessPolicy/2db139c1-0398-442e-adc9-fc2c51dad6ec)
  - Patient: read/search/update self
  - Observation: read/search/create/update in patient compartment
  - Encounter: read/search in patient compartment
- ClinicianPolicy (AccessPolicy/18b8951a-26cf-4deb-a71a-562d54ac0623)
  - Patient: read/search by `general-practitioner=%profile`
  - Observation: read/search/create/update by `performer=%profile`
  - Encounter: read/search/create/update by `participant=%profile`
  - Note: Medplum AccessPolicy criteria do not allow chained search; this is the least-privilege approximation for DEV.
- ResearcherReadOnlyPolicy (AccessPolicy/9bef92df-a988-412d-9bbf-21035c0183c0)
  - Read/search only on DEV seed data tagged `dev-seed`.
- BackendServicePolicy (AccessPolicy/ec90fd03-bf9d-4eab-bc1f-7f4da73c4ed7)
  - Read/search on Patient; read/search/create/update on Observation and Encounter.
  - Note: This is broad (`_id=*`) and should be narrowed when backend requirements are finalized.

## Client application + secrets
- ClientApplication: ClientApplication/9b6b3f87-aab6-4c17-8bef-25d33d323c89 (name: starvit-dev-backend)
- ProjectSecret: STARVIT_DEV_BACKEND_CLIENT_SECRET
  - Value set to placeholder and must be rotated before real use.
  - Do not print or commit real secrets.

## Seed data
All seed data is tagged with `https://api.medplum.starvit.ca/fhir/tags|dev-seed`.

Patients:
- Patient/4c60514d-f106-43d0-8590-4a219c386a81 (Patient One, linked to clinician)
- Patient/39d0a682-6aab-4bf5-94df-d52bc34ddadd (Patient Two, linked to clinician)

Encounters:
- Encounter/4cd2032e-1628-4c3d-a34c-91fc657526a0 (Patient One)
- Encounter/329b4999-8522-4243-929b-1c903336c01b (Patient Two)

## Reproducible templates
Templates live in `docs/dev/medplum-templates/`. Replace placeholders (PROJECT_ID, policy IDs, profile IDs) and apply via MCP `manageResource` create/update.
Example apply (AccessPolicy):
```
manageResource: {"action":"create","resourceType":"AccessPolicy","resource":{...}}
```

## Smoke test (MCP)
Run the following with the MCP tool to validate search/create/update on Patient and Observation.

1) Search for a seeded Patient (admin or clinician context):
```
manageResource: {"action":"search","resourceType":"Patient","searchParams":{"_tag":"https://api.medplum.starvit.ca/fhir/tags|dev-seed"}}
```

2) Create an Observation for Patient One (admin/backend/clinician):
```
manageResource: {
  "action":"create",
  "resourceType":"Observation",
  "resource": {
    "resourceType": "Observation",
    "meta": {"project": "daead41a-9994-4c09-869f-4907ac20b2b5", "tag": [{"system":"https://api.medplum.starvit.ca/fhir/tags","code":"dev-seed"}]},
    "status": "final",
    "code": {"text": "BHB"},
    "subject": {"reference": "Patient/4c60514d-f106-43d0-8590-4a219c386a81"},
    "valueQuantity": {"value": 1.2, "unit": "mmol/L"}
  }
}
```

3) Update that Observation value (admin/backend/clinician):
```
manageResource: {"action":"update","resourceType":"Observation","id":"<OBS_ID>","resource":{...updated valueQuantity...}}
```

### TG2 Verification evidence (performed 2025-12-29)
Executed via MCP (admin client):
- Search Patients by tag `https://api.medplum.starvit.ca/fhir/tags|dev-seed`: 2 results.
- Created Observation: Observation/c9f9dcff-fab9-4eee-a687-ab80daa8776a (BHB 1.2 mmol/L).
- Updated Observation: Observation/c9f9dcff-fab9-4eee-a687-ab80daa8776a (BHB 1.4 mmol/L).
Note: Role-based denial checks (patient/researcher) require user-context tokens and were not executed here.

## IAM/RBAC audit summary
- Principals enumerated: clinician, patient, researcher, backend service.
- Medplum controls: ProjectMembership + AccessPolicy enforced; no admin flags set on memberships.
- Risks:
  - BackendServicePolicy uses `_id=*` broad criteria.
- Mitigations:
  - Keep `dev-seed` tag for research policy.
  - Narrow backend policy when backend endpoints are fixed.

## Security/privacy gate (decision note)
- Data classification: PHI remains in Medplum; dev data is synthetic.
- Access control: AccessPolicies and ProjectMemberships created and scoped; patient access is compartment-based.
- Auditability: Medplum AuditEvent assumed enabled; verify retention settings in ops.
- Logging: No PHI logged or exported by this change.
- Decision: Approved for DEV with mitigations (rotate placeholder secret).

## Threat model (STRIDE + LINDDUN)
Top risks:
- Elevation of privilege via overly broad policies (backend, researcher).
- Information disclosure if seed tags are not enforced.
- Linkability risk for researcher if tags are applied to non-dev data.
Mitigations:
- Enforce dev-seed tags for research policy.
- Add monitoring on access patterns for read-all scopes.
Test cases:
- Researcher attempts to read untagged Patient (expect 403).
- Patient attempts to read another Patient (expect 403).
- Researcher attempts to create Observation (expect 403).

### TG3 Critics (performed 2025-12-29)
- Threat model review complete (no new high-risk paths introduced beyond policy scope).
- Clinical safety review complete; no protocol/decision logic added.

## Clinical safety review
- No protocol logic or clinician recommendations introduced.
- No clinical decisioning pathways modified.
- Safe for DEV bootstrap.

## Release readiness
- Not a production release. No deployment or migration steps required.
- If promoted beyond DEV, re-run security/privacy gate and threat model with real PHI constraints.

## Change log entry
2025-12-29: Bootstrapped `starvit-dev` Medplum tenant with AccessPolicies, ProjectMemberships, client app, project secret placeholder, and seed Patient/Encounter data for dev testing. Mitigations: rotate placeholder secret, tighten backend policy.
