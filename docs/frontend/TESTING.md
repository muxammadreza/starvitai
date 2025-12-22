# Frontend testing (Starvit)

## Scope
Frontend tests must prove:
- critical user journeys work (clinician dashboard + research workbench)
- forms validate correctly and handle errors
- RBAC UX does not expose actions to the wrong roles (server still enforces)
- accessibility meets WCAG 2.2 AA target

## Required layers
1) Component tests
- form components (RHF + Zod)
- tables, filters, and empty/error/loading states

2) Contract alignment
- generated API clients match OpenAPI
- breaking changes require coordinated PRs

3) E2E smoke tests (Playwright)
- login
- navigate to patient detail
- view a cohort

4) Accessibility checks
- axe smoke on key pages
- keyboard navigation walkthrough

## Anti-patterns
- excessive E2E suite for everything
- coupling UI tests to unstable data
