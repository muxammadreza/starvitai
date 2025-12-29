from __future__ import annotations

from datetime import datetime
from uuid import uuid4

import pytest

from app.modules.phi_gateway import fhir_writer
from app.modules.phi_gateway.fhir_writer import MeasurementInput, MeasurementQuantity


class InMemoryFhirStore:
    def __init__(self) -> None:
        self.storage: dict[str, list[dict]] = {
            "Patient": [],
            "Observation": [],
            "Provenance": [],
        }

    async def create_resource(self, resource_type: str, data: dict, token=None):
        resource = dict(data)
        resource.setdefault("id", str(uuid4()))
        resource["resourceType"] = resource_type
        self.storage.setdefault(resource_type, []).append(resource)
        return resource

    async def search_resources(self, resource_type: str, search_params: dict, token=None):
        resources = list(self.storage.get(resource_type, []))
        patient = search_params.get("patient")
        if patient:
            resources = [r for r in resources if r.get("subject", {}).get("reference") == patient]

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

        date_filter = search_params.get("date")
        if date_filter and isinstance(date_filter, str) and date_filter.startswith("ge"):
            cutoff = datetime.fromisoformat(date_filter[2:])
            resources = [
                r
                for r in resources
                if datetime.fromisoformat(r.get("effectiveDateTime")) >= cutoff
            ]

        sort_key = search_params.get("_sort")
        if sort_key:
            reverse = sort_key.startswith("-")
            resources.sort(
                key=lambda r: datetime.fromisoformat(r.get("effectiveDateTime")),
                reverse=reverse,
            )

        count = int(search_params.get("_count", len(resources)))
        return resources[:count]


@pytest.mark.asyncio
async def test_measurement_roundtrip(monkeypatch):
    store = InMemoryFhirStore()
    monkeypatch.setattr(fhir_writer, "fhir_store", store)

    patient = await store.create_resource("Patient", {"resourceType": "Patient"})
    patient_id = patient["id"]

    payload = MeasurementInput(
        patientId=patient_id,
        measuredAt="2025-12-28T08:30:00-05:00",
        glucose=MeasurementQuantity(value=5.2, unit="mmol/L"),
        ketones=MeasurementQuantity(value=1.3, unit="mmol/L"),
        weight=MeasurementQuantity(value=72.4, unit="kg"),
    )

    result = await fhir_writer.write_measurements(patient_id, payload, token=None)

    assert result["measurement_id"]
    assert result["glucose_id"]
    assert result["ketone_id"]
    assert result["weight_id"]
    assert result["gki_id"]

    measurements = await fhir_writer.get_recent_measurements(patient_id, token=None, days=7, limit=10)
    assert len(measurements) == 1
    record = measurements[0]
    assert record.measurementId == result["measurement_id"]
    assert record.glucose.value == 5.2
    assert record.ketones.value == 1.3
    assert record.weight is not None
    assert record.weight.value == 72.4

    gki_points = await fhir_writer.get_gki_trend(patient_id, token=None, days=7, limit=10)
    assert len(gki_points) == 1
    point = gki_points[0]
    assert point.derivedObservationId == result["gki_id"]
    assert point.gki.value == round(5.2 / 1.3, 2)
    assert set(point.sourceObservationIds) == {result["glucose_id"], result["ketone_id"]}
