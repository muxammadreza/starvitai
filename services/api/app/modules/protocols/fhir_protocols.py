from __future__ import annotations

from typing import Optional

from app.adapters import fhir_store
from app.core.authz import UserContext
from app.modules.audit.audit_events import build_audit_event
from app.modules.protocols.protocol_definition import ProtocolDefinitionSchema, build_protocol_definition_resource


async def create_protocol_definition(
    *,
    schema: ProtocolDefinitionSchema,
    token: Optional[str],
    actor: UserContext,
    request_id: str,
) -> dict:
    resource = build_protocol_definition_resource(schema)
    created = await fhir_store.create_resource("PlanDefinition", resource, token=token)

    audit_event = build_audit_event(
        action="C",
        actor=actor,
        resource_refs=[f"PlanDefinition/{created.get('id')}", resource.get("url")],
        request_id=request_id,
        subtype="protocol-definition-create",
        description="ProtocolDefinition created",
    )
    await fhir_store.create_resource("AuditEvent", audit_event, token=token)
    return created


async def list_protocol_definitions(
    *,
    protocol_id: Optional[str],
    version: Optional[str],
    token: Optional[str],
) -> list[dict]:
    search_params: dict[str, str] = {}
    if protocol_id:
        search_params["identifier"] = f"urn:starvit:protocol|{protocol_id}"
    if version:
        search_params["version"] = version
    return await fhir_store.search_resources("PlanDefinition", search_params, token=token)
