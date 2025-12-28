# Medplum v5 compatibility notes (Starvit)

Starvit targets **Medplum v5.0.10+**.

This document exists to prevent accidental copy/paste of legacy Medplum v4 snippets or deprecated APIs.

## Breaking changes / deprecations to avoid

### 1) Search modifiers
Medplum v5 is strict FHIR and removes non-standard search modifiers.

Avoid:
- `:in` and `:not-in` search modifiers

Use instead:
- `_id=a,b,c` for ID lists
- Standard token searches or server-side ValueSet patterns where supported

### 2) Password reset and onboarding
Avoid:
- `PasswordChangeRequest`

Use instead:
- `UserSecurityRequest` and the `/auth/setpassword` endpoint flow

### 3) Access control
Avoid:
- `AccessPolicy.readonly` (deprecated)
- `AccessPolicy.resource.compartment` (deprecated)
- `InviteRequest.accessPolicy` (obsolete)

Use instead:
- `AccessPolicy.resource.interaction` allowlist
- `AccessPolicy.resource.criteria` with compartment scoping (`_compartment=%profile`) and simple, testable criteria
- Bind via `ProjectMembership.accessPolicy`

### 4) Project settings
Avoid:
- `ProjectSecret`

Use instead:
- `ProjectSetting` (including secrets) and project/system settings as supported by Medplum

### 5) Other renames
Avoid:
- `MemoizedSearchControl`

Use instead:
- `SearchControl`

### 6) Transaction bundles
- Prefer `batch` bundles by default.
- Only use `transaction` bundles when the `transaction-bundles` feature is enabled for the Medplum project.
- Treat transaction bundles as beta; implement retry logic.

## Where this is enforced
- `.agent/rules/36_medplum_v5_non_deprecated.md`
- Backend adapter workflows under `.agent/workflows/backend/`