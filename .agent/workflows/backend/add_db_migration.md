---
description: Add a DB migration safely (Postgres)
---

# Add a Postgres migration safely

## Inputs
- goal statement (what changes + why)
- target tables/columns
- expected data volume + downtime tolerance

## Steps
1) **Design for backwards compatibility** (prefer expand/contract):
   - add new nullable column/table first
   - backfill in a separate step/job
   - switch reads/writes
   - only then drop old fields
2) **Write migration with rollback in mind**
   - reversible where feasible
   - avoid long-running locks; split large changes
3) **Backfill plan**
   - idempotent backfill job (safe to restart)
   - progress metrics + checkpoints
4) **Test**
   - run on staging with representative scale
   - verify query plans and indexes
5) **Rollout + rollback**
   - decide whether rollback is schema-only, data-only, or both
   - document conditions that trigger rollback

## Output
- migration + backfill PR
- rollout/rollback notes in `docs/ops/runbooks/` (or equivalent)
