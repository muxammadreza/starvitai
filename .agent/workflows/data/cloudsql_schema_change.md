---
description: Cloud SQL (Postgres) schema change workflow for non-PHI operational data
---

1) Confirm the data class:
   - MUST be non-PHI (identity/roles, workflow state, audit metadata without payload)
2) Define the migration:
   - forward migration + rollback strategy
   - indexes for query patterns
3) Implement migrations:
   - Alembic (or equivalent) in PR
   - add application code changes in the same PR when feasible
4) Validate:
   - staging migration rehearsal
   - query plan for hot paths
5) Production rollout:
   - backup/PITR readiness check
   - deploy with low-traffic window if high risk
   - monitor connection counts and slow queries

Deliverables:
- migration files + schema docs update
- rollout + rollback note
- performance notes (indexes, constraints)
