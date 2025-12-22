---
description: Data retention and deletion workflow (PHI and de-identified zones)
---

Use this when adjusting retention schedules or executing deletions.

1) Identify the data product and class:
   - PHI (FHIR)
   - de-identified (BigQuery/TigerGraph)
   - telemetry/logs
2) Determine the legal/compliance constraint:
   - minimum retention (if any)
   - deletion obligations (if any)
3) Implement deletion safely:
   - PHI: through controlled backend flows; document audit trail
   - BigQuery: table/partition purge + snapshot policies
   - TigerGraph: delete vertex/edge sets via allowlisted admin process
4) Verify:
   - confirm data no longer queryable
   - confirm backups/snapshots alignment with retention
5) Document:
   - change record with who/what/when/why
   - update docs/data retention table

Deliverables:
- Execution log + verification
- Updated retention docs/runbooks
