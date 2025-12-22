---
description: Train and register a model (Vertex AI-first) with governance artifacts and full lineage
---

Train and register a model using Starvit governance and de-ID constraints.

1) Define the contract:
   - prediction task + label definition + horizon
   - intended use and explicit out-of-scope use
   - input schema (Pydantic) and output schema (include versions + uncertainty)

2) Dataset + features (de-ID only):
   - select BigQuery snapshot tables/views
   - generate a `dataset_version` and `feature_version`
   - write `docs/ml/datasheets/<dataset_version>.md`
   - enforce point-in-time correctness (no post-outcome features)

3) Pipeline orchestration (Vertex AI Pipelines):
   - components: validate -> transform -> train -> evaluate -> register
   - pin container image digests and library versions
   - use least-privilege pipeline service account

4) Experiments + metadata:
   - track runs in Vertex AI Experiments
   - log: dataset_version, feature_version, graph_version (if used), git_sha, params

5) Evaluation (must include):
   - baseline comparisons
   - ranking/classification metrics as appropriate
   - calibration assessment
   - subgroup slices (de-ID safe)

6) Governance docs:
   - model card: performance, limitations, failure modes, monitoring plan
   - update `docs/ml/MODEL_REGISTRY_CONVENTIONS.md`

7) Register:
   - publish model to Vertex AI Model Registry as a new version
   - attach labels: `dataset_version`, `feature_version`, `graph_version`, `model_semver`

8) Quality gate:
   // turbo
   - Run `poetry run pytest -q`

Deliver:
- Vertex pipeline spec + run ID
- Experiment run link + metrics
- Model Registry entry details
- model card + dataset datasheet
- PR-ready diff
