---
name: starvit-wf-swe-swe-backend-feature-module
description: Add a backend feature module in the modular monolith
---

# Add a backend feature module in the modular monolith

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

