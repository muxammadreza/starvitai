# TigerGraph stack choices (Starvit)

## Deployment
- TigerGraph runs in the **de-identified** zone.
- Prefer managed TigerGraph where it reduces ops burden; otherwise self-managed with strict network isolation.

## Interfaces
- GSQL for schema, loading jobs, and server-side queries.
- RESTPP endpoints for query execution and admin operations.
- Python integration via **pyTigerGraph** (Research API server-side only).

## Graph analytics
- Prefer TigerGraph Graph Data Science (GDS) library algorithms for:
  - similarity signals, centrality, community structure
  - node embeddings (where supported)
- Export derived features/embeddings to BigQuery for training.

## Key libraries (Python)
- `pyTigerGraph` for REST interactions and GDS helpers
- `google-cloud-bigquery` for feature tables
- (optional) `kfp` / Vertex AI SDK for pipeline orchestration

## Security conventions
- Store TigerGraph credentials in secret manager/vault.
- Research API fetches credentials at runtime; never commit secrets.

## References (official)
- TigerGraph docs (GSQL, loading jobs, RESTPP, GDS, pyTigerGraph)
  - https://docs.tigergraph.com/
