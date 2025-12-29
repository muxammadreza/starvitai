# Data contract: De-identified observations (BigQuery)

Date: 2025-12-29
Owner: Data Platform
Status: Proposal (synthetic-only scaffold)

## Table
- Name: `analytics.deid_observations`
- Owner: Data Platform
- Grain: one record per de-identified Observation
- Primary key: `observation_id`
- Partitioning: `DATE(effective_at)`
- Clustering: `patient_key`, `code`

## Fields
| Field | Type | Semantics | Units |
| --- | --- | --- | --- |
| observation_id | STRING | Source Observation id | - |
| patient_key | STRING | Pseudonymous patient token | - |
| effective_at | TIMESTAMP | Observation effective time | ISO-8601 |
| code_system | STRING | Coding system URI | - |
| code | STRING | Observation code | - |
| value | FLOAT | Observation value | source unit |
| unit | STRING | Unit for value | UCUM when available |
| run_id | STRING | De-ID run identifier | - |
| transform_version | STRING | Transformer version | - |
| policy_version | STRING | De-ID policy version | - |

## Permitted uses
- Cohorting: yes (with policy-tagged access where needed).
- Reporting: yes (de-identified only).
- Training/inference: yes (with governance review).

## Lineage
- Sources: Medplum FHIR Observation (PHI zone).
- Transformations: De-ID transformer (`deid-stub-v0`) with allowlisted field extraction + pseudonymization.
- Configuration: policy version `policy-stub-v0` (placeholder).

## Quality guarantees
- Assertion: no direct identifiers present in output columns.
- Assertion: `patient_key` is derived within transformer boundary.
- SLA: stub only (no production SLA).

## Notes
- This proposal is for synthetic-only scaffolding.
- Production rollout requires formal DLP policy + IAM/RLS review.
