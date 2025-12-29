from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import HTTPException

from app.adapters import fhir_store
from app.core.authz import UserContext
from app.modules.audit.audit_events import build_audit_event

STARVIT_ACTIVITY_SYSTEM = "urn:starvit:activity"
STARVIT_TASK_SYSTEM = "urn:starvit:task"
STARVIT_TASK_CODE_PROTOCOL_RECOMMENDATION = "protocol-recommendation"
STARVIT_TASK_APPROVAL_REQUIRED_URL = "urn:starvit:task:approval-required"
STARVIT_TASK_PROTOCOL_ID_URL = "urn:starvit:task:protocol-id"
STARVIT_TASK_PROTOCOL_VERSION_URL = "urn:starvit:task:protocol-version"
STARVIT_TASK_PROTOCOL_TITLE_URL = "urn:starvit:task:protocol-title"
STARVIT_TASK_RECOMMENDATION_URL = "urn:starvit:task:recommendation"
STARVIT_TASK_RATIONALE_URL = "urn:starvit:task:recommendation-rationale"
STARVIT_TASK_REQUEST_ID_URL = "urn:starvit:task:request-id"
STARVIT_TASK_DECISION_REASON_URL = "urn:starvit:task:decision-reason"
STARVIT_TASK_APPROVAL_STATUS_URL = "urn:starvit:task:approval-status"
STARVIT_SIGNATURE_TYPE_SYSTEM = "urn:iso-astm:E1762-95:2013"
STARVIT_SIGNATURE_TYPE_CODE = "1.2.840.10065.1.12.1.1"


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _resolve_patient_reference(patient_id: str) -> str:
    if patient_id.startswith("Patient/"):
        return patient_id
    return f"Patient/{patient_id}"


def _build_task_requester(actor: UserContext) -> dict:
    if actor.profile:
        return {"reference": actor.profile}
    return {"identifier": {"system": "urn:starvit:user-sub", "value": actor.sub}}


def _build_task_provenance(
    *,
    task_id: str,
    decision: str,
    actor: UserContext,
    request_id: str,
    reason: Optional[str] = None,
) -> dict:
    who = (
        {"reference": actor.profile}
        if actor.profile
        else {"identifier": {"system": "urn:starvit:user-sub", "value": actor.sub}}
    )
    extensions: list[dict[str, Any]] = [
        {"url": "urn:starvit:provenance:approval-decision", "valueString": decision},
        {"url": "urn:starvit:provenance:request-id", "valueString": request_id},
    ]
    if reason:
        extensions.append({"url": STARVIT_TASK_DECISION_REASON_URL, "valueString": reason})

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
        "signature": [
            {
                "type": [
                    {
                        "system": STARVIT_SIGNATURE_TYPE_SYSTEM,
                        "code": STARVIT_SIGNATURE_TYPE_CODE,
                        "display": "Author's Signature",
                    }
                ],
                "when": _to_utc_iso(datetime.now(timezone.utc)),
                "who": who,
            }
        ],
        "extension": extensions,
    }


def _apply_status_update(task: dict, status: str, status_reason: Optional[str]) -> dict:
    updated = dict(task)
    updated["status"] = status
    if status_reason:
        updated["statusReason"] = {
            "text": status_reason,
        }
    return updated


def build_proposed_action_task(
    *,
    patient_id: str,
    protocol_definition_id: str,
    protocol_definition_version: str,
    protocol_title: Optional[str],
    recommendation: str,
    rationale: Optional[str],
    owner_profile: Optional[str],
    actor: UserContext,
    request_id: str,
) -> dict:
    now = datetime.now(timezone.utc)
    extensions: list[dict[str, Any]] = [
        {"url": STARVIT_TASK_APPROVAL_REQUIRED_URL, "valueBoolean": True},
        {"url": STARVIT_TASK_PROTOCOL_ID_URL, "valueString": protocol_definition_id},
        {"url": STARVIT_TASK_PROTOCOL_VERSION_URL, "valueString": protocol_definition_version},
        {"url": STARVIT_TASK_RECOMMENDATION_URL, "valueString": recommendation},
        {"url": STARVIT_TASK_REQUEST_ID_URL, "valueString": request_id},
    ]
    if protocol_title:
        extensions.append({"url": STARVIT_TASK_PROTOCOL_TITLE_URL, "valueString": protocol_title})
    if rationale:
        extensions.append({"url": STARVIT_TASK_RATIONALE_URL, "valueString": rationale})

    canonical = f"urn:starvit:protocol-definition:{protocol_definition_id}|{protocol_definition_version}"
    task = {
        "resourceType": "Task",
        "status": "requested",
        "intent": "proposal",
        "code": {
            "coding": [
                {
                    "system": STARVIT_TASK_SYSTEM,
                    "code": STARVIT_TASK_CODE_PROTOCOL_RECOMMENDATION,
                    "display": "Protocol recommendation",
                }
            ]
        },
        "description": recommendation,
        "authoredOn": _to_utc_iso(now),
        "requester": _build_task_requester(actor),
        "for": {"reference": _resolve_patient_reference(patient_id)},
        "instantiatesCanonical": canonical,
        "extension": extensions,
    }
    if owner_profile:
        task["owner"] = {"reference": owner_profile}
    return task


async def create_proposed_action_task(
    *,
    patient_id: str,
    protocol_definition_id: str,
    protocol_definition_version: str,
    protocol_title: Optional[str],
    recommendation: str,
    rationale: Optional[str],
    owner_profile: Optional[str],
    token: Optional[str],
    actor: UserContext,
    request_id: str,
) -> dict:
    task = build_proposed_action_task(
        patient_id=patient_id,
        protocol_definition_id=protocol_definition_id,
        protocol_definition_version=protocol_definition_version,
        protocol_title=protocol_title,
        recommendation=recommendation,
        rationale=rationale,
        owner_profile=owner_profile,
        actor=actor,
        request_id=request_id,
    )
    task_res = await fhir_store.create_resource("Task", task, token=token)

    audit_event = build_audit_event(
        action="C",
        actor=actor,
        resource_refs=[f"Task/{task_res.get('id')}", task_res.get("instantiatesCanonical")],
        request_id=request_id,
        subtype="clinician-approval-proposal",
        description="Clinician approval task proposed",
    )
    await fhir_store.create_resource("AuditEvent", audit_event, token=token)

    return task_res


async def list_pending_tasks(
    *,
    token: Optional[str],
    patient_id: Optional[str] = None,
) -> list[dict]:
    search_params: dict[str, Any] = {
        "status": "requested",
        "intent": "proposal",
        "code": f"{STARVIT_TASK_SYSTEM}|{STARVIT_TASK_CODE_PROTOCOL_RECOMMENDATION}",
        "_sort": "-authored-on",
    }
    if patient_id:
        search_params["patient"] = _resolve_patient_reference(patient_id)

    return await fhir_store.search_resources("Task", search_params, token=token)


async def get_task_decision_log(
    *,
    task_id: str,
    token: Optional[str],
) -> dict:
    task = await fhir_store.read_resource("Task", task_id, token=token)
    provenance = await fhir_store.search_resources("Provenance", {"target": f"Task/{task_id}"}, token=token)
    audit_events = await fhir_store.search_resources("AuditEvent", {"entity": f"Task/{task_id}"}, token=token)
    return {
        "task": task,
        "provenance": provenance,
        "auditEvents": audit_events,
    }


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

    current_status = task.get("status")
    if current_status and current_status not in {"requested", "in-progress", "ready"}:
        raise HTTPException(status_code=409, detail="Task already finalized")

    status = "completed" if decision == "approve" else "rejected"
    updated_task = _apply_status_update(task, status, reason)
    extensions = list(updated_task.get("extension") or [])
    extensions.append({"url": STARVIT_TASK_APPROVAL_STATUS_URL, "valueString": status})
    if reason:
        extensions.append({"url": STARVIT_TASK_DECISION_REASON_URL, "valueString": reason})
    updated_task["extension"] = extensions

    task_res = await fhir_store.update_resource("Task", task_id, updated_task, token=token)

    provenance = _build_task_provenance(
        task_id=task_id,
        decision=decision,
        actor=actor,
        request_id=request_id,
        reason=reason,
    )
    provenance_res = await fhir_store.create_resource("Provenance", provenance, token=token)

    audit_event = build_audit_event(
        action="U",
        actor=actor,
        resource_refs=[f"Task/{task_id}", f"Provenance/{provenance_res.get('id')}"],
        request_id=request_id,
        subtype=f"clinician-approval-{decision}",
        description="Clinician approval decision recorded",
    )
    await fhir_store.create_resource("AuditEvent", audit_event, token=token)

    return task_res
