---
name: starvit-wf-critics-threat-model
description: Threat model a feature or service change
---

# Threat model a feature or service change

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

