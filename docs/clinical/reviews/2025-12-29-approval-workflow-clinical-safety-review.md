# Clinical safety review: clinician approval workflow (2025-12-29)

## Scope
Versioned PlanDefinition schema and clinician approval workflow (Task → approve/reject) for protocol recommendations.

## Findings
- No autonomous treatment execution; all recommendations remain clinician-supervised.
- Decision provenance and audit trail improve safety transparency.

## Safety gates
- Approval-required steps enforced at protocol schema level.
- Decisions captured with Task status transitions + Provenance signature.
- AuditEvent emitted for proposal + decision.

## Required fixes
- None.

## Nice-to-haves
- Add UI cues that decisions are pending approval for all recommendation panels.

## Sign-off
Reviewer: Codex (clinical safety workflow)
Version identifiers: PlanDefinition schema v1; Task approval workflow v1
