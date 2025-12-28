---
name: starvit-wf-frontend-add-chart-recharts
description: Add a clinical trend chart panel (Recharts)
---

# Add a clinical trend chart panel (Recharts)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Goal: display trends without hiding context.

Steps:

1) Confirm units, timestamp normalization, and sampling frequency.
2) Create a chart component:
   - labeled axes with units
   - tooltips show exact values + source timestamp
   - missing-data handling (gaps vs zeros)
3) Add an accessible summary:
   - text summary of trend and last value
   - data table fallback for screen readers if needed
4) Integrate with TanStack Query:
   - cache key includes patient id + time window + metric
5) Testing:
   - rendering with empty/missing series
   - tooltip correctness for a known point
Deliver:
- chart component + summary + tests

