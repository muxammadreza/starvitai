---
name: starvit-rule-23-role-supply-chain-security
description: Owns dependency integrity, artifact provenance, and safe ingestion of third-party code/models/datasets.
---

# Role: Supply chain security

Owns dependency integrity, artifact provenance, and safe ingestion of third-party code/models/datasets.

## Minimum posture
- Lock dependencies (pnpm-lock, poetry.lock). No floating versions for critical deps.
- SBOM for deployables (SPDX/CycloneDX).
- Build provenance / attestation where possible.

## Intake policy
Any new third-party component must have:
- provenance (publisher, repo, release tags)
- maintenance signal (recent releases, active issues)
- license compatibility
- security posture (known CVEs, advisories)

## Deliverables
- Dependency review checklist
- Automated scanners in CI (SCA)
- Provenance notes for models/datasets

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
