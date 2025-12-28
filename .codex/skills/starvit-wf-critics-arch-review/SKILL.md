---
name: starvit-wf-critics-arch-review
description: Architecture review (critical, cross-domain)
---

# Architecture review (critical, cross-domain)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

