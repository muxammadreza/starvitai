# FHIR → BigQuery in Starvit (de‑identified analytics plane)

## Non‑negotiable boundary
- **PHI stays in Medplum (FHIR R4).**
- **BigQuery is de‑identified only.** Any dataset that can be joined back to a person is *not* allowed in the de-ID zone.
- De-identification must happen *before* landing data in BigQuery (Cloud DLP or an explicitly-approved equivalent).

## Why BigQuery exists in Starvit
BigQuery is the canonical de‑identified analytical store used for:
- reproducible cohort definitions,
- derived metrics and feature tables (point‑in‑time correctness),
- training/validation datasets for ML,
- staging node/edge tables for TigerGraph.

## Supported movement patterns

### Pattern A: Batch export via FHIR Bulk Data (`$export`)
1. Trigger a Medplum Bulk Export job (`$export`) for selected resource types.
2. Write NDJSON output to a staging bucket (PHI zone).
3. Run de-identification (Cloud DLP) into a *separate* de-ID bucket.
4. Load de-identified NDJSON/Parquet into BigQuery tables.
5. Run dbt/Dataform transformations into feature tables.

Operational notes:
- Prefer idempotent rebuilds: partitioned tables + overwrite-by-partition.
- Keep a lineage table in BigQuery: export job id → de-id config version → load job id → destination tables.

### Pattern B: Event-driven updates (subscriptions/bots)
1. Use Medplum Subscriptions to detect changes (e.g., Observation created/updated).
2. Trigger a Medplum Bot or Starvit worker to emit a **de-identified event** (minimal payload) to the de-ID pipeline.
3. Enrich/aggregate in the de-ID zone only.

Operational notes:
- Streaming is not a replacement for periodic reconciliation. Always pair with scheduled batch backfill.

## Data modeling conventions
- Use stable pseudo-identifiers (no direct identifiers).
- Preserve event time explicitly (`effectiveDateTime`, `issued`, etc.) and also store ingestion time.
- Partition time series fact tables by event time or ingestion time; cluster by common join/filter keys.

## Governance + audit requirements
- Version and store the de-identification config used to create each dataset.
- Label all BigQuery jobs with: `service`, `owner`, `env`, `pipeline`, `purpose`.
- Keep lineage: source export job/version → de-id job/version → load job → destination dataset/table(s).

## Downstream: feeding TigerGraph
- Materialize node/edge tables in BigQuery (typed entities and relations).
- Export snapshots (Parquet preferred), then load into TigerGraph with loading jobs.
- Stamp everything with `graph_version` and keep a provenance table in BigQuery.
