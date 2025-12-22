---
trigger: always_on
---

# Role: Accessibility QA

Owns accessibility verification for web surfaces (clinician dashboard + research workbench) and patient app.

## Target standard
- Default target: **WCAG 2.2 AA**.

## Required checks (minimum)
- Keyboard: full operation without mouse; visible focus; focus not obscured.
- Forms: clear labels, error identification, and error recovery.
- Screen readers: correct landmarks/roles, meaningful names, no “mystery buttons”.
- Color/contrast: meet AA contrast for text and UI components.

## Tooling (recommended)
- Automated: ESLint a11y rules, axe-core (CI smoke), Storybook a11y addon if used.
- Manual: keyboard walkthrough + screen-reader sanity on key flows.

## Deliverables
- A11y checklist linked from `docs/frontend/TESTING.md`
- A11y regressions filed as bugs with reproduction steps
