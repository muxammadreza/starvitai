import pytest

from app.adapters import fhir_store, MedplumFhirStore
from app.core.config import settings
from app.modules.phi_gateway.fhir_writer import MeasurementInput, MeasurementQuantity, calculate_gki, write_measurements


# Mock the settings to ensure consistent test state
@pytest.fixture
def mock_settings_stub(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")


@pytest.fixture
def mock_settings_live(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "live")
    # Set required Medplum config for live mode
    monkeypatch.setattr(settings, "MEDPLUM_FHIR_BASE_URL", "https://api.medplum.starvit.ca/fhir/R4")


@pytest.mark.asyncio
async def test_gki_calculation_stub():
    # Test GKI logic (using Stub mode store so no network calls)

    class MockStore:
        async def create_resource(self, resource_type, data, token=None):
            return {"id": "stub-id", **data}  # Return payload with an ID

    # Swap the store instance
    original_store = fhir_store.create_resource
    fhir_store.create_resource = MockStore().create_resource

    payload = MeasurementInput(
        patientId="p123",
        measuredAt="2025-12-01T08:30:00-05:00",
        glucose=MeasurementQuantity(value=5.0, unit="mmol/L"),
        ketones=MeasurementQuantity(value=1.0, unit="mmol/L"),
    )
    result = await write_measurements("p123", payload, token=None)

    # Check components
    assert result["gki_id"] is not None
    assert calculate_gki(5.0, 1.0) == 5.0

    # Test GKI logic with different values
    assert calculate_gki(4.0, 2.0) == 2.0

    # Restore
    fhir_store.create_resource = original_store


@pytest.mark.asyncio
async def test_live_mode_requires_token(mock_settings_live):
    store = MedplumFhirStore()

    # Should raise NotImplementedError if no token provided in live mode
    with pytest.raises(NotImplementedError):
        await store.search_resources("Patient", {})

    with pytest.raises(NotImplementedError):
        await store.create_resource("Patient", {})
