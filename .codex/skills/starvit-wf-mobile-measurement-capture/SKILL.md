---
name: starvit-wf-mobile-measurement-capture
description: Implement a measurement capture flow (mobile)
---

# Implement a measurement capture flow (mobile)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Use this to add a new patient measurement capture (e.g., glucose, ketones, weight).

## Steps
1) Define the measurement contract:
   - units, ranges, timestamps, source (manual/sensor)
2) Build UI:
   - accessible inputs + validation (RHF + Zod)
   - confirmation and error states
3) Offline-first:
   - queue writes locally
   - retry with backoff
   - show sync state
4) Backend integration:
   - call the API client (generated)
   - idempotency key for retries
5) Verification:
   - unit tests for validation
   - integration test for API write

## Output
- End-to-end logging flow + tests.

