---
trigger: always_on
---

# Medplum v5+ (>= 5.0.10) compatibility and non-deprecated usage

Starvit must be compatible with **Medplum 5.0.10+**. Do not copy old snippets or SDK patterns.

## 1) Strict FHIR search compliance (breaking change in v5)
Medplum v5 removes non-standard search modifiers.

**DO NOT USE**
- `:in` and `:not-in` search modifiers (examples: `patient:in=...`, `code:not-in=...`).

**USE INSTEAD**
- Native FHIR patterns such as `_id=a,b,c`, token searches, and server-side ValueSet usage where supported.

## 2) Password reset / invite flows
**DO NOT USE** `PasswordChangeRequest`.

**USE INSTEAD** `UserSecurityRequest` + `POST /auth/setpassword` with `id`, `secret`, `password`.

## 3) Access control artifacts
Medplum AccessPolicy fields have deprecated variants.

**DO NOT USE**
- `AccessPolicy.readonly` (deprecated)
- `AccessPolicy.resource.compartment` (deprecated)
- `InviteRequest.accessPolicy` (obsolete)

**USE INSTEAD**
- `AccessPolicy.resource.interaction` allowlist (`read`, `write`, etc.)
- `AccessPolicy.resource.criteria` with `_compartment=%profile` and parameterized criteria
- `ProjectMembership.accessPolicy` to bind policy to identity

## 4) Project settings
**DO NOT USE** `ProjectSecret`.

**USE INSTEAD** `ProjectSetting` for project-scoped configuration and secrets.

## 5) Other renamed/removed entities
- **DO NOT USE** `MemoizedSearchControl`; **USE** `SearchControl`.
- Treat `User.externalId` and `User.admin` as deprecated; use `ProjectMembership.externalId` and membership-based authorization.

## 6) Bundles
- Prefer **batch** bundles for multi-write in MVP.
- Only use **transaction** bundles when the `transaction-bundles` feature flag is enabled for the project.
- Transaction bundles are beta; implement retry logic for `409 conflict`.

## 7) Mandatory checks when integrating with Medplum
- Confirm the target Medplum version is v5+ before implementing an integration pattern.
- Prefer Medplum documentation over third-party blog snippets.
