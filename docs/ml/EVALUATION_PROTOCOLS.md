# Evaluation protocols (Starvit)

These protocols exist to prevent “promising” models from becoming unsafe decision aids. Treat them as required gates for anything that influences clinical workflows.

## 1) Problem framing
Document:
- Intended use vs out-of-scope use
- Target population and exclusions (e.g., cachexia contexts if studying KMT)
- Decision impact: research-only vs clinician-facing suggestion vs protocol edit proposal

## 2) Time-aware evaluation
For longitudinal outcomes, prefer temporal splits:
- train: earlier time range
- valid/test: later time range
This reduces leakage and better matches deployment reality.

## 3) Graph/link prediction evaluation
Document explicitly:
- definition of positive edges
- negative sampling method (random vs hard negatives)
- whether embeddings were trained transductively (seeing all nodes) or inductively
- ranking metrics (MRR, Hits@K) and classification metrics (PR-AUC) as needed
- ablations: “graph only” vs “tabular only” vs “graph+tabular”

## 4) Calibration
If probabilities are shown to clinicians/researchers, calibrate and measure reliability.

## 5) External validity
When possible:
- validate on an external site/cohort (de-identified)
- report distribution shift and robustness to measurement differences

## 6) Error analysis
For top errors, attach:
- supporting / contradictory graph paths
- feature contributions (where available)
- notes on plausible confounders

## 7) Clinical evaluation alignment
For models that could be used as clinical decision support, align reporting and study design with relevant standards:
- CONSORT-AI / SPIRIT-AI when the model is evaluated in interventional trial settings
- TRIPOD-AI (and related guidance) for prediction model reporting
- “Good Machine Learning Practice” (GMLP) guiding principles for medical-device-grade ML process controls

## 8) Governance
Every evaluation must link to:
- a model card
- a dataset datasheet
- a provenance log (code + data version + parameters)
- monitoring plan (drift, performance regressions, safety signals)
