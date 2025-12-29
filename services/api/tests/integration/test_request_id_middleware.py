from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def test_request_id_header_added(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    client = TestClient(app)

    resp = client.get("/health")
    assert resp.status_code == 200
    assert "X-Request-Id" in resp.headers


def test_request_id_passthrough(monkeypatch):
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")
    client = TestClient(app)

    resp = client.get("/health", headers={"X-Request-Id": "req-test"})
    assert resp.status_code == 200
    assert resp.headers.get("X-Request-Id") == "req-test"
