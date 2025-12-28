# AccessPolicy artifacts

Store Medplum AccessPolicy JSON examples and templates here.

Guidelines:
- Never include PHI in policy examples.
- Prefer parameterized templates for patient/org scoping.
- Keep an accompanying test matrix in the PR description.

## Templates
Templates live under `templates/` and are intended to be applied via the Medplum MCP server.

- `templates/policy.patient_portal.template.json`: patient self-access based on `%profile`.
- `templates/policy.clinician_patient_scoped.template.json`: clinician access scoped by one or more `%patient` parameters set on ProjectMembership.
- `templates/policy.backend_service.template.json`: machine-to-machine backend policy (resource-type allowlist + write constraints).

## Important Medplum constraints
- AccessPolicy `criteria` only supports `:not` and `:missing` modifiers.
- Chained searches are not allowed in AccessPolicy criteria.
- Avoid deprecated fields such as `readonly` and `resource.compartment`.
