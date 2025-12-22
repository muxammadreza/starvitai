---
description: Implement graph exploration view (React Flow) for research workbench
---

Goal: provide interactive, de-identified graph exploration using allowlisted backend queries.

Steps:

1) Confirm de-ID constraints and allowlisted query template id(s).
2) Define graph schema:
   - node types and required labels
   - edge types, directionality, and meaning
3) Fetch data with generated clients + TanStack Query:
   - support pagination / incremental expansion
   - cache by (cohort id, query template id, params)
4) Render with React Flow:
   - semantic legends for node/edge types
   - progressive loading (expand on click)
   - level-of-detail rules (collapse clusters at zoom out)
5) Add auditability:
   - show dataset version + query template id in UI
   - log user actions that alter graph state significantly
6) Testing:
   - unit tests for graph transforms
   - interaction test for expand/collapse and filtering
Deliver:
- graph view + audit labels + tests
