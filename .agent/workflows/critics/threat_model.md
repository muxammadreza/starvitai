---
description: Threat model a feature or service change
---

## Approach
Use STRIDE for security threats and LINDDUN-style thinking for privacy risks.

## Steps
1) Diagram the dataflow:
   - actors
   - trust boundaries
   - data stores
2) Enumerate threats:
   - spoofing/tampering/repudiation/info disclosure/DoS/elevation
   - privacy risks: linkability, identifiability, detectability, disclosure
3) Prioritize risks:
   - severity x likelihood
   - PHI boundary escalates severity
4) Define mitigations:
   - technical controls
   - monitoring + detection
   - operational controls
5) Produce test cases for the top risks.

## Output
Threat model note + mitigation checklist.
