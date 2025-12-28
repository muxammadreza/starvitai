---
name: starvit-wf-data-public-bigquery-dataset-intake
description: Intake a public/external dataset into the Starvit de-ID zone (BigQuery) for governed use
---

# Intake a public/external dataset into the Starvit de-ID zone (BigQuery) for governed use

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Use when: you want to use a BigQuery public dataset (or any third-party dataset) to augment research/ML.

## Workflow
1) Confirm the scientific need
   - what hypothesis/feature it enables
   - which columns are required (minimum necessary)

2) Confirm governance
   - licensing/attribution and allowed downstream use
   - privacy risk: can the dataset enable re-identification when joined with Starvit data?

3) Confirm feasibility constraints
   - dataset location (US/EU/etc) vs Starvit de-ID dataset location
   - VPC Service Controls: public datasets may be blocked by default

4) Materialize a minimal governed subset
   - run queries in the dataset's location and write results to a governed dataset in the same location
   - export to Cloud Storage and load into Starvit de-ID location if cross-location is required
   - document transformation steps and checksums

5) Create an ADR + data contract
   - dataset purpose, owner, retention, and allowed joins
   - tables, schemas, partitioning, and lineage

6) Add monitoring
   - data quality checks
   - cost guardrails

## Deliverables
- ADR under `docs/decisions/`
- BigQuery tables/views in a governed dataset
- Data contract + lineage notes
- Risk assessment (privacy + licensing)

