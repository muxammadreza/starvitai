---
name: starvit-wf-frontend-a11y-lint-keyboard
description: Add a11y linting + keyboard navigation checks
---

# Add a11y linting + keyboard navigation checks

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Enable lint rules:
   - jsx-a11y and relevant rules
2) Add axe smoke tests for key routes.
3) Verify focus handling:
   - focus visible
   - focus not obscured
4) Verify interactive elements:
   - proper labels
   - no div-onclick without role/tabindex

## Output
A11y guardrails in CI + documented keyboard checklist.

