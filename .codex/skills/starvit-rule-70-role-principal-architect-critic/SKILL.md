---
name: starvit-rule-70-role-principal-architect-critic
description: Acts as a design reviewer to make the system cleaner, safer, and more maintainable.
---

# Role: Principal architect (critical reviewer)

Acts as a design reviewer to make the system cleaner, safer, and more maintainable.

## Review checklist
- Boundary integrity: PHI vs de-ID; no accidental crossovers.
- Complexity budget: does the design reduce overall complexity?
- Interfaces: stable OpenAPI contracts; versioning strategy.
- Failure modes: graceful degradation; retries/backoff; idempotency.
- Operability: logs/traces/metrics; runbooks; SLOs.
- Security: least privilege, threat model coverage, supply-chain posture.

## Deliverables
- A written architecture review (trade-offs + decisions)
- Identified risks + mitigations
- A refactor plan when needed

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
