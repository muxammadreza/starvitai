---
description: Build/extend the graph ingestion pipeline (BigQuery -> TigerGraph) with lineage and alerts
---

Create or update the pipeline that materializes de-identified data into TigerGraph.

1) Define the snapshot boundary:
   - daily/weekly graph snapshots (recommended) with immutable version IDs
   - map snapshot version to BigQuery table/view versions

2) Export strategy:
   - materialize BigQuery exports (CSV/Parquet) to Cloud Storage
   - include schema hash + data_version + export_time metadata

3) Load strategy:
   - run TigerGraph loading jobs per snapshot
   - enforce reject thresholds (fail fast if too many rejects)
   - record counts per vertex/edge type

4) Orchestration:
   - schedule with Cloud Run Jobs or Vertex AI Pipelines (choose one and standardize)
   - use a dedicated least-privilege service account
   - write structured logs with correlation IDs

5) Observability:
   - emit metrics: rows exported, rows loaded, rejects, runtime, cost estimate
   - alert on anomalies (null spikes, schema drift, runtime regressions)

6) Backfill strategy:
   - safe replay for N prior snapshots
   - avoid double-loading by snapshot ID

Deliver:
- pipeline spec in `docs/graph/INGESTION_PIPELINE.md`
- implementation plan + code changes (if requested)
- example run output with lineage fields.
