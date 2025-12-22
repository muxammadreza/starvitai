---
description: Implement TigerGraph schema + loading jobs + core queries (Starvit de-identified zone)
---

Implement a graph schema change end-to-end.

1) Preconditions:
   - confirm de-ID boundary: all inputs are de-identified BigQuery exports
   - confirm expected query patterns + max depth/limits

2) Implement schema:
   - author `schema.gsql` with vertex/edge types + primary IDs
   - include required common attributes: `data_version`, `ingested_at`, `source_system`

3) Implement loading jobs:
   - define input contracts (CSV/Parquet fields, types, nullability)
   - build idempotent upserts (stable keys; avoid duplicates)
   - emit load summaries: inserted/updated counts and reject counts

4) Implement core queries:
   - bounded traversal queries for cohort/subgraph extraction
   - graph QA queries (counts, degree distributions)
   - ensure all queries are parameterized and safe-default limited

5) Wire Research API:
   - add allowlisted endpoints mapping to specific GSQL queries
   - validate all parameters (type, range, limits)
   - emit provenance logs (who/what/when + query id + params hash)

6) Tests and validation:
   - schema lint checks (naming conventions, attribute presence)
   - ingest a small synthetic dataset
   - validate query latency and result correctness

7) Quality gate:
   // turbo
   - Run `poetry run pytest -q`

Deliver: PR-ready diff + loading job contracts + allowlist entries + test evidence + updated `docs/graph/**`.
