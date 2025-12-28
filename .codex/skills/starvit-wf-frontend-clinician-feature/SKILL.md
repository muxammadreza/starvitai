---
name: starvit-wf-frontend-clinician-feature
description: Implement a clinician dashboard feature (Starvit web stack)
---

# Implement a clinician dashboard feature (Starvit web stack)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Implement a clinician dashboard feature in `apps/clinician`.

Rules to follow:
- `rules/11_role_frontend_clinician_web.md`
- `rules/17_starvit_frontend_stack_web.md`
- `rules/19_starvit_api_contracts_openapi.md`

Workflow:

1) Clarify feature scope:
   - which screen (cohort list, patient detail, approvals, audit log)
   - what permission(s) gate it
   - which FHIR resources / derived metrics are involved
2) Contract-first:
   - confirm the backend endpoint exists in OpenAPI
   - generate/update Orval client and use TanStack Query hooks
3) UI composition:
   - use `packages/ui` primitives + shadcn/Radix components
   - implement loading/empty/error/partial-data + permissions denied states
4) Clinical correctness:
   - units, timestamps, provenance, derived-metric versioning
5) Testing:
   - unit tests for utilities/components
   - interaction tests for critical user actions
   - update E2E smoke suite if this is a core path
6) Performance:
   - virtualize lists/tables where needed
   - avoid unnecessary client components
Deliver:
- feature implementation
- tests
- short demo script (what to click, expected outputs)

