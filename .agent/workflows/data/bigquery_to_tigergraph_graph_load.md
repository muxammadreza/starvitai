---
description: Build/refresh a TigerGraph snapshot using BigQuery as the staging surface
---

Use when: you need to (re)build TigerGraph vertices/edges from de-ID BigQuery tables.

## Workflow
1) Declare snapshot metadata
   - `graph_version` (timestamped or semver)
   - vertex/edge types in scope
   - event-time semantics and cohort scope

2) Materialize staging tables in BigQuery
   - one table per vertex type: `vertex_id`, attributes, optional `valid_from`/`valid_to`, `graph_version`
   - one table per edge type: `src_id`, `dst_id`, `event_time`, attributes, `graph_version`
   - ensure stable pseudo-IDs; no PHI

3) Export snapshot artifacts to Cloud Storage
   - Parquet preferred
   - `gs://<bucket>/graph_snapshots/<graph_version>/<type>.parquet`
   - record row counts and checksums

4) Load into TigerGraph
   - use loading jobs from cloud storage (GCS) or the Data Warehouse Loader if available
   - validate vertex/edge counts and PK uniqueness
   - run a minimal smoke query suite

5) Persist provenance
   - write a BigQuery row into `graph_build_log` with job ids, sources, counts, and URIs
   - tag/annotate TigerGraph snapshot with `graph_version`

## Deliverables
- staging SQL + BigQuery DDL
- Cloud Storage snapshot path(s)
- TigerGraph loading job config + runbook
- provenance log entry
