---
name: starvit-wf-frontend-add-rbac-guard
description: Add or modify RBAC guards in the frontend
---

# Add or modify RBAC guards in the frontend

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Confirm the source of truth:
   - server-enforced RBAC is primary
   - frontend guards are UX helpers
2) Add route-level guard:
   - redirect or show "not authorized"
3) Hide/disable unauthorized actions in UI.
4) Add tests:
   - component tests for guard behavior
   - E2E smoke for unauthorized user

## Output
RBAC UX aligned with backend enforcement.

