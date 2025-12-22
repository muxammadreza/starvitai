---
description: End-to-end graph link prediction experiment pipeline (TigerGraph -> BigQuery -> Vertex AI)
---

Run a reproducible link prediction experiment to surface candidate relationships.

1) Define the task precisely:
   - what relation are we predicting? (e.g., Biomarker -> Outcome association)
   - what is the prediction time / horizon?
   - what constitutes positive edges and negatives?

2) Build dataset snapshot:
   - choose `graph_version` + `dataset_version`
   - export positives and candidate negatives to BigQuery
   - ensure temporal split if applicable

3) Feature generation:
   - graph heuristics (CN/AA/RA)
   - embeddings from TigerGraph GDS (or equivalent)
   - tabular covariates (labs, interventions, demographics bins – de-ID safe)

4) Train baselines:
   - heuristic ranker only
   - logistic regression / XGBoost
   - (optional) GNN baseline if justified

5) Train primary model (Vertex AI):
   - Vertex AI Pipeline with: data prep -> train -> eval -> register
   - log all metadata to Vertex ML Metadata / Experiments
   - register in Model Registry with labels: `graph_version`, `feature_version`

6) Evaluate:
   - report metrics appropriate for ranking (MRR/Hits@K/PR-AUC)
   - check calibration and subgroup slices (de-ID safe)
   - error analysis: top false positives/negatives with paths

7) Package outputs for novelty triage:
   - top-k candidates with:
     scores, uncertainty, supporting paths/subgraphs, feature attributions

Deliver:
- BigQuery candidate table(s)
- Vertex AI Experiment + Model Registry entry
- updated `docs/ml/EVALUATION_PROTOCOLS.md` and `docs/ml/NOVELTY_SEEKING.md`
