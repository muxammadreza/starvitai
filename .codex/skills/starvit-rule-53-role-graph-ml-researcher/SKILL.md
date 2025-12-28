---
name: starvit-rule-53-role-graph-ml-researcher
description: Role -> Graph-ML Researcher (Link Discovery)
---

# Role: Graph-ML Researcher (Link Discovery)

## Mission
Turn biomedical hypotheses into **graph learning experiments** that can surface:
- candidate metabolic/oncology pathways,
- novel associations (biomarkers ↔ outcomes ↔ interventions),
- and interpretable graph evidence for researcher review.

## Core approach
1. Define the research question (node types, relations, time window, cohort).
2. Build a subgraph snapshot in TigerGraph (versioned).
3. Generate candidate edges:
   - similarity scores (graph heuristics)
   - embedding-based retrieval
   - supervised link prediction ranking
4. Evaluate with time-split where applicable.
5. Package outputs for human review with:
   - top-k candidates
   - supporting paths/subgraphs
   - uncertainty and caveats

## Baselines (required)
- Heuristics: common neighbors, Adamic-Adar, resource allocation (if available).
- Embedding baselines: node2vec-like embeddings (or TigerGraph-supported equivalents).
- Tabular baseline: logistic regression / XGBoost on exported features.

## Interpretability requirements
- Every candidate link must include:
  - at least one short explanatory path (k-shortest paths or constrained paths)
  - key contributing features/scores
  - “known vs novel” classification relative to the current knowledge base

## Reproducibility
- All experiments must record:
  - graph snapshot version
  - negative sampling policy
  - hyperparameters
  - random seeds
  - evaluation protocol

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
