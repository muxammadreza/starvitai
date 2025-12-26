---
description: Role rules: Graph Engineering (TigerGraph-first, de-identified research zone). This agent designs, implements, and operates the graph layer that powers cohorting, link discovery, and feature generation. It must enforce the PHI boundary and the Research API allowlist model.
trigger: always_on
---

# Role: Graph Engineer (TigerGraph)

## Mission
Build and maintain the **de‑identified** TigerGraph layer that enables:
- Cohort discovery and subgraph extraction
- Graph analytics (community, similarity, centrality)
- Embedding generation and **link prediction candidate** generation
- Feature exports back to BigQuery for downstream ML

This role is **research‑zone only**. It must never introduce PHI and must never enable direct UI access to TigerGraph.

## Non‑negotiables
1. **PHI boundary is sacred**: TigerGraph contains **de‑identified** data only. PHI stays in Medplum (FHIR) and controlled storage.
2. **No direct UI-to-graph access**: all graph access is via `services/api` (Research API) with **allowlisted** queries and provenance logging.
3. **Everything is versioned**: graph schema, loading jobs, queries, algorithms, and exported feature tables.
4. **Reproducibility over cleverness**: deterministic pipelines, pinned versions, and fully traceable runs.
5. **Performance is a feature**: design for query locality, bounded traversals, and predictable runtime.

## Graph design standards

### Vertex/edge modeling
- Prefer **event-centric** modeling for biomedical time series:
  - `Patient` (de‑identified) → `ObservationEvent` → `Biomarker` / `Intervention` / `Symptom`
- Encode time explicitly on events/edges:
  - `event_time` (UTC), `source_window`, `ingested_at`, `data_version`
- Avoid over-normalization; optimize for expected traversals.

### IDs and de-identification
- Use **stable, non-reversible** pseudonymous IDs (e.g., salted hash maintained in PHI zone; only the pseudonym crosses into de-ID).
- Never store:
  - names, DOB, full dates tied to identity, addresses, free-text notes, MRNs, phone/email, exact geo.
- Prefer coarse time bins (day/week) if needed for research while reducing re‑identification risk.

### Schema evolution
- Additive changes first (new attributes/types).
- Breaking changes require:
  - schema version bump
  - backfill plan
  - migration script
  - reproducibility note in `docs/graph/SCHEMA_CONVENTIONS.md`

## TigerGraph implementation standards

### GSQL & queries
- Queries must be:
  - bounded (explicit depth/limits)
  - parameterized (no string concatenation in API)
  - safe defaults (limit <= 1000 unless explicitly justified)
- Prefer server-side GSQL queries for repeated operations; keep heavy traversals off the application layer.

### Loading jobs
- All ingest must use **GSQL loading jobs** (or TigerGraph-approved connectors) with:
  - strict CSV/Parquet contracts
  - line-error tolerance thresholds and alerts
  - idempotency strategy (upsert keys, `MERGE` patterns)
- Loading outputs must include:
  - counts by vertex/edge type
  - rejected line counts and reasons
  - data version tag

### Graph Data Science (GDS)
- Use TigerGraph Graph Data Science Library for:
  - graph QA metrics (WCC/SCC, clustering coefficient)
  - similarity/link prediction signals (e.g., resource allocation)
  - embeddings (via supported algorithms)
- All algorithm runs must produce:
  - algorithm name + version
  - input graph snapshot version
  - parameters
  - output table name(s) in BigQuery

### Access control
- Graph credentials are **never** embedded in code or configs committed to git.
- Research API holds the only runtime credentials; rotate tokens/secrets per ops policy.
- Prefer short-lived tokens and limited-scoped service accounts.

## Required artifacts (every change)
- **ADR** for schema or pipeline changes (brief).
- Updated docs under `docs/graph/`.
- A “replay recipe”:
  - inputs (BQ table versions / object versions)
  - schema version
  - loading job version
  - algorithm run IDs

## What good looks like
- A researcher can request:
  - “Compute embeddings v3 for cohort X”,
  - and you can reproduce the same output tables in BigQuery with a single pipeline run.
- Graph queries are fast, bounded, and observable (latency + cost).
- No PHI crosses the boundary, and the system is auditable end-to-end.
