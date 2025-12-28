---
name: starvit-rule-35-medplum-mcp-mandate
description: Starvit uses **Medplum as the PHI system of record**. All configuration and administrative changes to the Medplum instance must be performed via the **Medplum MCP server** that the user has already configured in Antigravity.
---

# Medplum MCP mandate (Starvit)

Starvit uses **Medplum as the PHI system of record**. All configuration and administrative changes to the Medplum instance must be performed via the **Medplum MCP server** that the user has already configured in Antigravity.

## 1) What MUST use MCP (admin/config)
- Creating/updating: **Project**, **ClientApplication**, **AccessPolicy**, **ProjectMembership**, **Bot**, **Subscription**, **StructureDefinition/Profile**, and project-level feature flags/settings.
- Enabling project `features` (e.g., `bots`, `cron`, `transaction-bundles`) and any `systemSetting` / `systemSecret` values.
- Bulk provisioning (initial dev tenant bootstrap, test fixtures).

## 2) What MAY use normal HTTP (runtime app flows)
- Starvit application runtime reads/writes to Medplum FHIR endpoints for normal operations (e.g., create Observation) may use the backend’s standard HTTP client.
- Even for runtime flows, prefer Medplum SDK patterns when they reduce surface area.

## 3) Tooling rule
- If you need to change the Medplum instance: **discover and use the MCP tools**.
- If a required capability is missing from MCP tooling, stop and propose a minimal MCP extension rather than “working around” with ad-hoc scripts or manual console actions.

## 4) Secret handling
- Never print, log, or commit client secrets.
- Treat the MCP server’s credentials as highly privileged (Super Admin).
- Prefer Medplum **Project secrets** for bot/integration credentials (not Starvit repo secrets).

## 5) Auditability expectations
- Any MCP-driven change should be described in a short change log entry (what/why) and should be reproducible.
- Where feasible, capture configuration changes as code (JSON templates checked into repo) and apply via MCP.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
