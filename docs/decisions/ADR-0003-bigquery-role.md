# ADR-0003: BigQuery’s role in Starvit (and how it feeds TigerGraph)

## Status
Accepted (2025-12-21)
Updated (2025-12-26): PHI system of record is Medplum.

## Context
Starvit is a clinician-supervised metabolic-therapy support platform with a strict PHI boundary:
- PHI is stored only in **Medplum** as **FHIR R4**.
- The research/ML plane is **de-identified** and must support:
  - reproducible cohorting and SQL analytics on clinical events,
  - feature/label tables for ML training and evaluation,
  - graph-based discovery (embeddings, relationship mining, link prediction candidates) in TigerGraph,
  - auditability (lineage, versions, “why this recommendation”).

## Decision
We will keep **BigQuery** as a first-class component of the **de-identified analytics plane**.

BigQuery’s role is:
1) Canonical de-ID analytical warehouse
2) Feature + label store (point-in-time correct, versioned)
3) Staging surface for graph construction (materialize node/edge tables; export snapshots)
4) Governance anchor (IAM, RLS, retention)

TigerGraph’s role is:
- Relationship mining and discovery workflows (subgraph patterns, cohorts, link prediction candidates)
- Graph feature generation (embeddings/centrality/community metrics) exported back to BigQuery

UIs never access TigerGraph directly; graph access is mediated by the backend Research API with allowlisted queries + provenance logging.

## Consequences
### Pipeline topology
- Medplum FHIR → (export) → PHI staging → (Cloud DLP de-id) → de-ID staging → BigQuery → (export snapshot) → TigerGraph
- TigerGraph graph features → BigQuery feature tables → ML training/serving

### Schema and versioning
- Do not assume a vendor-provided “SQL-on-FHIR” schema.
- We maintain a versioned flattening schema:
  - raw de-identified NDJSON (optional retention)
  - normalized “resource” tables (one per resource type)
  - curated fact/dimension tables for analytics/features
- Every derived table must carry: `source_version`, `transform_version`, `generated_at`, and (when applicable) `graph_version`.

### Public dataset augmentation (conditional)
- BigQuery public datasets may be constrained by location and governance.
- Public data usage requires an explicit intake workflow and ADR:
  - materialize a minimal subset into a governed dataset in the same location as Starvit de-ID analytics, or
  - colocate Starvit de-ID analytics in a location compatible with the required public datasets.

### Operational work
- Establish dataset taxonomy and locations (dev/stage/prod) and enforce job labels.
- Build and operate the export/de-ID/load pipelines and the graph load/export pipeline.

## Alternatives considered
1) **TigerGraph-first (no BigQuery)**
2) **GCS + Spark/Dataproc-only (no BigQuery)**
3) **Traditional OLTP database as analytics store (Postgres/AlloyDB)**

## Follow-ups
- Implement/maintain the workflows:
  - `.agent/workflows/data/fhir_to_bigquery_export.md`
  - `.agent/workflows/data/public_bigquery_dataset_intake.md`
  - `.agent/workflows/data/bigquery_to_tigergraph_graph_load.md`
  - `.agent/workflows/graph/run_gds_and_export_embeddings.md`
