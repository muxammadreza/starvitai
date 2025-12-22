# Ingestion pipeline (BigQuery -> TigerGraph)

## Boundary
Only **de-identified** BigQuery exports may enter TigerGraph.

## Snapshot model
- Create immutable graph snapshots (daily/weekly) with IDs.
- Each snapshot maps to:
  - BigQuery table/view versions
  - schema version
  - loading job version

## Typical flow
1. BigQuery materializes export tables/views (post-DLP).
2. Export to Cloud Storage (CSV/Parquet) with schema hash metadata.
3. TigerGraph loading jobs ingest the files.
4. Post-load validation:
   - counts by type
   - reject rate
   - spot-check query results
5. Write lineage record back to BigQuery (`graph_lineage` table).

## Orchestration options
- Cloud Run Jobs (simple)
- Vertex AI Pipelines (if tightly coupled to ML pipelines)

## Observability
Log and alert on:
- reject spikes
- runtime regressions
- schema drift
- cohort count anomalies
