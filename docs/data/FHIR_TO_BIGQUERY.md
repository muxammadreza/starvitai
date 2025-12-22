# FHIR → BigQuery in Starvit (de‑identified analytics plane)

## Non‑negotiable boundary
- **PHI stays in GCP Healthcare API (FHIR R4).**
- **BigQuery is de‑identified only.** Any export/stream to BigQuery must originate from a **de‑identified** FHIR store or dataset (created via Cloud Healthcare `datasets.deidentify` / `fhirStores.deidentify`).

## Why BigQuery exists in Starvit
BigQuery is the canonical de‑identified analytical store used for:
- reproducible cohort definitions,
- derived metrics and feature tables (point‑in‑time correctness),
- training/validation datasets for Vertex AI,
- staging node/edge tables for TigerGraph loads.

## Supported movement patterns

### Pattern A: Batch export (backfills + periodic loads)
Use the Cloud Healthcare API FHIR store export to BigQuery.

Operational notes:
- Choose schema type `ANALYTICS_V2` by default.
- Use `WRITE_TRUNCATE` for idempotent rebuilds, `WRITE_APPEND` + `_since` for incremental backfills.
- Prefer exporting only the resource types you need (`_type` filter) to control cost/complexity.

### Pattern B: Streaming changes (near‑real‑time)
Use Cloud Healthcare API streaming of FHIR resource changes to BigQuery.

Operational notes:
- Schema type must be chosen up front; switching from `ANALYTICS` to `ANALYTICS_V2` requires a new dataset + new config.
- Pair streaming with periodic batch reconciliations to handle missed events and schema drift.

## Data modeling conventions
- Use stable pseudo‑identifiers (no PHI) as join keys.
- Preserve event time explicitly (`effectiveDateTime`, `issued`, etc.) and also store ingestion time.
- Partition time series fact tables by event time or ingestion time; cluster by common join/filter keys.

## Governance + audit requirements
- Version and store the de‑identification config used to create the destination de‑identified FHIR store.
- Label all BigQuery jobs with: `service`, `owner`, `env`, `pipeline`, `purpose`.
- Keep lineage: source FHIR store/version → export job → destination dataset/table(s).

## Downstream: feeding TigerGraph
- Materialize node/edge tables in BigQuery (typed entities and relations).
- Export snapshots to Cloud Storage (Parquet preferred), then load into TigerGraph with loading jobs.
- Stamp everything with `graph_version` and keep a provenance table in BigQuery.
