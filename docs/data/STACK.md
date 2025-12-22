# Data & database stack

## Scope
This folder defines Starvit’s **data plane** (in addition to TigerGraph):
- PHI system of record (FHIR on GCP Healthcare API)
- de-identification boundary and pipeline patterns
- BigQuery warehouse + feature tables
- transformation layer (dbt/Dataform)
- streaming/batch pipelines (Pub/Sub + Dataflow where needed)
- operational relational database for **non-PHI** app data (Cloud SQL for Postgres)

## Architectural boundaries (authoritative)
- **PHI is stored only in the FHIR store** (GCP Healthcare API, FHIR R4).
- The research/ML zone is **de-identified only**:
  - BigQuery datasets
  - TigerGraph
  - ML feature tables and embeddings
- The backend API is the policy enforcement point:
  - access controls
  - allowlisted graph queries
  - auditability (inputs → outputs → model/version → clinician decision)

## Recommended components
### 1) PHI zone
- GCP Healthcare API (FHIR R4): canonical clinical data and observations.

### 2) De-identification and movement
- Use Healthcare API de-identification and/or Cloud DLP configurations as the gate.
- Support both:
  - batch exports (backfill, daily refresh)
  - streaming changes (when near-real-time research updates are required)

### 3) Warehouse and feature store (de-identified)
- BigQuery:
  - analytics datasets
  - feature tables/views for training/evaluation
  - (optional) online feature access via BigQuery views or Vertex Feature Store integration

### 4) Transformation layer
- dbt Core is preferred for CI-tested transformations and data contracts.
- Dataform is acceptable for BigQuery-native SQL-first workflows when it improves team velocity.

### 5) Pipelines
- Pub/Sub for event buffering (de-identified messages only).
- Dataflow (Apache Beam) for robust stream/batch ETL where needed.
- Workflows/Composer for orchestration depending on complexity.

### 6) Operational relational database (non-PHI)
- Cloud SQL for Postgres:
  - users/roles (non-clinical identity metadata)
  - workflow state and configuration versions
  - audit metadata (no PHI payloads)
  - system bookkeeping

## Conventions
- Environment separation: dev/stage/prod projects and datasets.
- Dataset naming: `sv_<env>_<domain>`
- Every data product must have:
  - owner + on-call
  - contract (grain, keys, semantics, units)
  - tests + monitoring
  - retention policy
