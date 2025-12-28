# Medplum MCP server (Starvit)

Starvit uses Medplum as the PHI system of record. To reduce compliance and security risk, Starvit treats **Medplum configuration as code** and applies it via an MCP (Model Context Protocol) server.

## What MCP is used for
Use the MCP server for Medplum administrative and configuration changes, including:
- Projects, ClientApplications, AccessPolicies, ProjectMemberships
- Enabling project features (e.g., bots/cron/transaction-bundles)
- Creating/updating Bots, Subscriptions, StructureDefinitions/Profiles
- Project/system settings and secrets

## What MCP is NOT required for
Normal application runtime operations (read/write FHIR resources) can use the backend’s standard HTTP client and OAuth2 tokens.

## Operational rules
1) **MCP-first:** If you need to change the Medplum instance, use the MCP tooling.
2) **Discover tool names:** The exact MCP tool names vary by server implementation. Use MCP introspection/discovery to list available tools before attempting mutations.
3) **No manual console drift:** Avoid one-off edits in the Medplum App UI for things that should be reproducible. Prefer committing JSON templates to the repo and applying via MCP.
4) **Secrets:** Never commit secrets. Treat the MCP client credentials as privileged.

## References
- Medplum MCP integration docs: Medplum provides an official MCP endpoint for hosted instances; Starvit uses a custom MCP server for the self-hosted environment.
