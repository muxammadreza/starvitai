# ML stack choices (Starvit)

## Orchestration
- Vertex AI Pipelines (KFP v2 components) for reproducible runs.
- Vertex AI Experiments / ML Metadata for tracking.

## Storage
- Offline features: BigQuery (default).
- Online features (only when needed): Vertex AI Feature Store (with strict contracts).

## Registry and serving
- Vertex AI Model Registry for versioned models.
- Serving behind Research API with:
  - model version, feature version, uncertainty
  - evidence links (graph paths, key features)
  - “clinician approval required” flag

## Graph integration
- TigerGraph produces:
  - embeddings
  - similarity/link prediction heuristics
  - subgraph exports for interpretability

## References (official)
- https://cloud.google.com/vertex-ai
