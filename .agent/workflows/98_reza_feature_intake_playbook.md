---
description: Reza's feature intake playbook for Starvit (end-to-end routing)
---

Use this when you want to add a feature, change logic, or ship a new capability.

Preferred: run `/router` first. This playbook remains useful when you want to manually route without the router.

## 0) One-sentence intent
Write: “I want Starvit to …”

## 1) Classify the change (select all that apply)
- UI/UX surface (mobile, clinician dashboard, research workbench)
- Backend API / protocol engine logic
- PHI ingestion or FHIR resource usage
- Data plane (BigQuery datasets, dbt/Dataform transforms, Dataflow pipelines)
- Graph (TigerGraph schema/queries/embeddings)
- ML/AI (training, evaluation, serving, novelty discovery)
- Security/compliance scope (RBAC, audit logging, retention)

## 2) Route to the right workflows

### A) UI-only
- `workflows/frontend/*` (choose the relevant surface workflow)
- Gate: `workflows/03_security_privacy_gate.md` (sanity check), accessibility workflow

### B) Backend endpoint or domain logic
- `workflows/backend/add_api_endpoint.md` or `workflows/swe/swe_backend_feature_module.md`
- If PHI-adjacent: `workflows/backend/fhir_resource_change.md`
- Gates: `workflows/03_security_privacy_gate.md`, observability workflow

### C) Data plane (BigQuery / transforms / pipelines)
Pick based on what changes:
- New dataset/IAM/policies:
  - `workflows/data/provision_bigquery_datasets_and_iam.md`
  - `workflows/data/bigquery_rls_policy_tags_masking.md` (if needed)
- FHIR → BigQuery movement (research zone):
  - `workflows/data/fhir_to_bigquery_export.md`
  - `workflows/data/data_governance_deid_pipeline.md` (mandatory gate)
- Transformation changes (dbt/Dataform):
  - `workflows/data/dbt_or_dataform_transformation_change.md`
- Streaming pipeline:
  - `workflows/data/dataflow_streaming_pipeline_pubsub_bigquery.md`
- Operational DB (non-PHI):
  - `workflows/data/cloudsql_schema_change.md`
- Always add:
  - `workflows/data/data_quality_checks.md`
  - `workflows/data/define_data_contracts_and_lineage.md`

### D) Graph feature / cohorting / link discovery
- `workflows/graph/design_graph_schema.md`
- `workflows/graph/implement_tigergraph_schema_and_loading.md` (if schema/queries change)
- `workflows/graph/build_graph_ingestion_pipeline.md` (if ingestion changes)
- Governance gate: `workflows/graph/build_graph_query_allowlist_api.md` (or `workflows/graph/research_api_allowlist_change.md` alias)

### E) ML/AI changes
- Feature set changes:
  - `workflows/data/point_in_time_feature_pipeline.md`
  - `workflows/data/build_feature_tables.md`
- Training/evaluation:
  - `workflows/ml/train_and_register_model.md`
  - `workflows/ml/evaluation_and_model_card.md`
- Serving/inference:
  - `workflows/ml/mlops_model_deploy.md`
  - `workflows/ml/inference_contract_audit.md`
- Novelty discovery:
  - `workflows/ml/novelty_candidate_generation.md`

## 3) Quality and safety checklist (always)
- PHI boundary respected?
- Dataset/feature/graph/model version tags updated?
- Data contract or API contract updated?
- Tests added (unit + integration + data quality)?
- ADR/RFC needed (schema/pipeline/architecture)?
- Observability added (logs/traces/metrics + dashboards)?
- No secrets or sensitive data in code/config/logs?
- Rollback/backfill plan documented if data changes persist?

Deliver expectation:
- PR-ready diff + test evidence + updated docs + an ops note if deployment-affecting.

## Special routing: clinical research vs engineering

If your request is any of the following, explicitly label it **CLINICAL_RESEARCH** and run `/router`:
- protocol decision logic or safety gates
- contraindications, escalation triggers, adverse-event triage
- evidence synthesis (PRISMA), evidence cards, trial endpoints
- SaMD/CDS regulatory framing for clinician-facing features

The router should select the `clinical_research` domain and invoke `workflows/clinical/*`.
