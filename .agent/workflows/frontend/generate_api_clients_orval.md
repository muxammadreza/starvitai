---
description: Generate typed API clients from FastAPI OpenAPI (Orval)
---

Goal: make frontend/backend drift difficult.

Inputs:
- Backend OpenAPI schema URL (local dev or deployed)
- Output locations for generated clients and schemas

Steps:

1) Validate OpenAPI schema is reachable and up-to-date.
2) Decide generation mode:
   - React Query hooks (preferred) OR plain client functions for SSR-only call sites.
3) Configure Orval:
   - split output by tags
   - generate schemas/types
   - generate MSW mocks if needed
4) Run generation and commit outputs.
5) Update frontend imports:
   - replace hand-written fetch calls with generated hooks/functions
6) Add a contract check:
   - CI step that fails if OpenAPI changed without regeneration
Deliver:
- Orval config + generated clients
- updated call sites for at least one feature end-to-end
