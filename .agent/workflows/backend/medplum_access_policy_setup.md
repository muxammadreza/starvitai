---
description: Configure Medplum Projects, ProjectMemberships, and AccessPolicies (tenant and patient scoping)
---

## Goal
Establish least-privilege access controls in Medplum so that:
- each patient can see only their own compartment
- clinicians see only the patients they are assigned (or within an allowed org)
- backend/bots have scoped programmatic access

**Implementation rule:** All Medplum admin/config changes in this workflow MUST be performed via the configured **Medplum MCP server** (see `.agent/rules/35_medplum_mcp_mandate.md`).

## Steps
1) Project boundaries
   - Create separate Medplum Projects per environment (`dev`, `stage`, `prod`).
   - (Optional multi-tenant) Decide: one Project per customer organization (hard isolation) vs one Project with compartment-based separation.

2) Define AccessPolicies (FHIR `AccessPolicy` resources)
   - Start with role-based policies:
     - `PatientPortalPolicy` (patient-only compartment access)
     - `ClinicianPolicy` (read/write limited clinical resource set; broad search constrained)
     - `BackendServicePolicy` (only the resource types required for computations and suggestions)
   - Use **criteria-based restrictions** and **compartment scoping**:
     - Patient self-access: use the built-in `%profile` variable (patient profile reference).
       - Example: `Patient?_id=%profile.id`
       - Example: `Observation?_compartment=%profile`
     - Clinician scoping: prefer parameterized criteria using membership parameters (e.g., `%org`) or relationships explicitly modeled in FHIR (e.g., `Patient?general-practitioner=%profile`).
   - Use `resource.interaction` allowlists (do not use the deprecated `readonly` field).
   - Note: AccessPolicy criteria have practical limits (e.g., avoid chained searches and advanced modifiers); keep policies simple and testable.

3) Bind policies to users/apps via ProjectMembership
   - Practitioner/Patient/RelatedPerson profiles for people.
   - ClientApplication and Bot profiles for programmatic identities.
   - Attach AccessPolicy (or parameterized policy instances) to ProjectMembership.

4) Validate Binary rules
   - For `Binary`, enforce `securityContext` (cannot be controlled via criteria search).

5) Test
   - Use a test matrix:
     - patient token cannot read other patient resources
     - clinician cannot access non-assigned patient compartments
     - backend token can perform only required operations
   - Ensure denial is HTTP 403 (policy enforcement).

## Deliverables
- AccessPolicy JSON resources (checked into repo under `docs/security/access-policies/`)
- Test plan + automated integration tests
- ProjectMembership provisioning runbook
