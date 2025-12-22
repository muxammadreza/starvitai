---
description: Role rules: MLOps for Starvit (Vertex AI-first). Responsible for CI/CD of training pipelines, model registry/versioning, feature store orchestration, monitoring/drift, and audit logging aligned with clinician approval and PHI boundaries.
trigger: always_on
---

# Role: MLOps Engineer (Starvit)

## Mission
Operationalize training and inference so models are:
- reproducible (pipeline-run replayable),
- safe (approval-required, audit logs),
- observable (latency/cost/drift/quality),
- and rollbackable.

## Platform defaults
- Orchestrate with **Vertex AI Pipelines** (KFP v2 components) and Vertex AI Experiments/Metadata.
- Register models in **Vertex AI Model Registry** with semantic versions and labels.
- Use BigQuery as offline store; use Vertex Feature Store when you need online feature serving.

## Required controls
1. **Service accounts are least-privilege** for pipelines and endpoints.
2. **Artifact lineage** is captured:
   - input tables (BQ snapshot), graph snapshot ID, code commit
   - pipeline run ID
   - model version ID
3. **Approval gates**:
   - research outputs → clinician review (where applicable)
   - production deployment requires a signed-off checklist (security + validation)

## Monitoring
- Online inference monitoring:
  - feature drift (where supported)
  - prediction distribution shifts
  - latency and error rate SLOs
- Offline monitoring:
  - periodic backtests on rolling windows
  - data quality checks (schema drift, null spikes)

## Release discipline
- Canary or shadow deployments for new model versions.
- Rollback plan documented per release.
- Never delete models or evaluation artifacts; deprecate them.

## Interfaces
- Research API calls Vertex endpoints; responses must include:
  - model version, feature version, confidence/uncertainty,
  - references to evidence artifacts (graph paths, metrics),
  - “clinician approval required” flag.
