from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

from app.core.config import settings
from app.modules.deid.job_runner import DeidJobResult

SAFE_APP_ENVS = {"dev", "test", "local"}


@dataclass(frozen=True)
class DeidBQPayload:
    observation_rows: List[Dict[str, object]]
    run_metadata: Dict[str, object]


class DeidBQStubSink:
    def build_payload(self, result: DeidJobResult) -> DeidBQPayload:
        self._assert_safe_environment()

        rows: List[Dict[str, object]] = [
            {
                "observation_id": record.observation_id,
                "patient_key": record.patient_key,
                "effective_at": record.effective_at,
                "code_system": record.code_system,
                "code": record.code,
                "value": record.value,
                "unit": record.unit,
                "run_id": record.run_id,
                "transform_version": record.transform_version,
                "policy_version": record.policy_version,
            }
            for record in result.output_records
        ]

        now = datetime.now(tz=timezone.utc).isoformat()
        run_metadata = {
            "run_id": result.run_id,
            "started_at": now,
            "completed_at": now,
            "input_count": result.input_count,
            "output_count": result.output_count,
            "transform_version": result.transform_version,
            "policy_version": result.policy_version,
            "source_system": "synthetic",
            "code_hash": "stub",
            "config_hash": "stub",
        }

        return DeidBQPayload(observation_rows=rows, run_metadata=run_metadata)

    def _assert_safe_environment(self) -> None:
        if settings.APP_ENV not in SAFE_APP_ENVS:
            raise RuntimeError("De-id stub blocked outside dev/test/local environments")
        if settings.STARVIT_MODE != "stub":
            raise RuntimeError("De-id stub requires STARVIT_MODE=stub")
