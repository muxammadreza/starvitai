---
description: Bootstrap Starvit web frontend stack (Next.js + shadcn/ui + contract clients)
---

Goal: bring a web app (`apps/clinician-web` or `apps/research-workbench`) to Starvit baseline conventions.

Steps:

1) Confirm app uses Next.js App Router + TypeScript.
2) Install/verify UI baseline:
   - Tailwind configured with CSS-variable theme tokens
   - shadcn/ui installed and `packages/ui` exists (shared components)
   - Radix primitives available for dialogs/menus/tabs/etc.
3) Install/verify data + forms:
   - TanStack Query wired at app root (QueryClientProvider)
   - React Hook Form + Zod for validation
4) Set up API contract generation:
   - ensure backend OpenAPI URL is defined (env var)
   - add Orval config in app (or shared package) and generate typed clients
   - optionally generate MSW mocks for UI development
5) Quality gates:
   - ESLint (including a11y rules) + Prettier + TypeScript strict
   - Basic E2E smoke test (Playwright) for a single route
Deliver:
- working baseline app
- generated client wiring
- one example page demonstrating: table + form + error/empty/loading states
