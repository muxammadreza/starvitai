---
name: starvit-wf-mobile-bootstrap-patient-mobile
description: Bootstrap patient mobile app baseline (Expo + RHF/Zod + TanStack Query)
---

# Bootstrap patient mobile app baseline (Expo + RHF/Zod + TanStack Query)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

