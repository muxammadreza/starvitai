---
description: Generate and triage novelty candidates (graph + ML + evidence) with safety gates
---

Turn link prediction outputs into a ranked queue of hypotheses for researcher review.

1) Ingest candidate edges:
   - from BigQuery output tables
   - include graph_version + model_version + params_hash

2) Compute novelty features:
   - rarity in internal evidence graph
   - cross-cohort robustness (sensitivity checks)
   - pathway coherence (community membership / motif support)

3) Evidence bundle creation:
   - k supporting paths (constrained, interpretable)
   - key features and scores
   - literature anchor list (retrieved, cited; never hallucinated)

4) Apply gating:
   - minimum confidence threshold
   - reject if no supporting paths
   - reject if violates hard biological constraints

5) Prioritize queue:
   - Tier 0/1/2/3 assignment (see `role_novelty_discovery`)
   - generate “experiment next steps” checklist for Tier 1

Deliver:
- `novelty_queue` table in BigQuery
- a reviewable markdown report under `docs/research/novelty_runs/<run_id>.md`
