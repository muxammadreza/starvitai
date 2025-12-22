---
description: Performance profiling workflow
---

## Steps
1) Define the scenario:
   - endpoint/page/pipeline stage
   - representative dataset size
2) Measure baseline:
   - latency (p50/p95)
   - CPU/memory
3) Profile:
   - backend profiling (language-specific)
   - DB query analysis
   - frontend profiling (React devtools, Lighthouse)
4) Identify bottlenecks and propose fixes.
5) Add regression guard:
   - benchmark
   - alert or CI check

## Output
Perf report + prioritized fixes.
