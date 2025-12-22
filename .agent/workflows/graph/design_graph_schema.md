---
description: Design a TigerGraph schema for a Starvit research question (de-identified zone)
---

Design the graph schema (vertices/edges/attributes) for a specific research use case.

1) Frame the question:
   - what are the node types? (Patient_anon, ObservationEvent, Biomarker, Intervention, Outcome, Pathway, Publication, etc.)
   - what relationships must be traversable in 1–3 hops?
   - what is the primary time axis? (event_time, window_start/end)

2) Identify data sources (de-ID only):
   - BigQuery tables/views (post-DLP)
   - evidence/literature tables (de-ID by nature)
   - derived metrics tables (e.g., GKI series)

3) Choose modeling pattern:
   - event-centric time-series (preferred) vs direct edges
   - if direct edges, add `valid_from/valid_to` or edge timestamp

4) Define IDs and uniqueness:
   - stable pseudonymous patient_id
   - deterministic event_id (patient_id + time_bin + source + type)
   - canonical biomarker/intervention identifiers (LOINC/RxNorm/curated IDs)

5) Define attributes:
   - units (mmol/L vs mg/dL) and conversions (never mix)
   - missingness indicators
   - source provenance (system, pipeline version)

6) Define schema evolution plan:
   - additive first
   - migration/backfill strategy for breaking changes

Deliver:
- `docs/graph/schema/<topic>.md` containing: schema diagram (Mermaid), vertex/edge specs, ID rules, and expected traversals.
- A minimal GSQL schema stub (vertex/edge declarations) ready to implement.
