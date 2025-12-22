# TigerGraph ops runbook (Starvit)

## Required runbooks
- Backup/restore
- Credential rotation
- Snapshot creation + rollback
- Upgrade minor versions (TigerGraph + GDS/Graph-ML components)
- Runaway query mitigation

## Monitoring
- availability (uptime)
- query latency (p50/p95/p99)
- load job runtime + reject rate
- disk/memory utilization

## DR drills
Perform at least quarterly in a non-prod environment:
- restore last snapshot
- validate core allowlisted queries
- validate embedding/feature exports
