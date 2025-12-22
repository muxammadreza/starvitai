---
description: Intake workflow for new third-party dependencies/models/datasets
---

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
