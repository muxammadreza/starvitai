from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Protocol

from app.core.config import settings
from app.modules.deid.transformer import DeidPolicy, DeidRecord, DeidTransformer, DEFAULT_DEID_POLICY

SAFE_APP_ENVS = {"dev", "test", "local"}


@dataclass(frozen=True)
class DeidJobSpec:
    source_kind: Literal["synthetic"]
    records: List[Dict[str, Any]]
    run_id: str
    policy: DeidPolicy = DEFAULT_DEID_POLICY


@dataclass(frozen=True)
class DeidJobResult:
    run_id: str
    output_records: List[DeidRecord]
    input_count: int
    output_count: int
    transform_version: str
    policy_version: str


class JobRunner(Protocol):
    def run(self, job: DeidJobSpec) -> DeidJobResult:
        ...


class DeidStubRunner:
    def __init__(self, transformer: DeidTransformer | None = None) -> None:
        self._transformer = transformer or DeidTransformer()

    def run(self, job: DeidJobSpec) -> DeidJobResult:
        self._assert_safe_environment()
        if job.source_kind != "synthetic":
            raise ValueError("De-id stub only accepts synthetic fixtures")

        transformer = self._transformer
        if job.policy != transformer.policy:
            transformer = DeidTransformer(policy=job.policy)

        records = transformer.transform(job.records, run_id=job.run_id)
        return DeidJobResult(
            run_id=job.run_id,
            output_records=records,
            input_count=len(job.records),
            output_count=len(records),
            transform_version=transformer.transform_version,
            policy_version=transformer.policy.version,
        )

    def _assert_safe_environment(self) -> None:
        if settings.APP_ENV not in SAFE_APP_ENVS:
            raise RuntimeError("De-id stub blocked outside dev/test/local environments")
        if settings.STARVIT_MODE != "stub":
            raise RuntimeError("De-id stub requires STARVIT_MODE=stub")
