---
description: Build/extend the Research API allowlist for TigerGraph queries (no direct UI access)
---

Expose graph capabilities safely via allowlisted endpoints.

1) Define the query contract:
   - purpose, parameters, limits, expected output schema
   - classify endpoint: research-only

2) Implement the TigerGraph query:
   - bounded traversal and safe defaults
   - deterministic ordering where feasible (stable pagination)

3) Add allowlist entry:
   - query id, param schema, max limits, authZ rules
   - caching policy (optional)

4) Add provenance logging:
   - user/role, query id, params hash, graph_version
   - output table id(s) if exporting

5) Abuse controls:
   - rate limit by user/org
   - prohibit wildcard expansions that can explode runtime

6) Tests:
   - contract tests for param validation
   - integration test with a local/stub TigerGraph client

Deliver: PR-ready diff + allowlist entry + tests + example request/response + audit log example.
