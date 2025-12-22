# Graph Data Science algorithms (Starvit)

Use GDS outputs for:
- sanity checks (connectivity, degree stats)
- similarity/link prediction signals
- embeddings for downstream ML

## Algorithm families
- Centrality: PageRank, betweenness (if feasible at scale)
- Community: connected components / community detection
- Similarity: common-neighbor style, resource allocation, Adamic-Adar (where available)
- Embeddings: node embedding algorithms supported by TigerGraph tooling

## Output contracts
Every run must output a BigQuery table with:
- `entity_id`
- `graph_snapshot_id`
- `algo`, `algo_version`
- `params_hash`
- `generated_at`
- and the feature columns (including embedding vectors)

## Notes
- Keep runs deterministic where possible.
- Document transductive vs inductive settings explicitly.

## References (official)
- https://docs.tigergraph.com/
