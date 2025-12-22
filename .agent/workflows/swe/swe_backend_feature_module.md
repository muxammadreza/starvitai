---
description: Add a backend feature module in the modular monolith
---

## Steps
1) Place feature in the correct module boundary.
2) Define public interface (service layer + schemas).
3) Add tests:
   - unit tests for logic
   - integration tests for persistence and auth
4) Ensure observability:
   - logs/traces/metrics
5) Document:
   - endpoint docs
   - runbook notes

## Output
A reviewable module with clear boundaries.
