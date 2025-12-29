from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

from app.core.authz import Role, UserContext

AUDIT_EVENT_TYPE_SYSTEM = "http://terminology.hl7.org/CodeSystem/audit-event-type"
AUDIT_EVENT_SUBTYPE_SYSTEM = "urn:starvit:audit-subtype"
AUDIT_EVENT_ROLE_SYSTEM = "urn:starvit:role"
AUDIT_EVENT_REQUEST_ID_URL = "urn:starvit:audit:request-id"
STARVIT_SYSTEM_ID = "urn:starvit:system"

ALLOWED_ACTIONS = {"C", "U", "R", "D", "E"}


@dataclass(frozen=True)
class AuditActor:
    reference: Optional[str]
    identifier_system: str
    identifier_value: str
    role_code: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_actor(actor: UserContext) -> AuditActor:
    role_code = actor.role.value if isinstance(actor.role, Role) else str(actor.role)
    if actor.profile:
        return AuditActor(
            reference=actor.profile,
            identifier_system="urn:starvit:user-sub",
            identifier_value=actor.sub,
            role_code=role_code,
        )
    return AuditActor(
        reference=None,
        identifier_system="urn:starvit:user-sub",
        identifier_value=actor.sub,
        role_code=role_code,
    )


def build_audit_event(
    *,
    action: str,
    actor: UserContext,
    resource_refs: Iterable[str],
    request_id: str,
    subtype: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"Unsupported audit action: {action}")

    audit_actor = _build_actor(actor)
    agent: dict = {
        "requestor": True,
        "role": [
            {
                "coding": [
                    {
                        "system": AUDIT_EVENT_ROLE_SYSTEM,
                        "code": audit_actor.role_code,
                    }
                ]
            }
        ],
    }
    if audit_actor.reference:
        agent["who"] = {"reference": audit_actor.reference}
    else:
        agent["who"] = {
            "identifier": {
                "system": audit_actor.identifier_system,
                "value": audit_actor.identifier_value,
            }
        }

    entities = [{"what": {"reference": ref}} for ref in resource_refs if ref]

    event: dict = {
        "resourceType": "AuditEvent",
        "type": {
            "system": AUDIT_EVENT_TYPE_SYSTEM,
            "code": "rest",
            "display": "Restful Operation",
        },
        "action": action,
        "recorded": _now_iso(),
        "outcome": "0",
        "agent": [agent],
        "source": {
            "observer": {
                "identifier": {
                    "system": STARVIT_SYSTEM_ID,
                    "value": "starvit-api",
                }
            }
        },
        "entity": entities,
        "extension": [
            {
                "url": AUDIT_EVENT_REQUEST_ID_URL,
                "valueString": request_id,
            }
        ],
    }

    if subtype:
        event["subtype"] = [
            {
                "system": AUDIT_EVENT_SUBTYPE_SYSTEM,
                "code": subtype,
                "display": description or subtype,
            }
        ]

    if description:
        event["text"] = {
            "status": "generated",
            "div": f"<div>{description}</div>",
        }

    return event
