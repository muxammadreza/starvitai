---
description: Generate graph-derived features (TigerGraph -> BigQuery) for downstream ML and research
---

Generate graph features safely and reproducibly.

1) Choose inputs:
   - graph snapshot/version
   - node/edge types and cohort scope

2) Choose feature families:
   - centrality/community metrics
   - similarity/link-prediction heuristics
   - embeddings (node representations)

3) Run algorithms:
   - follow `workflows/graph/run_gds_and_export_embeddings.md`
   - record algorithm params + runtime budgets

4) Export to BigQuery:
   - include: graph_version, algo, algo_version, params_hash, generated_at
   - ensure join keys exist for downstream training

5) Validate:
   - dimension checks (embeddings)
   - distribution sanity
   - drift vs prior versions

Deliver:
- BigQuery feature tables
- updated docs under `docs/graph/**` and `docs/ml/**`
