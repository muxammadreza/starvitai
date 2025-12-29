from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional
import hashlib

DEID_STUB_VERSION = "deid-stub-v0"
PSEUDO_SALT = "deid-stub-salt"


@dataclass(frozen=True)
class DeidPolicy:
    version: str
    allowed_resource_types: frozenset[str]


DEFAULT_DEID_POLICY = DeidPolicy(
    version="policy-stub-v0",
    allowed_resource_types=frozenset({"Observation"}),
)


@dataclass(frozen=True)
class DeidRecord:
    observation_id: str
    patient_key: str
    effective_at: str
    code_system: str
    code: str
    value: float
    unit: str
    run_id: str
    transform_version: str
    policy_version: str


class DeidTransformer:
    def __init__(self, policy: DeidPolicy = DEFAULT_DEID_POLICY) -> None:
        self._policy = policy

    @property
    def policy(self) -> DeidPolicy:
        return self._policy

    @property
    def transform_version(self) -> str:
        return DEID_STUB_VERSION

    def transform(self, resources: Iterable[Dict[str, Any]], run_id: str) -> List[DeidRecord]:
        output: List[DeidRecord] = []
        for resource in resources:
            resource_type = resource.get("resourceType")
            if resource_type not in self._policy.allowed_resource_types:
                continue
            if resource_type == "Observation":
                record = self._transform_observation(resource, run_id)
                if record is not None:
                    output.append(record)
        return output

    def _transform_observation(self, resource: Dict[str, Any], run_id: str) -> Optional[DeidRecord]:
        observation_id = resource.get("id")
        subject_ref = (resource.get("subject") or {}).get("reference")
        effective = resource.get("effectiveDateTime")
        coding = ((resource.get("code") or {}).get("coding") or [{}])[0]
        value_quantity = resource.get("valueQuantity") or {}

        if not observation_id or not subject_ref or not effective:
            return None

        code_system = coding.get("system")
        code = coding.get("code")
        value = value_quantity.get("value")
        unit = value_quantity.get("unit")

        if not code_system or not code or value is None or not unit:
            return None

        patient_key = self._pseudonymize(subject_ref)

        return DeidRecord(
            observation_id=str(observation_id),
            patient_key=patient_key,
            effective_at=str(effective),
            code_system=str(code_system),
            code=str(code),
            value=float(value),
            unit=str(unit),
            run_id=run_id,
            transform_version=DEID_STUB_VERSION,
            policy_version=self._policy.version,
        )

    def _pseudonymize(self, value: str) -> str:
        digest = hashlib.sha256(f"{PSEUDO_SALT}:{value}".encode("utf-8")).hexdigest()
        return f"p_{digest[:24]}"
