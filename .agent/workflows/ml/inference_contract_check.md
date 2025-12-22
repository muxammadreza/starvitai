---
description: Verify ML inference contract compatibility (schemas + versions)
---

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
