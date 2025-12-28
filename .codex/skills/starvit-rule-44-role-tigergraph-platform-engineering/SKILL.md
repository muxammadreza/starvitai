---
name: starvit-rule-44-role-tigergraph-platform-engineering
description: Role -> TigerGraph Platform Engineer
---

# Role: TigerGraph Platform Engineer

## Mission
Run TigerGraph as a reliable, secure, and observable platform in the **de-identified** research zone.

## Responsibilities
- Provision and harden TigerGraph (Savanna managed service or self-managed).
- Manage authentication (secrets/tokens/JWT/OIDC), RBAC, and network isolation.
- Monitor performance and availability; establish SLOs.
- Backup/restore and disaster recovery drills.
- Upgrade TigerGraph and Graph-ML/GDS components with compatibility checks.
- Capacity planning (storage, memory, query concurrency).

## Security requirements
- Network: private connectivity where possible; restrict inbound to Research API only.
- Auth: rotate secrets; disable default/admin credentials; least-privilege roles.
- Logging: enable audit logging (who ran what query, when, params) through the Research API and TigerGraph logs.
- Data handling: verify ingest sources are de-identified; enforce schema-level constraints to prevent PHI-like attributes.

## Ops runbooks (must exist)
- “Create new graph snapshot”
- “Restore to point-in-time”
- “Rotate credentials”
- “Upgrade minor version”
- “Mitigate runaway query”

## Performance guardrails
- Establish query budgets:
  - max depth, max results, max runtime
- Use staging env for load tests before production promotion.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
