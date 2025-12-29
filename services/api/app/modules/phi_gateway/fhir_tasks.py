from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException

from app.adapters import fhir_store
from app.core.authz import UserContext
from app.modules.audit.audit_events import build_audit_event

STARVIT_ACTIVITY_SYSTEM = "urn:starvit:activity"


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _build_task_provenance(
    *,
    task_id: str,
    decision: str,
    actor: UserContext,
    request_id: str,
) -> dict:
    who = (
        {"reference": actor.profile}
        if actor.profile
        else {"identifier": {"system": "urn:starvit:user-sub", "value": actor.sub}}
    )
    return {
        "resourceType": "Provenance",
        "target": [{"reference": f"Task/{task_id}"}],
        "recorded": _to_utc_iso(datetime.now(timezone.utc)),
        "activity": {
            "coding": [
                {
                    "system": STARVIT_ACTIVITY_SYSTEM,
                    "code": "clinician-approval",
                    "display": "Clinician approval decision",
                }
            ]
        },
        "agent": [
            {
                "who": who,
                "type": {
                    "coding": [
                        {
                            "system": "urn:starvit:role",
                            "code": actor.role.value,
                        }
                    ]
                },
            }
        ],
        "extension": [
            {"url": "urn:starvit:provenance:approval-decision", "valueString": decision},
            {"url": "urn:starvit:provenance:request-id", "valueString": request_id},
        ],
    }


def _apply_status_update(task: dict, status: str, status_reason: Optional[str]) -> dict:
    updated = dict(task)
    updated["status"] = status
    if status_reason:
        updated["statusReason"] = {
            "text": status_reason,
        }
    return updated


async def transition_task_status(
    *,
    task_id: str,
    decision: str,
    reason: Optional[str],
    token: Optional[str],
    actor: UserContext,
    request_id: str,
) -> dict:
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="decision must be approve or reject")

    task = await fhir_store.read_resource("Task", task_id, token=token)
    if not task.get("id"):
        raise HTTPException(status_code=404, detail="Task not found")

    status = "completed" if decision == "approve" else "rejected"
    updated_task = _apply_status_update(task, status, reason)

    task_res = await fhir_store.update_resource("Task", task_id, updated_task, token=token)

    provenance = _build_task_provenance(
        task_id=task_id,
        decision=decision,
        actor=actor,
        request_id=request_id,
    )
    provenance_res = await fhir_store.create_resource("Provenance", provenance, token=token)

    audit_event = build_audit_event(
        action="U",
        actor=actor,
        resource_refs=[f"Task/{task_id}", f"Provenance/{provenance_res.get('id')}"] ,
        request_id=request_id,
        subtype=f"clinician-approval-{decision}",
        description="Clinician approval decision recorded",
    )
    await fhir_store.create_resource("AuditEvent", audit_event, token=token)

    return task_res
