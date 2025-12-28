---
name: starvit-wf-security-supply-chain-intake
description: Intake workflow for new third-party dependencies/models/datasets
---

# Intake workflow for new third-party dependencies/models/datasets

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Inputs
- name/version/source
- purpose (why needed)

## Steps
1) Source validation:
   - official publisher/repo
   - release tags and signatures if available
2) Maintenance signal:
   - recent releases
   - responsive issue tracker
3) License + compliance:
   - compatible with project licensing
4) Security posture:
   - CVE/advisory scan
   - dependency tree size and risk
5) Pinning strategy:
   - lockfile + checksum
   - container images by digest

## Output
A short intake note and an approval decision.

