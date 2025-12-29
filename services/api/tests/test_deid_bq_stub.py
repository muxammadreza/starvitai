from __future__ import annotations

from app.core.config import settings
from app.modules.deid.bq_stub import DeidBQStubSink
from app.modules.deid.job_runner import DeidJobSpec, DeidStubRunner
from app.modules.deid.transformer import DEFAULT_DEID_POLICY


def _synthetic_observation() -> dict:
    return {
        "resourceType": "Observation",
        "id": "obs-2",
        "subject": {"reference": "Patient/p-2"},
        "effectiveDateTime": "2025-12-29T00:00:00Z",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "104816-4",
                }
            ]
        },
        "valueQuantity": {"value": 1.8, "unit": "mmol/L"},
    }


def test_bq_stub_payload(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation()],
        run_id="run-bq-1",
        policy=DEFAULT_DEID_POLICY,
    )
    result = runner.run(job)

    sink = DeidBQStubSink()
    payload = sink.build_payload(result)

    assert payload.run_metadata["run_id"] == "run-bq-1"
    assert payload.run_metadata["input_count"] == 1
    assert payload.run_metadata["output_count"] == 1
    assert payload.run_metadata["source_system"] == "synthetic"
    assert len(payload.observation_rows) == 1
    row = payload.observation_rows[0]
    assert row["observation_id"] == "obs-2"
    assert row["code"] == "104816-4"
    assert row["unit"] == "mmol/L"


def test_bq_stub_blocks_prod_env(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

    result = DeidStubRunner().run(
        DeidJobSpec(
            source_kind="synthetic",
            records=[_synthetic_observation()],
            run_id="run-bq-2",
        )
    )

    monkeypatch.setattr(settings, "APP_ENV", "prod")
    sink = DeidBQStubSink()

    try:
        sink.build_payload(result)
    except RuntimeError as exc:
        assert "blocked" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError for prod env")
