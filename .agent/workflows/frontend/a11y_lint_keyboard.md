---
description: Add a11y linting + keyboard navigation checks
---

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
