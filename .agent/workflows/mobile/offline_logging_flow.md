---
description: Implement offline-first logging flow (patient app)
---

Goal: allow patients to log measurements reliably under poor connectivity.

Steps:

1) Define the measurement schema and constraints (units/ranges).
2) Implement local write-ahead log (WAL):
   - append-only events
   - idempotency keys
3) Implement sync engine:
   - detect connectivity
   - flush queue with retries + backoff
   - handle conflicts (server rejects -> show actionable error)
4) UX:
   - clear “pending sync” state
   - manual retry button
5) Tests:
   - offline queue behavior
   - conflict/resolution behavior
Deliver:
- offline-capable logging + tests
