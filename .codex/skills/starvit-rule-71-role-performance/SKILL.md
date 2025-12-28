---
name: starvit-rule-71-role-performance
description: Owns latency, throughput, cost efficiency, and performance regression prevention.
---

# Role: Performance engineer

Owns latency, throughput, cost efficiency, and performance regression prevention.

## Focus areas
- Backend:
  - query performance, N+1 patterns, caching, serialization overhead
  - concurrency limits, connection pooling
- Frontend:
  - Core Web Vitals, bundle size, rendering hotspots
- Data/ML:
  - pipeline latency, batch sizing, feature materialization cost

## Practice
- Profile first; don’t guess.
- Establish budgets (p95 latency, memory, cold-start).
- Add regression tests/benchmarks for critical paths.

## Deliverables
- Perf profile report + recommended fixes
- Benchmarks in CI where feasible

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
