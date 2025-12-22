# ADR-0003: BigQuery’s role in Starvit (and how it feeds TigerGraph)

## Status
Accepted (2025-12-21)

## Context
Starvit is a clinician-supervised metabolic-therapy support platform with a strict PHI boundary:
- PHI is stored only in **GCP Cloud Healthcare API** as **FHIR R4**.
- The research/ML plane is **de-identified** and must support:
  - reproducible cohorting and SQL analytics on clinical events,
  - feature/label tables for ML training and evaluation,
  - graph-based discovery (embeddings, relationship mining, link prediction candidates) in TigerGraph,
  - auditability (lineage, versions, “why this recommendation”).

We also want the option to augment with external datasets (including BigQuery public datasets), but we cannot assume cross-region joins or perimeter access will work without explicit design.

## Decision
We will keep **BigQuery** as a first-class component of the **de-identified analytics plane**.

BigQuery’s role is:
1) Canonical de-ID analytical warehouse (SQL-on-FHIR using Analytics V2 schema)
2) Feature + label store (point-in-time correct, versioned)
3) Staging surface for graph construction (materialize node/edge tables; export snapshots)
4) Governance anchor (IAM, policy tags, RLS, retention)

TigerGraph’s role is:
- Relationship mining and discovery workflows (subgraph patterns, cohorts, link prediction candidates)
- Graph feature generation (embeddings/centrality/community metrics) exported back to BigQuery

UIs never access TigerGraph directly; graph access is mediated by the backend Research API with allowlisted queries + provenance logging.

## Consequences
### Pipeline topology
- PHI FHIR store → (deidentify) → de-ID FHIR store → (export/stream) → BigQuery → (export snapshot) → TigerGraph
- TigerGraph graph features → BigQuery feature tables → Vertex AI training/serving

### Schema and versioning
- Prefer Healthcare API **Analytics V2** schema when exporting/streaming FHIR to BigQuery.
- Every derived table must carry: `source_version`, `transform_version`, `generated_at`, and (when applicable) `graph_version`.

### Public dataset augmentation (conditional)
- BigQuery public datasets are often located in `US` or `EU`, and BigQuery does not allow cross-location joins.
- Public datasets may be blocked by VPC Service Controls by default.
- Therefore, public data usage requires an explicit intake workflow and ADR:
  - materialize a minimal subset into a governed dataset in the same location as Starvit de-ID analytics, or
  - colocate Starvit de-ID analytics in a location compatible with the required public datasets.

### Operational work
- Establish dataset taxonomy and locations (dev/stage/prod) and enforce job labels.
- Build and operate the export/streaming pipelines and the graph load/export pipeline.

## Alternatives considered
1) **TigerGraph-first (no BigQuery)**
   - Pros: fewer systems.
   - Cons: weak for tabular cohorting, point-in-time feature tables, and integration with Vertex AI feature stores; forces custom ETL and makes reproducibility harder.

2) **GCS + Spark/Dataproc-only (no BigQuery)**
   - Pros: flexible compute.
   - Cons: more infra and governance burden; slower iteration for analysts; still needs a “warehouse-like” semantic layer.

3) **Traditional OLTP database as analytics store (Postgres/AlloyDB)**
   - Pros: familiar.
   - Cons: not cost/performance-optimal for large-scale analytic transformations; poor fit for public dataset integration.

## Follow-ups
- Implement/maintain the workflows:
  - `.agent/workflows/data/fhir_to_bigquery_export.md`
  - `.agent/workflows/data/public_bigquery_dataset_intake.md`
  - `.agent/workflows/data/bigquery_to_tigergraph_graph_load.md`
  - `.agent/workflows/graph/run_gds_and_export_embeddings.md`
- Update `docs/ARCHITECTURE.md` diagram when data residency requirements are finalized.
