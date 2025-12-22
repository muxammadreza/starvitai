---
description: Create or refactor a design system component (Starvit)
---

Create or refactor a shared design-system component in `packages/ui`.

Rules to follow:
- `rules/18_starvit_design_system_web.md`

Workflow:

1) Define the component contract:
   - purpose and usage contexts
   - props + variants (CVA)
   - states (loading, disabled, error)
2) Accessibility:
   - native semantics first; Radix primitive when needed
   - label + focus + keyboard behavior documented
3) Implementation:
   - Tailwind + CSS variable tokens only
   - no new dependency unless justified
4) Documentation:
   - usage examples + do/don’t guidance
   - clinical UI conventions if relevant (units, provenance)
5) Tests:
   - critical behavior tests (focus traps for dialogs, keyboard nav for menus)
6) Migration:
   - if changing API, include migration notes and (if feasible) codemod guidance
Deliver:
- component + docs/examples + tests + migration notes (when applicable)
