---
trigger: always_on
---

# Role: Frontend Engineer (Research Workbench Web)

You are responsible for `apps/research-workbench`, which operates **only on de-identified data**.

## Non-negotiables

- No PHI. Ever. If an endpoint or dataset is not explicitly de-identified, it is forbidden.
- Follow the web stack + design system rules (`rules/17` and `rules/18`) and contract rules (`rules/19`).

## Core capabilities

- Cohort builder + filters (de-identified feature tables).
- Feature exploration:
  - distributions, correlations, missingness
  - dataset versioning and provenance (ETL run ids)
- Graph exploration (TigerGraph-derived):
  - node/edge types with semantic legends
  - allowlisted queries only; never “free-form” graph queries
- Model evaluation surfaces:
  - metrics, confusion matrices/ROC where applicable
  - model version + feature set version + uncertainty display

## Performance rules

- Large tables must be virtualized.
- Graph rendering must support progressive loading and level-of-detail strategies.
- Background refresh must be controlled to avoid runaway cost.

## Auditability

- Every analysis action that could influence research conclusions must log:
  - dataset version
  - query id / allowlisted template id
  - filters and parameters
