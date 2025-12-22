---
description: Scientific evidence ingestion → structured evidence cards → feature/protocol mapping
---

Use this workflow whenever a new paper, guideline, mechanistic hypothesis, or dataset is introduced.

## A) Ingest (source capture)
1) Capture metadata
   - full citation (authors, year)
   - DOI/URL (or internal path)
   - source type: RCT / observational / case series / case report / systematic review / guideline / mechanistic / dataset
   - population + context (cancer type, stage, cachexia status, treatment line)

2) Record provenance
   - where it was found
   - whether it is peer-reviewed
   - conflicts of interest (if disclosed)

## B) Extract (structured evidence)
Create an **Evidence Card** using:
- `.agent/workflows/clinical/evidence_card.md`

Minimum extraction:
- PICO (population, intervention, comparator, outcomes)
- effect sizes or directional outcomes
- protocol-relevant variables (labs, vitals, meds, diet parameters)
- safety signals and contraindications
- explicit limitations and external validity

## C) Grade (lightweight, reproducible)
Apply the evidence grading rubric in `docs/clinical/EVIDENCE_METHODS.md`.
Document:
- study design
- sample size
- bias risks
- generalizability
- why this does or does not support a clinical-facing claim

## D) Translate (Bio-Digital Mirror)
Mechanism → measurable signals → derived features → protocol/UX implications.

For every proposed feature or rule:
- name the underlying evidence
- specify what would falsify it
- specify what we will **not** claim

## E) Materialize (artifacts)
Write to the repository:
- Evidence Card: `docs/research/evidence-cards/<slug>.md`
- Mapping note: `docs/research/evidence-cards/<slug>.mapping.md`
- If part of a topic: add/update a living review in `docs/research/living-reviews/`

## F) Decide next action
Choose one:
- research backlog (analysis/feature engineering/graph query)
- protocol suggestion (requires clinician review + clinical safety gate)
- ignore (document rationale)

Deliverables:
- Evidence card + mapping note
- Backlog items (engineering + research) with acceptance criteria
