---
description: Build a point-in-time correct feature pipeline (offline -> training -> eval)
---

1) Define prediction event:
   - what is the prediction time?
   - what is the label time?
2) Define feature availability:
   - for each upstream table, what timestamps define “known by time t”?
3) Implement joins:
   - join on entity keys + time constraints
   - avoid leakage by filtering upstreams to <= prediction time
4) Validate:
   - leakage tests (spot-check future timestamps)
   - compare training vs evaluation datasets consistency
5) Version and document:
   - feature set version
   - upstream versions
   - embedding versions (if used)

Deliverables:
- BigQuery SQL (dbt/Dataform) for feature view
- Leakage-prevention evidence
- docs/ml + docs/data updates
