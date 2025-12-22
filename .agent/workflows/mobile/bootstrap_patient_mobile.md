---
description: Bootstrap patient mobile app baseline (Expo + RHF/Zod + TanStack Query)
---

Goal: bring `apps/patient-mobile` to Starvit baseline conventions.

Steps:

1) Confirm Expo + TypeScript + React Navigation.
2) Add form and validation baseline:
   - React Hook Form + Zod
3) Add server-state baseline:
   - TanStack Query with persistent cache strategy (if used)
4) Add offline-first write queue:
   - store pending writes locally
   - retry with backoff when online
   - show sync status
5) Add privacy constraints:
   - disable PHI in analytics events
   - logging scrubbers for sensitive values
Deliver:
- working baseline app with one measurement logging flow end-to-end
