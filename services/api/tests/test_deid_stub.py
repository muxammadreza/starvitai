from __future__ import annotations

from app.core.config import settings
from app.modules.deid.job_runner import DeidJobSpec, DeidStubRunner
from app.modules.deid.transformer import DEFAULT_DEID_POLICY, DEID_STUB_VERSION


def _synthetic_observation() -> dict:
    return {
        "resourceType": "Observation",
        "id": "obs-1",
        "subject": {"reference": "Patient/p-1"},
        "effectiveDateTime": "2025-12-29T00:00:00Z",
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "15074-8",
                }
            ]
        },
        "valueQuantity": {"value": 5.1, "unit": "mmol/L"},
        "note": "synthetic-only fixture",
    }


def test_deid_stub_transforms_synthetic_fixture(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation()],
        run_id="run-1",
        policy=DEFAULT_DEID_POLICY,
    )

    result = runner.run(job)

    assert result.input_count == 1
    assert result.output_count == 1
    assert result.transform_version == DEID_STUB_VERSION
    record = result.output_records[0]
    assert record.patient_key.startswith("p_")
    assert record.patient_key != "Patient/p-1"
    assert record.observation_id == "obs-1"
    assert record.code == "15074-8"
    assert record.unit == "mmol/L"


def test_deid_stub_blocks_non_synthetic_source(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation()],
        run_id="run-2",
    )

    # Manually construct an invalid job to bypass typing constraints.
    job_invalid = job.__class__(
        source_kind="synthetic",
        records=job.records,
        run_id=job.run_id,
        policy=job.policy,
    )
    object.__setattr__(job_invalid, "source_kind", "phi")

    try:
        runner.run(job_invalid)  # type: ignore[arg-type]
    except ValueError as exc:
        assert "synthetic" in str(exc)
    else:
        raise AssertionError("Expected ValueError for non-synthetic source")


def test_deid_stub_blocks_prod_env(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "prod")
    monkeypatch.setattr(settings, "STARVIT_MODE", "stub")

    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation()],
        run_id="run-3",
    )

    try:
        runner.run(job)
    except RuntimeError as exc:
        assert "blocked" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError for prod env")


def test_deid_stub_blocks_live_mode(monkeypatch) -> None:
    monkeypatch.setattr(settings, "APP_ENV", "test")
    monkeypatch.setattr(settings, "STARVIT_MODE", "live")

    runner = DeidStubRunner()
    job = DeidJobSpec(
        source_kind="synthetic",
        records=[_synthetic_observation()],
        run_id="run-4",
    )

    try:
        runner.run(job)
    except RuntimeError as exc:
        assert "STARVIT_MODE" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError for live mode")
