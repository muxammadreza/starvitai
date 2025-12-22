# Research API allowlist for graph queries

## Principle
No UI talks directly to TigerGraph. All access is through a **Research API** allowlist.

## Allowlist entry fields
- query_id
- description + intended use
- parameter schema (types, ranges, max limits)
- authZ rules
- maximum runtime / depth / result limits
- caching policy (optional)

## Logging
Log for every call:
- actor (user/service), role
- query_id
- params_hash (not raw PHI)
- graph_snapshot_id
- output table ids (if exporting)

## Anti-patterns
- free-form GSQL execution endpoints
- unbounded traversals
- query parameters that accept arbitrary strings used in query construction
