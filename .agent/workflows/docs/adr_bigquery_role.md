---
description: Produce/update an ADR clarifying BigQuery’s role and the TigerGraph integration strategy
---

Use when: the team is uncertain about BigQuery vs TigerGraph responsibilities, public dataset integration, or data residency constraints.

## Workflow
1) Summarize constraints
   - PHI boundary (Healthcare API only)
   - de-ID-only analytics (BigQuery + TigerGraph)
   - no direct UI access to TigerGraph
   - target latency requirements (batch vs near real-time)

2) Inventory use cases
   - cohorting and tabular analytics
   - feature/label tables for ML
   - graph construction and graph features
   - external/public dataset augmentation

3) Decide (and state) the division of labor
   - BigQuery: canonical de-ID warehouse + feature store + staging surface
   - TigerGraph: relationship mining, embeddings, link prediction candidates

4) Call out feasibility traps
   - BigQuery location constraints (public datasets in US/EU; no cross-location joins)
   - VPC Service Controls restrictions
   - schema migration constraints for Analytics → Analytics V2 streaming

5) Capture consequences and action items
   - datasets to create (env separation, location)
   - required workflows/pipelines to build
   - monitoring and governance additions

6) Write the ADR
   - add under `docs/decisions/`
   - update `docs/ARCHITECTURE.md` diagram/notes if required

## Deliverables
- ADR file
- Any required edits to architecture docs and agent rules
