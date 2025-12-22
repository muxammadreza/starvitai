# Graph layer (TigerGraph) — Starvit

TigerGraph exists only in the **de-identified research zone**.

Primary jobs:
- Cohort discovery and subgraph extraction
- Relationship mining and link discovery
- Graph features/embeddings generation for ML

Key guardrails:
- No PHI in graph.
- No direct UI access: all access via allowlisted Research API queries.
- Everything versioned: graph schema, snapshots, algorithms, exports.

Start here:
- `docs/graph/TIGERGRAPH_STACK.md`
- `docs/graph/SCHEMA_CONVENTIONS.md`
- `docs/graph/INGESTION_PIPELINE.md`
- `docs/graph/GDS_ALGORITHMS.md`
- `docs/graph/QUERY_ALLOWLIST.md`
- `docs/graph/OPS.md`
