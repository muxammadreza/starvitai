---
description: Implement a high-performance table view (TanStack Table + Virtualization)
---

Goal: render cohorts, observations, or audit logs at scale.

Steps:

1) Define table contract:
   - columns (id, label, formatter, sort/filter capabilities)
   - row identity and stable keys
2) Implement with TanStack Table:
   - sorting, filtering, column visibility
   - server-side pagination where needed
3) Add virtualization with `@tanstack/react-virtual`:
   - windowed rows
   - sticky headers if needed
4) UX states:
   - skeleton loading
   - empty state with “clear filters”
   - error state with retry
5) Accessibility:
   - keyboard navigation for row focus
   - ensure semantic table markup or accessible grid pattern
6) Testing:
   - column config unit tests
   - interaction test for sorting/filtering
Deliver:
- reusable table component (prefer `packages/ui` if general)
- one integrated screen with real API data
