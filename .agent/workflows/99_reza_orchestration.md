---
description: Reza's orchestration workflow for running a "virtual team" in Antigravity (Starvit)
---

Use this as your default “how do I run the team?” playbook.

If you want automatic domain routing and workflow selection, start with `/router`.

## Step 1 — Define the change in one paragraph
Include:
- outcome (what done looks like)
- where it lives (UI / API / data / graph / ML)
- users impacted (patients, clinicians, researchers)
- constraints (security/compliance, performance targets, deadlines)

## Step 2 — Pick the lead agent (domain lead)
Choose the lead based on the *primary* surface being changed:

### UI/UX
- Lead: Frontend engineer (clinician dashboard, research workbench, or mobile)
- Partner: UI/UX design system
- Gate: Accessibility QA

### Backend/API
- Lead: Backend platform engineer
- Partner: DevEx/build (if CI/deploy changes)
- Gate: Security + Privacy/Compliance

### Data plane (BigQuery/Dataflow/Cloud SQL)
- Lead: Data Platform Architect (design) OR BigQuery Analytics Engineer (implementation)
- Partners (as needed):
  - Analytics Engineer (dbt/Dataform) for transforms
  - Dataflow/Streaming engineer for pipelines
  - Cloud SQL DB engineer for operational DB changes
- Gates:
  - Data Governance Steward (classification, policies)
  - Data Quality Engineer (tests/SLAs)
  - Security + Privacy/Compliance (PHI boundary)

### Graph / ML
- Lead: Graph/ML researcher or ML engineering
- Gates: Model Risk Eval + Privacy/Compliance + Data Quality

### Clinical research / protocol science
- Lead: Metabolic Oncology Clinical Lead
- Partners:
  - Scientific Evidence Curator (PRISMA + evidence cards)
  - Biostatistician/Trialist (SPIRIT/SPIRIT-AI; endpoint definitions)
  - Patient Safety Monitoring Lead (red flags; escalation)
  - Regulatory Affairs (SaMD/CDS framing) when clinician-facing recommendations are involved
- Gates:
  - Clinical safety review
  - Security + Privacy/Compliance (PHI boundary)

Use this path when you are:
- adding/updating protocol logic gates
- drafting evidence cards or living review updates
- shaping the research workbench to support cohorting and trial endpoints


## Step 3 — Force a lightweight design artifact
Before implementation, request:
- a short RFC/ADR (problem, options, decision, risks)
- the data contract or API contract (if applicable)
- test plan (unit + integration + quality gates)
- rollout plan (staging, backfill, migration notes)

## Step 4 — Implement as a vertical slice
- smallest end-to-end slice first (UI → API → data as needed)
- keep PRs reviewable
- each slice must include:
  - tests
  - docs updates (docs/*)
  - observability hooks (logs/traces/metrics)
  - provenance/versioning updates (datasets/features/models)

## Step 5 — Independent critique (always)
Run at least one critic workflow:
- Architecture critic (monolith boundaries, PHI boundary)
- Security critic (secrets, IAM, injection risk)
- Performance critic (query budgets, caching, indexes)
- Data governance critic (RLS/policy tags, retention)
- ML risk critic (leakage, evaluation integrity, monitoring) where relevant

## Step 6 — Integration + release
- run full test suite and contract checks
- confirm observability and dashboards
- confirm version bumps (dataset/feature/graph/model)
- document deployment and rollback notes

If unsure, start with `98_reza_feature_intake_playbook.md` and it will route you to the right workflows.
