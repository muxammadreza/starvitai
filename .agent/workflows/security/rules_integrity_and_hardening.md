---
description: Hardening checklist for rule/workflow packs and automation
---

## Objective
Prevent tampering, reduce risky automation, and make agent behavior reviewable.

## Checklist
1) Review permissions:
   - agent tooling must use allowlists
   - prevent write access to PHI resources unless explicitly required
2) Repository hardening:
   - CODEOWNERS for `.agent/`
   - required reviews for security-sensitive paths
3) Integrity:
   - maintain `.agent/manifest.sha256`
   - CI verifies manifest
4) Supply chain:
   - SBOM generation for deployables
   - provenance/attestations where feasible
5) Secrets hygiene:
   - secret scanning
   - no secrets in PRs, logs, or docs

## Output
A short security note describing what was hardened.
