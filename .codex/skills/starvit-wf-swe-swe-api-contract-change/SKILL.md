---
name: starvit-wf-swe-swe-api-contract-change
description: Change an API contract safely (OpenAPI + clients)
---

# Change an API contract safely (OpenAPI + clients)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

