# Graph schema conventions (Starvit)

## Goals
- Support bounded traversals for cohorting and evidence extraction.
- Make time explicit for longitudinal biology.
- Keep schema stable and versioned.

## Naming
- Vertex types: `Patient`, `ObservationEvent`, `Biomarker`, `Intervention`, `Outcome`, `Pathway`, `Publication`
- Edge types are verbs: `HAS_EVENT`, `MEASURED`, `RECEIVED`, `ASSOCIATED_WITH`, `MENTIONED_IN`

## Time modeling
Preferred: event-centric nodes with timestamps.
- `(:Patient)-[:HAS_EVENT]->(:ObservationEvent {event_time})-[:MEASURED]->(:Biomarker)`

If direct edges are necessary:
- include `valid_from`, `valid_to` or `edge_time`

## IDs
- Patient: stable pseudonym (non-reversible)
- Event: deterministic (patient + time_bin + type + source)
- External entities: canonical IDs where possible (LOINC, RxNorm, gene symbols mapped to stable IDs)

## Provenance
Every node/edge should carry:
- `data_version`
- `source_system`
- `ingested_at`

## Versioning
- Graph schema version: `graph_schema_semver`
- Snapshot version: `graph_snapshot_id` (immutable)
