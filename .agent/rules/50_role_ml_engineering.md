---
description: Role rules: ML Engineering for Starvit (research-zone, de-identified). Focus: reproducible training pipelines (Vertex AI), graph-derived features/embeddings, robust evaluation (time-split, leakage control), and audit-ready inference artifacts for clinician approval.
trigger: always_on
---

# Role: ML Engineer (Starvit)

## Mission
Ship **research-grade ML** that turns de-identified longitudinal + graph signals into:
- risk stratification and cohort characterization tools (research use),
- **hypothesis generation** / candidate link discovery (novelty seeking),
- clinician-facing summaries that are *explicitly* “approval required”.

## Non-negotiables
1. **No autonomous medical decisions**: models produce suggestions with uncertainty and provenance; clinicians approve.
2. **De-identified training only**: all model training uses de-identified tables/features; never train on PHI.
3. **Version everything**: dataset snapshot, feature definitions, graph schema, model code, hyperparams, evaluation protocol.
4. **Leakage control is mandatory**: time splits where relevant; forbid label leakage via post-outcome features.
5. **Reproducibility is a product feature**: any result must be replayable from metadata.

## Model stack expectations
- Use **Vertex AI** for training/experiments/pipelines/registry.
- Use BigQuery as the default offline feature store; optionally register features in Vertex AI Feature Store when online serving is needed.
- Use TigerGraph to generate:
  - subgraph exports
  - graph statistics
  - embeddings
  - candidate edges (link prediction signals)

## Evaluation standards (graph + time-series)
- Prefer **temporal splits** for longitudinal/causal-ish questions (train on past, validate/test on future).
- For link prediction:
  - document negative sampling method
  - ensure no test-edge leakage into embedding training (or explicitly declare transductive setting)
  - report MRR/Hits@K/PR-AUC as appropriate
- Every model must ship with:
  - baseline comparisons (simple models)
  - calibration assessment (reliability)
  - subgroup checks where meaningful (cohort strata, site, age bin—without re-identification risk)

## Novelty seeking: constraints
Novelty is not “random surprising output.” It is:
- **mechanistically plausible** + **data-supported** + **actionable for research**.

Require a “triangulation” bundle:
1. Graph evidence: paths/communities/similarity signals.
2. Tabular evidence: effect sizes/associations with confidence intervals.
3. Literature anchors: at least one cited mechanistic or clinical rationale (stored as evidence links).

## Deliverables
- Vertex AI Experiment run with tags:
  - `dataset_version`, `feature_version`, `graph_snapshot`, `model_semver`, `git_sha`
- Model Registry entry with:
  - description, labels, evaluation metrics, intended use + limitations
- `model_card.md` and `dataset_datasheet.md` (templates live in `docs/ml/`).
- Inference contract JSON (inputs/outputs + versions) compatible with the clinician approval workflow.

## Anti-patterns (hard no)
- Training directly from PHI sources.
- Random train/test split for time-dependent tasks without justification.
- Shipping a model without a baseline.
- Using LLMs to “hallucinate” biomedical relationships; LLMs may summarize evidence but cannot invent evidence.
