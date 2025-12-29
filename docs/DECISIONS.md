# Decisions / ADRs

Use Architecture Decision Records (ADRs) for:
- schema changes (FHIR analytics, TigerGraph schema)
- security posture changes
- ML model release changes
- infra/ops changes that affect compliance

Minimum ADR fields:
- Context
- Decision
- Consequences
- Alternatives considered
- Links to PRs and rollout plan

## ADR index
- ADR-0003: BigQuery’s role in Starvit (and how it feeds TigerGraph) — `docs/decisions/ADR-0003-bigquery-role.md`
- ADR-0004: Medplum-authenticated role mapping and backend authz — `docs/decisions/ADR-0004-medplum-authz-role-mapping.md`
- ADR-0005: Measurement Observations and derived metrics mapping — `docs/decisions/ADR-0005-measurement-observation-mapping.md`
