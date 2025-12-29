from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def _headers(role: str, profile: str | None = None):
    headers = {
        "Authorization": "Bearer stub-token",
        "X-Starvit-Role": role,
    }
    if profile:
        headers["X-Starvit-Profile"] = profile
    return headers


def test_patient_role_allowed_and_forbidden(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    client = TestClient(app)

    # Allowed: patient measurement write
    resp = client.post(
        "/api/patient/measurements",
        json={"patientId": "p123", "glucose": "5.1", "ketones": "1.2"},
        headers=_headers("patient", "Patient/p123"),
    )
    assert resp.status_code == 200

    # Forbidden: clinician-only PHI endpoint
    resp = client.get("/api/clinician/patients", headers=_headers("patient", "Patient/p123"))
    assert resp.status_code == 403


def test_clinician_role_allowed_and_forbidden(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    client = TestClient(app)

    # Allowed: clinician list
    resp = client.get("/api/clinician/patients", headers=_headers("clinician", "Practitioner/p1"))
    assert resp.status_code == 200

    # Forbidden: patient-only PHI endpoint
    resp = client.post(
        "/api/patient/measurements",
        json={"patientId": "p123", "glucose": "5.1"},
        headers=_headers("clinician", "Practitioner/p1"),
    )
    assert resp.status_code == 403


def test_research_role_allowed_and_forbidden(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    client = TestClient(app)

    # Allowed: research graph query (de-identified)
    resp = client.post(
        "/api/research/graph/query",
        json={"query": "get_patient_subgraph", "params": {"cohort": "anon_123"}},
        headers=_headers("research", "Practitioner/p2"),
    )
    assert resp.status_code == 200

    # Forbidden: PHI endpoint
    resp = client.get("/api/clinician/patients", headers=_headers("research", "Practitioner/p2"))
    assert resp.status_code == 403
