---
name: starvit-wf-ops-slo-setup
description: Define SLIs/SLOs and error budget policy for a service
---

# Define SLIs/SLOs and error budget policy for a service

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

