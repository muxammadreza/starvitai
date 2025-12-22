---
description: Change the allowlisted TigerGraph query surface via Research API
---

## Steps
1) Define the query intent and required parameters.
2) Confirm de-ID constraints:
   - no PHI fields
   - cohort minimums / aggregation when needed
3) Implement query server-side:
   - allowlist entry
   - parameter validation
   - execution time limits
4) Add tests:
   - authorization checks
   - output schema validation
5) Document:
   - endpoint usage
   - expected performance limits

## Output
Safe expansion of graph query capability.
