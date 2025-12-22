---
description: Frontend performance audit and performance budget enforcement
---

Goal: prevent gradual bundle bloat and slow clinician workflows.

Steps:

1) Identify critical user journeys (cohort list, patient detail, approval queue).
2) Measure:
   - initial load
   - client bundle size
   - table render performance on large datasets
3) Apply fixes:
   - reduce client component surface
   - dynamic import heavy widgets (graphs, rarely used charts)
   - virtualize large lists
4) Add a performance budget:
   - max route JS size threshold
   - max first-load warnings in CI
Deliver:
- perf report + actionable recommendations
- CI guardrails if feasible
