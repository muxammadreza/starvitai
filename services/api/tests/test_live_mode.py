import pytest
from app.core.config import settings
from app.modules.phi_gateway.fhir_writer import write_observation_glucose_ketone_weight
from app.adapters import fhir_store

# Mock the settings to ensure consistent test state
@pytest.fixture
def mock_settings_stub(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

@pytest.fixture
def mock_settings_live(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "live")
    monkeypatch.setattr(settings, "MEDPLUM_BASE_URL", "http://mock-medplum/")

@pytest.mark.asyncio
async def test_gki_calculation_stub():
    # Test GKI logic (using Stub mode store so no network calls)
    # Stub store just returns the Observation object in a wrapped response usually, 
    # but let's check what write_observation returns.
    # In stub mode, MedplumStore.create_resource returns {..., "mode": "stub"}
    
    # We really want to verify the logic inside `write_observation` before it calls store.
    # But since we can't easily intercept without mocking the store, let's mock the store's create_resource.
    
    class MockStore:
        async def create_resource(self, resource_type, data, token=None):
            return data # Return the payload for inspection

    # Swap the store instance
    original_store = fhir_store.create_resource
    fhir_store.create_resource = MockStore().create_resource
    
    data = {"glucose": "5.0", "ketones": "1.0"}
    result = await write_observation_glucose_ketone_weight("p123", data)
    
    # Check components
    comps = result["component"]
    gki_comp = next((c for c in comps if c["code"].get("text") == "GKI"), None)
    assert gki_comp is not None
    assert gki_comp["valueQuantity"]["value"] == 5.0
    
    # Test GKI logic with different values
    data2 = {"glucose": "4.0", "ketones": "2.0"}
    result2 = await write_observation_glucose_ketone_weight("p123", data2)
    gki_comp2 = next((c for c in result2["component"] if c["code"].get("text") == "GKI"), None)
    assert gki_comp2 is not None
    assert gki_comp2["valueQuantity"]["value"] == 2.0

    # Restore
    fhir_store.create_resource = original_store

@pytest.mark.asyncio
async def test_live_mode_requires_token(mock_settings_live):
    from app.adapters import MedplumStore
    store = MedplumStore()
    
    # Should raise NotImplementedError if no token provided in live mode
    with pytest.raises(NotImplementedError):
        await store.search_resources("Patient", {})
        
    with pytest.raises(NotImplementedError):
        await store.create_resource("Patient", {})
