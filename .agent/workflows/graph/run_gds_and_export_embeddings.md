---
description: Run TigerGraph Graph Data Science algorithms and export embeddings/features back to BigQuery
---

Generate graph-derived features (centrality, community, embeddings, similarity) for ML and research.

1) Choose algorithm outputs:
   - QA: connected components, degree stats
   - Similarity: resource allocation / common-neighbor style scores
   - Embeddings: node embedding algorithm supported by the platform

2) Define the scope:
   - which snapshot (graph_version)
   - which node types (e.g., Biomarker, Intervention, Outcome)
   - cohort filter (optional)

3) Execute runs:
   - use pyTigerGraph / GDS endpoints
   - pin algorithm parameters and random seeds (if applicable)
   - enforce runtime budgets

4) Persist outputs:
   - write results to TigerGraph attributes or output tables
   - export to BigQuery feature tables with:
     `graph_version`, `algo`, `algo_version`, `params_hash`, `generated_at`

5) Validate:
   - distribution sanity checks (no NaN, correct dimensions)
   - drift checks vs prior version
   - downstream join keys work (entity_id)

Deliver:
- BigQuery tables ready for training
- updated `docs/graph/GDS_ALGORITHMS.md` and `docs/ml/DATASETS_FEATURES.md`
