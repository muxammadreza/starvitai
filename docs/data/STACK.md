# Data & database stack

## Scope
This folder defines Starvit’s **data plane** (in addition to TigerGraph):
- PHI system of record (FHIR on Medplum)
- de-identification boundary and pipeline patterns
- BigQuery warehouse + feature tables (de-identified)
- transformation layer (dbt/Dataform)
- streaming/batch pipelines (Pub/Sub + Dataflow where needed)
- operational relational database for **non-PHI** app data (Postgres)

## Architectural boundaries (authoritative)
- **PHI is stored only in the FHIR store** (Medplum, FHIR R4).
- The research/ML zone is **de-identified only**:
  - BigQuery datasets
  - TigerGraph
  - ML feature tables and embeddings
- The backend API is the policy enforcement point:
  - access controls
  - allowlisted graph queries
  - auditability (inputs → outputs → versions → clinician decision)

## Recommended components
### 1) PHI zone
- Medplum FHIR store (FHIR R4): canonical clinical data and observations.

### 2) De-identification and movement
- Use **Cloud DLP** (or an explicitly-approved equivalent) as the de-identification gate before any PHI leaves the PHI zone.
- Medplum → de-ID zone movement patterns:
  - **Batch export** via FHIR Bulk Data (`$export`) for backfills and periodic refreshes
  - **Event-driven** via Medplum Subscriptions/Bots to emit **de-identified** events for downstream processing

### 3) Warehouse and feature store (de-identified)
- BigQuery:
  - analytics datasets
  - feature tables/views for training/evaluation

### 4) Transformation layer
- dbt Core is preferred for CI-tested transformations and data contracts.
- Dataform is acceptable for BigQuery-native SQL-first workflows when it improves team velocity.

### 5) Pipelines
- Pub/Sub for event buffering (de-identified messages only).
- Dataflow (Apache Beam) for robust stream/batch ETL where needed.
- Workflows/Composer for orchestration depending on complexity.

### 6) Operational relational database (non-PHI)
- Postgres (Cloud SQL / managed PG / etc.):
  - workflow state and configuration versions
  - audit metadata (no PHI payloads)
  - system bookkeeping

## Conventions
- Environment separation: dev/stage/prod datasets.
- Dataset naming: `sv_<env>_<domain>`
- Every data product must have:
  - owner
  - contract (grain, keys, semantics, units)
  - tests + monitoring
  - retention policy
