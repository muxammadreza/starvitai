---
description: Architecture review (critical, cross-domain)
---

## Inputs
- design proposal (short doc)
- affected components

## Review axes
1) Boundaries and data zones (PHI vs de-ID)
2) Interfaces and versioning (OpenAPI/contracts)
3) Failure modes and resilience (timeouts, retries, idempotency)
4) Security posture (threat model, least privilege, supply chain)
5) Operability (SLOs, logs/traces, runbooks)
6) Complexity and maintainability (modular monolith discipline)

## Output
- decisions + trade-offs
- top risks + mitigations
- recommended refactors
