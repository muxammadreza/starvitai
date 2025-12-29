from __future__ import annotations

from uuid import uuid4

import pytest

from app.core.authz import Role, UserContext
from app.modules.phi_gateway import fhir_tasks


class InMemoryFhirStore:
    def __init__(self) -> None:
        self.storage: dict[str, list[dict]] = {
            "Task": [],
            "Provenance": [],
            "AuditEvent": [],
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
        return list(self.storage.get(resource_type, []))


@pytest.mark.asyncio
async def test_clinician_approval_emits_audit(monkeypatch):
    store = InMemoryFhirStore()
    monkeypatch.setattr(fhir_tasks, "fhir_store", store)

    task = await store.create_resource("Task", {"resourceType": "Task", "status": "requested"})

    actor = UserContext(
        sub="clinician-123",
        profile="Practitioner/p1",
        role=Role.CLINICIAN,
        token="stub",
        access_policy=None,
        project_id=None,
    )

    result = await fhir_tasks.transition_task_status(
        task_id=task["id"],
        decision="approve",
        reason="reviewed",
        token=None,
        actor=actor,
        request_id="req-approve",
    )

    assert result["status"] == "completed"
    audit_events = store.storage.get("AuditEvent", [])
    assert audit_events
    assert audit_events[-1]["action"] == "U"
