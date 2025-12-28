---
name: starvit-wf-ml-inference-contract-check
description: Verify ML inference contract compatibility (schemas + versions)
---

# Verify ML inference contract compatibility (schemas + versions)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Define request/response schemas (JSON Schema or Pydantic models).
2) Version the model interface:
   - model version
   - feature set version
   - uncertainty/confidence representation
3) Add golden tests:
   - fixed inputs -> expected output shape
   - regression checks on exemplar cohort
4) Ensure audit fields:
   - model id/version
   - feature version
   - timestamp and request id

## Output
A verified inference contract and regression suite.

