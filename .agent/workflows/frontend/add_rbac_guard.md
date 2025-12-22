---
description: Add or modify RBAC guards in the frontend
---

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
