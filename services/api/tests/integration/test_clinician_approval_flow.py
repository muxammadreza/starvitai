from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.modules.phi_gateway import fhir_tasks
from app.modules.protocols import fhir_protocols


class InMemoryFhirStore:
    def __init__(self) -> None:
        self.storage: dict[str, list[dict]] = {
            "Task": [],
            "Provenance": [],
            "AuditEvent": [],
            "PlanDefinition": [],
        }

    async def create_resource(self, resource_type: str, data: dict, token=None):
        resource = dict(data)
        resource.setdefault("id", str(uuid4()))
        resource["resourceType"] = resource_type
        self.storage.setdefault(resource_type, []).append(resource)
        return resource

    async def read_resource(self, resource_type: str, resource_id: str, token=None):
        for resource in self.storage.get(resource_type, []):
            if resource.get("id") == resource_id:
                return resource
        return {"resourceType": resource_type, "id": resource_id}

    async def update_resource(self, resource_type: str, resource_id: str, data: dict, token=None):
        updated = dict(data)
        updated["id"] = resource_id
        updated["resourceType"] = resource_type
        resources = self.storage.setdefault(resource_type, [])
        for idx, resource in enumerate(resources):
            if resource.get("id") == resource_id:
                resources[idx] = updated
                return updated
        resources.append(updated)
        return updated

    async def search_resources(self, resource_type: str, search_params: dict, token=None):
        resources = list(self.storage.get(resource_type, []))

        if resource_type == "Task":
            status = search_params.get("status")
            if status:
                resources = [r for r in resources if r.get("status") == status]

            intent = search_params.get("intent")
            if intent:
                resources = [r for r in resources if r.get("intent") == intent]

            code_filter = search_params.get("code")
            if code_filter:
                allowed = {item.strip() for item in code_filter.split(",") if item.strip()}

                def has_code(resource: dict) -> bool:
                    for coding in resource.get("code", {}).get("coding", []) or []:
                        token = f"{coding.get('system')}|{coding.get('code')}"
                        if token in allowed:
                            return True
                    return False

                resources = [r for r in resources if has_code(r)]

            patient = search_params.get("patient")
            if patient:
                resources = [
                    r for r in resources if r.get("for", {}).get("reference") == patient
                ]

            sort_key = search_params.get("_sort")
            if sort_key:
                reverse = sort_key.startswith("-")
                key = sort_key.lstrip("-")
                if key == "authored-on":
                    resources.sort(
                        key=lambda r: datetime.fromisoformat(r.get("authoredOn")),
                        reverse=reverse,
                    )

        if resource_type == "Provenance":
            target = search_params.get("target")
            if target:
                resources = [
                    r
                    for r in resources
                    if any(t.get("reference") == target for t in r.get("target", []) or [])
                ]

        if resource_type == "AuditEvent":
            entity = search_params.get("entity")
            if entity:
                resources = [
                    r
                    for r in resources
                    if any(e.get("what", {}).get("reference") == entity for e in r.get("entity", []) or [])
                ]

        if resource_type == "PlanDefinition":
            identifier = search_params.get("identifier")
            if identifier:
                system, _, value = identifier.partition("|")
                resources = [
                    r
                    for r in resources
                    if any(
                        ident.get("system") == system and ident.get("value") == value
                        for ident in r.get("identifier", []) or []
                    )
                ]
            version = search_params.get("version")
            if version:
                resources = [r for r in resources if r.get("version") == version]

        return resources


def _headers(role: str, profile: str | None = None):
    headers = {
        "Authorization": "Bearer stub-token",
        "X-Starvit-Role": role,
    }
    if profile:
        headers["X-Starvit-Profile"] = profile
    return headers


def test_clinician_approval_flow_roundtrip(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    store = InMemoryFhirStore()
    monkeypatch.setattr(fhir_tasks, "fhir_store", store)
    monkeypatch.setattr(fhir_protocols, "fhir_store", store)

    client = TestClient(app)

    protocol_payload = {
        "protocolId": "kmt-core",
        "version": "v1",
        "title": "KMT Core Review",
        "status": "active",
        "steps": [
            {
                "stepId": "review",
                "title": "Clinician review",
                "description": "Review metabolic markers",
                "approvalRequired": True,
            }
        ],
    }

    protocol_resp = client.post(
        "/api/clinician/protocols/definitions",
        json=protocol_payload,
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert protocol_resp.status_code == 200
    protocol_definition_id = protocol_resp.json()["protocolDefinitionId"]

    propose_resp = client.post(
        "/api/clinician/approvals/propose",
        json={
            "patientId": "Patient/p123",
            "protocolDefinitionId": protocol_payload["protocolId"],
            "protocolDefinitionVersion": protocol_payload["version"],
            "protocolTitle": protocol_payload["title"],
            "recommendation": "Maintain current regimen; monitor GKI daily",
            "rationale": "Stable ketone trend, no red flags",
        },
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert propose_resp.status_code == 200
    task_id = propose_resp.json()["taskId"]

    queue_resp = client.get(
        "/api/clinician/approvals/queue",
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert queue_resp.status_code == 200
    queue = queue_resp.json()["tasks"]
    assert queue
    assert queue[0]["protocolDefinitionId"] == protocol_payload["protocolId"]
    assert queue[0]["protocolDefinitionVersion"] == protocol_payload["version"]
    assert queue[0]["approvalRequired"] is True

    approve_resp = client.post(
        f"/api/clinician/approvals/{task_id}/approve",
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert approve_resp.status_code == 200

    log_resp = client.get(
        f"/api/clinician/approvals/{task_id}/log",
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert log_resp.status_code == 200
    body = log_resp.json()
    assert body["task"]["status"] == "completed"
    assert body["provenance"]
    assert body["auditEvents"]
    assert protocol_definition_id


def test_backend_service_requires_owner_profile(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    store = InMemoryFhirStore()
    monkeypatch.setattr(fhir_tasks, "fhir_store", store)
    monkeypatch.setattr(fhir_protocols, "fhir_store", store)

    client = TestClient(app)

    resp = client.post(
        "/api/clinician/approvals/propose",
        json={
            "patientId": "Patient/p123",
            "protocolDefinitionId": "kmt-core",
            "protocolDefinitionVersion": "v1",
            "protocolTitle": "KMT Core Review",
            "recommendation": "Maintain current regimen; monitor GKI daily",
            "rationale": "Stable ketone trend, no red flags",
        },
        headers=_headers("backend_service"),
    )
    assert resp.status_code == 400

    ok = client.post(
        "/api/clinician/approvals/propose",
        json={
            "patientId": "Patient/p123",
            "protocolDefinitionId": "kmt-core",
            "protocolDefinitionVersion": "v1",
            "protocolTitle": "KMT Core Review",
            "recommendation": "Maintain current regimen; monitor GKI daily",
            "rationale": "Stable ketone trend, no red flags",
            "ownerProfile": "Practitioner/p1",
        },
        headers=_headers("backend_service"),
    )
    assert ok.status_code == 200
