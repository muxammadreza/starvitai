---
description: Change an API contract safely (OpenAPI + clients)
---

## Steps
1) Propose the contract change:
   - endpoints, request/response schema
   - backward compatibility strategy
2) Update backend OpenAPI and validate.
3) Regenerate typed clients (Orval) and ensure diffs are reviewed.
4) Add contract tests and backward compatibility checks.
5) Update docs and versioning notes.

## Output
Contract change PR with tests and client updates.
