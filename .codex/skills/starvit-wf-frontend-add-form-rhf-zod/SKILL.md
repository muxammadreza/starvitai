---
name: starvit-wf-frontend-add-form-rhf-zod
description: Add a form with schema validation (React Hook Form + Zod)
---

# Add a form with schema validation (React Hook Form + Zod)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Goal: implement a clinician/research form that is hard to misuse.

Steps:

1) Define the domain intent and validation rules as a Zod schema.
2) Use React Hook Form with zodResolver; ensure:
   - default values
   - disabled states while saving
   - field-level and form-level error messaging
3) Add accessibility:
   - labels, descriptions, error association
   - keyboard-first navigation
4) Integrate with TanStack Query mutation:
   - optimistic update only when safe
   - rollback on failure
   - invalidate relevant queries by key
5) Add tests:
   - schema unit tests for edge cases
   - interaction test for success/failure UX
Deliver:
- form component + schema + tests
- documented error and loading states

