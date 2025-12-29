# Provenance metadata model: De-ID runs and lineage

Date: 2025-12-29
Owner: Data Platform
Status: Proposal (synthetic-only scaffold)

## Purpose
Capture lineage and versioning for each de-identification run so downstream analytics can trace outputs to code/config versions.

## Table: `analytics.deid_run_metadata`
| Field | Type | Semantics |
| --- | --- | --- |
| run_id | STRING | Unique run identifier |
| started_at | TIMESTAMP | Run start time |
| completed_at | TIMESTAMP | Run end time |
| input_count | INT64 | Number of source records received |
| output_count | INT64 | Number of records emitted |
| transform_version | STRING | Transformer version (code) |
| policy_version | STRING | De-ID policy version |
| source_system | STRING | `medplum` (prod) or `synthetic` (stub) |
| source_window_start | TIMESTAMP | Optional source time window start |
| source_window_end | TIMESTAMP | Optional source time window end |
| code_hash | STRING | Git commit or build hash |
| config_hash | STRING | De-ID config hash |

## Lineage linkage
- `deid_observations.run_id` → `deid_run_metadata.run_id`
- Versioned features should include `run_id` in feature tables when derived from de-id outputs.

## Logging expectations
- Logs include `run_id`, `transform_version`, `policy_version`, counts only.
- No PHI in logs or traces.
