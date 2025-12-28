---
name: starvit-wf-qa-accessibility-review
description: Accessibility review workflow (WCAG 2.2 AA oriented)
---

# Accessibility review workflow (WCAG 2.2 AA oriented)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Automated scan:
   - axe-core on key pages
   - ESLint a11y rules
2) Keyboard walkthrough:
   - tab order, focus visibility, focus not obscured
3) Form validation:
   - error identification, labels/instructions, error recovery
4) Screen reader sanity:
   - landmarks, headings, control names
5) File issues with reproduction steps and severity.

## Output
A11y findings report + fixes backlog.

