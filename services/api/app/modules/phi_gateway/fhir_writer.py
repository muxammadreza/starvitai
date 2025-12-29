from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator, model_validator

from app.adapters import fhir_store

UCUM_SYSTEM = "http://unitsofmeasure.org"
LOINC_SYSTEM = "http://loinc.org"
OBSERVATION_CATEGORY_SYSTEM = "http://terminology.hl7.org/CodeSystem/observation-category"
STARVIT_CODE_SYSTEM = "urn:starvit:observation-code"
MEASUREMENT_GROUP_SYSTEM = "urn:starvit:measurement-group"
STARVIT_ACTIVITY_SYSTEM = "urn:starvit:activity"
STARVIT_AGENT_SYSTEM = "urn:starvit:agent"


@dataclass(frozen=True)
class ObservationCode:
    system: str
    code: str
    display: str
    unit: str
    unit_code: str
    category_code: str
    category_display: str
    loinc_code: Optional[str] = None
    loinc_display: Optional[str] = None


GLUCOSE_CODE = ObservationCode(
    system=STARVIT_CODE_SYSTEM,
    code="glucose-blood-mmol",
    display="Blood glucose (mmol/L)",
    unit="mmol/L",
    unit_code="mmol/L",
    category_code="laboratory",
    category_display="Laboratory",
    loinc_code="15074-8",
    loinc_display="Glucose [Moles/volume] in Blood",
)
KETONE_CODE = ObservationCode(
    system=STARVIT_CODE_SYSTEM,
    code="bhb-blood-mmol",
    display="Blood beta-hydroxybutyrate (mmol/L)",
    unit="mmol/L",
    unit_code="mmol/L",
    category_code="laboratory",
    category_display="Laboratory",
    loinc_code="104816-4",
    loinc_display="Beta hydroxybutyrate [Moles/volume] in Blood",
)
WEIGHT_CODE = ObservationCode(
    system=STARVIT_CODE_SYSTEM,
    code="body-weight-kg",
    display="Body weight (kg)",
    unit="kg",
    unit_code="kg",
    category_code="vital-signs",
    category_display="Vital Signs",
    loinc_code="29463-7",
    loinc_display="Body weight",
)
GKI_CODE = ObservationCode(
    system=STARVIT_CODE_SYSTEM,
    code="gki",
    display="Glucose Ketone Index",
    unit="1",
    unit_code="1",
    category_code="laboratory",
    category_display="Laboratory",
)

ALLOWED_UNITS = {
    "glucose": {"mmol/L"},
    "ketones": {"mmol/L"},
    "weight": {"kg"},
}


class MeasurementQuantity(BaseModel):
    value: float = Field(..., gt=0)
    unit: str

    @field_validator("unit")
    @classmethod
    def normalize_unit(cls, value: str) -> str:
        return value.strip()


class MeasurementInput(BaseModel):
    patientId: str = Field(..., min_length=1)
    measuredAt: datetime
    glucose: MeasurementQuantity
    ketones: MeasurementQuantity
    weight: Optional[MeasurementQuantity] = None

    @field_validator("measuredAt")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("measuredAt must include a timezone offset")
        return value

    @model_validator(mode="after")
    def validate_units(self) -> "MeasurementInput":
        if self.glucose.unit not in ALLOWED_UNITS["glucose"]:
            raise ValueError("glucose.unit must be mmol/L")
        if self.ketones.unit not in ALLOWED_UNITS["ketones"]:
            raise ValueError("ketones.unit must be mmol/L")
        if self.weight and self.weight.unit not in ALLOWED_UNITS["weight"]:
            raise ValueError("weight.unit must be kg")
        return self


class MeasurementObservationIds(BaseModel):
    glucose: str
    ketones: str
    weight: Optional[str] = None


class MeasurementWriteResponse(BaseModel):
    status: str
    measurementId: str
    patientId: str
    measuredAt: datetime
    observationIds: MeasurementObservationIds
    gkiObservationId: str
    mode: str


class MeasurementRecord(BaseModel):
    measurementId: str
    measuredAt: datetime
    glucose: MeasurementQuantity
    ketones: MeasurementQuantity
    weight: Optional[MeasurementQuantity] = None
    observationIds: MeasurementObservationIds


class RecentMeasurementsResponse(BaseModel):
    patientId: str
    measurements: List[MeasurementRecord]
    mode: str


class DerivedMetricPoint(BaseModel):
    measurementId: Optional[str]
    measuredAt: datetime
    gki: MeasurementQuantity
    derivedObservationId: str
    sourceObservationIds: List[str]


class DerivedMetricsTrendResponse(BaseModel):
    patientId: str
    metric: str
    points: List[DerivedMetricPoint]
    mode: str


def _to_utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _build_quantity(value: float, code: ObservationCode) -> Dict[str, Any]:
    return {
        "value": value,
        "unit": code.unit,
        "system": UCUM_SYSTEM,
        "code": code.unit_code,
    }


def _build_observation(
    patient_id: str,
    code: ObservationCode,
    measured_at: datetime,
    value: float,
    measurement_id: str,
    derived_from: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    coding = [
        {
            "system": code.system,
            "code": code.code,
            "display": code.display,
        }
    ]
    if code.loinc_code:
        coding.append(
            {
                "system": LOINC_SYSTEM,
                "code": code.loinc_code,
                "display": code.loinc_display or code.display,
            }
        )
    observation: Dict[str, Any] = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": OBSERVATION_CATEGORY_SYSTEM,
                        "code": code.category_code,
                        "display": code.category_display,
                    }
                ]
            }
        ],
        "code": {
            "coding": coding,
            "text": code.display,
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "performer": [{"reference": f"Patient/{patient_id}"}],
        "effectiveDateTime": _to_utc_iso(measured_at),
        "valueQuantity": _build_quantity(value, code),
        "identifier": [
            {
                "system": MEASUREMENT_GROUP_SYSTEM,
                "value": measurement_id,
                "use": "official",
            }
        ],
    }

    if derived_from:
        observation["derivedFrom"] = [{"reference": f"Observation/{obs_id}"} for obs_id in derived_from]

    return observation


def _build_provenance(
    measurement_id: str,
    derived_observation_id: str,
    source_observation_ids: Iterable[str],
) -> Dict[str, Any]:
    return {
        "resourceType": "Provenance",
        "target": [{"reference": f"Observation/{derived_observation_id}"}],
        "recorded": _to_utc_iso(datetime.now(timezone.utc)),
        "activity": {
            "coding": [
                {
                    "system": STARVIT_ACTIVITY_SYSTEM,
                    "code": "derived-metric",
                    "display": "Derived metric calculated",
                }
            ]
        },
        "agent": [
            {
                "who": {
                    "identifier": {
                        "system": STARVIT_AGENT_SYSTEM,
                        "value": "starvit-backend",
                    }
                }
            }
        ],
        "entity": [
            {"role": "source", "what": {"reference": f"Observation/{obs_id}"}}
            for obs_id in source_observation_ids
        ],
        "identifier": [
            {
                "system": MEASUREMENT_GROUP_SYSTEM,
                "value": measurement_id,
                "use": "official",
            }
        ],
    }


def calculate_gki(glucose: float, ketones: float) -> float:
    if ketones <= 0:
        raise ValueError("ketones must be greater than 0 to compute GKI")
    return round(glucose / ketones, 2)


async def write_measurements(
    patient_id: str, payload: MeasurementInput, token: Optional[str]
) -> Dict[str, Any]:
    measurement_id = str(uuid4())

    glucose_obs = _build_observation(
        patient_id,
        GLUCOSE_CODE,
        payload.measuredAt,
        payload.glucose.value,
        measurement_id,
    )
    ketone_obs = _build_observation(
        patient_id,
        KETONE_CODE,
        payload.measuredAt,
        payload.ketones.value,
        measurement_id,
    )

    glucose_res = await fhir_store.create_resource("Observation", glucose_obs, token=token)
    ketone_res = await fhir_store.create_resource("Observation", ketone_obs, token=token)
    glucose_id = glucose_res.get("id")
    ketone_id = ketone_res.get("id")
    if not glucose_id or not ketone_id:
        raise HTTPException(status_code=502, detail="FHIR store did not return Observation IDs")

    weight_res: Optional[Dict[str, Any]] = None
    if payload.weight is not None:
        weight_obs = _build_observation(
            patient_id,
            WEIGHT_CODE,
            payload.measuredAt,
            payload.weight.value,
            measurement_id,
        )
        weight_res = await fhir_store.create_resource("Observation", weight_obs, token=token)

    try:
        gki_value = calculate_gki(payload.glucose.value, payload.ketones.value)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    gki_obs = _build_observation(
        patient_id,
        GKI_CODE,
        payload.measuredAt,
        gki_value,
        measurement_id,
        derived_from=[glucose_id, ketone_id],
    )
    gki_res = await fhir_store.create_resource("Observation", gki_obs, token=token)
    gki_id = gki_res.get("id")
    if not gki_id:
        raise HTTPException(status_code=502, detail="FHIR store did not return derived Observation ID")

    provenance = _build_provenance(
        measurement_id,
        derived_observation_id=gki_id,
        source_observation_ids=[glucose_id, ketone_id],
    )
    await fhir_store.create_resource("Provenance", provenance, token=token)

    return {
        "measurement_id": measurement_id,
        "glucose_id": glucose_id,
        "ketone_id": ketone_id,
        "weight_id": weight_res.get("id") if weight_res else None,
        "gki_id": gki_id,
    }


def _extract_identifier(resource: Dict[str, Any], system: str) -> Optional[str]:
    for ident in resource.get("identifier", []) or []:
        if ident.get("system") == system:
            return ident.get("value")
    return None


def _extract_effective_datetime(resource: Dict[str, Any]) -> datetime:
    value = resource.get("effectiveDateTime")
    if not value:
        raise ValueError("Observation missing effectiveDateTime")
    if isinstance(value, str) and value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    return datetime.fromisoformat(value)


def _extract_code(resource: Dict[str, Any]) -> Optional[str]:
    coding = resource.get("code", {}).get("coding", []) or []
    for entry in coding:
        if entry.get("system") == STARVIT_CODE_SYSTEM:
            return entry.get("code")
    return None


def _extract_quantity(resource: Dict[str, Any]) -> MeasurementQuantity:
    value_quantity = resource.get("valueQuantity") or {}
    return MeasurementQuantity(
        value=float(value_quantity.get("value")),
        unit=str(value_quantity.get("unit")),
    )


def _code_search_param(codes: Iterable[ObservationCode]) -> str:
    return ",".join(f"{code.system}|{code.code}" for code in codes)


async def get_recent_measurements(
    patient_id: str,
    token: Optional[str],
    days: int,
    limit: int,
) -> List[MeasurementRecord]:
    start = datetime.now(timezone.utc) - timedelta(days=days)
    search_params = {
        "patient": f"Patient/{patient_id}",
        "code": _code_search_param([GLUCOSE_CODE, KETONE_CODE, WEIGHT_CODE]),
        "date": f"ge{_to_utc_iso(start)}",
        "_sort": "-date",
        "_count": str(max(limit * 3, limit)),
    }

    observations = await fhir_store.search_resources("Observation", search_params, token=token)

    groups: Dict[str, Dict[str, Any]] = {}
    for obs in observations:
        code = _extract_code(obs)
        if code not in {GLUCOSE_CODE.code, KETONE_CODE.code, WEIGHT_CODE.code}:
            continue

        measurement_id = _extract_identifier(obs, MEASUREMENT_GROUP_SYSTEM) or obs.get("id")
        if not measurement_id:
            continue

        try:
            measured_at = _extract_effective_datetime(obs)
        except ValueError:
            continue

        entry = groups.setdefault(
            measurement_id,
            {
                "measurementId": measurement_id,
                "measuredAt": measured_at,
                "glucose": None,
                "ketones": None,
                "weight": None,
                "observationIds": {"glucose": None, "ketones": None, "weight": None},
            },
        )

        entry["measuredAt"] = measured_at
        quantity = _extract_quantity(obs)
        if code == GLUCOSE_CODE.code:
            entry["glucose"] = quantity
            entry["observationIds"]["glucose"] = obs.get("id")
        elif code == KETONE_CODE.code:
            entry["ketones"] = quantity
            entry["observationIds"]["ketones"] = obs.get("id")
        elif code == WEIGHT_CODE.code:
            entry["weight"] = quantity
            entry["observationIds"]["weight"] = obs.get("id")

    records = []
    for entry in groups.values():
        if not entry["glucose"] or not entry["ketones"]:
            continue
        records.append(
            MeasurementRecord(
                measurementId=entry["measurementId"],
                measuredAt=entry["measuredAt"],
                glucose=entry["glucose"],
                ketones=entry["ketones"],
                weight=entry["weight"],
                observationIds=MeasurementObservationIds(
                    glucose=entry["observationIds"]["glucose"],
                    ketones=entry["observationIds"]["ketones"],
                    weight=entry["observationIds"]["weight"],
                ),
            )
        )

    records.sort(key=lambda record: record.measuredAt, reverse=True)
    return records[:limit]


async def get_gki_trend(
    patient_id: str,
    token: Optional[str],
    days: int,
    limit: int,
) -> List[DerivedMetricPoint]:
    start = datetime.now(timezone.utc) - timedelta(days=days)
    search_params = {
        "patient": f"Patient/{patient_id}",
        "code": _code_search_param([GKI_CODE]),
        "date": f"ge{_to_utc_iso(start)}",
        "_sort": "date",
        "_count": str(limit),
    }

    observations = await fhir_store.search_resources("Observation", search_params, token=token)

    points: List[DerivedMetricPoint] = []
    for obs in observations:
        if _extract_code(obs) != GKI_CODE.code:
            continue

        measurement_id = _extract_identifier(obs, MEASUREMENT_GROUP_SYSTEM)
        try:
            measured_at = _extract_effective_datetime(obs)
        except ValueError:
            continue

        derived_from = []
        for entry in obs.get("derivedFrom", []) or []:
            ref = entry.get("reference") or ""
            if ref.startswith("Observation/"):
                derived_from.append(ref.split("/")[-1])

        points.append(
            DerivedMetricPoint(
                measurementId=measurement_id,
                measuredAt=measured_at,
                gki=_extract_quantity(obs),
                derivedObservationId=obs.get("id"),
                sourceObservationIds=derived_from,
            )
        )

    points.sort(key=lambda point: point.measuredAt)
    return points[:limit]
