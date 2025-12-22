---
description: Define SLIs/SLOs and error budget policy for a service
---

## Inputs
- service name + critical endpoints
- user impact definition

## Steps
1) Choose SLIs (typical):
   - availability (success rate)
   - latency (p95/p99)
   - correctness (domain-specific)
2) Set SLO targets and windows (e.g., 30 days).
3) Define alerts:
   - fast burn (page)
   - slow burn (ticket)
4) Create dashboards:
   - golden signals (latency, traffic, errors, saturation)
5) Document error budget policy:
   - when to freeze features
   - when to prioritize reliability work

## Output
- `docs/ops/SLOs.md` section for the service
- alert policies and dashboard links
