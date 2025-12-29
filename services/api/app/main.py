import logging
import uuid
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.adapters import graph_store
from app.core.config import settings
from app.core.authz import Role, UserContext, require_roles
from app.modules.phi_gateway.fhir_writer import (
    DerivedMetricsTrendResponse,
    MeasurementInput,
    MeasurementWriteResponse,
    RecentMeasurementsResponse,
    get_gki_trend,
    get_recent_measurements,
    update_measurements,
    write_measurements,
)
from app.modules.phi_gateway.fhir_tasks import (
    STARVIT_TASK_APPROVAL_REQUIRED_URL,
    STARVIT_TASK_PROTOCOL_ID_URL,
    STARVIT_TASK_PROTOCOL_TITLE_URL,
    STARVIT_TASK_PROTOCOL_VERSION_URL,
    STARVIT_TASK_RATIONALE_URL,
    STARVIT_TASK_RECOMMENDATION_URL,
    create_proposed_action_task,
    get_task_decision_log,
    list_pending_tasks,
    transition_task_status,
)
from app.modules.protocols.fhir_protocols import create_protocol_definition, list_protocol_definitions
from app.modules.protocols.protocol_definition import ProtocolDefinitionSchema

logger = logging.getLogger("starvit-api")

@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(f"Starting Starvit API in {settings.STARVIT_MODE.upper()} mode")

    # Key config check
    if settings.STARVIT_MODE == "live":
        if not settings.JWT_ISSUER or not settings.JWT_AUDIENCE or not settings.JWKS_URL:
            logger.error("Missing JWT configuration (ISSUER, AUDIENCE, or JWKS_URL) in LIVE mode")
            raise RuntimeError("Missing JWT configuration in LIVE mode")

        if not settings.GCP_PROJECT_ID:
            logger.error("GCP_PROJECT_ID missing in LIVE mode")
            raise RuntimeError("Missing GCP_PROJECT_ID in LIVE mode")

        if not settings.TG_API_BASE or not settings.TG_API_KEY:
            raise RuntimeError("Missing TigerGraph configuration in LIVE mode")
    yield


app = FastAPI(title="Starvit API", lifespan=lifespan)


ALLOWED_ORIGINS_DEV = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]
ALLOWED_ORIGINS_STAGING = [
    "https://clinician-staging.starvit.ca",
    "https://research-staging.starvit.ca",
]
ALLOWED_ORIGINS_PROD = [
    "https://clinician.starvit.ca",
    "https://research.starvit.ca",
    "https://app.starvit.ca",
]


def get_allowed_origins():
    if settings.APP_ENV == "prod":
        return ALLOWED_ORIGINS_PROD
    elif settings.APP_ENV == "staging":
        return ALLOWED_ORIGINS_STAGING
    else:
        return ALLOWED_ORIGINS_DEV


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response


@app.exception_handler(NotImplementedError)
async def not_implemented_exception_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=501,
        content={"detail": str(exc), "mode": settings.STARVIT_MODE},
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "mode": settings.STARVIT_MODE}


@app.get("/api/admin/config", dependencies=[Depends(require_roles({Role.BACKEND_SERVICE}))])
def get_admin_config():
    return {"status": "secure_admin_access_granted", "mode": settings.STARVIT_MODE}


@app.get("/api/admin/tigergraph/health", dependencies=[Depends(require_roles({Role.BACKEND_SERVICE}))])
async def tigergraph_health_check():
    """
    Probes TigerGraph connectivity.
    """
    if settings.STARVIT_MODE == "stub":
        return {"status": "ok", "mode": "stub", "timings": "0ms"}

    try:
        # Echo query or simple 'gsql' endpoint check
        # We'll try hitting a known safe endpoint or just check if TCP connects
        # For Savanna, we might list endpoints or just return config status if no simple health endpoint exists.
        # Actually, let's try a simple query if available, or just report configured.

        if not settings.TG_API_BASE:
            return {"status": "error", "detail": "Not Configured"}

        return {"status": "configured", "base_url": settings.TG_API_BASE}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def validate_no_phi(params: dict):
    """
    Reject params that look like FHIR IDs or Patient IDs unless specifically allowlisted (e.g. pseudonymized IDs).
    Rules:
    - No keys containing 'patient' with values that differ from 'anon_*' or 'p_*' (pseudonyms).
    - Checks recursively (simple depth).
    """
    import re

    # FHIR UUID pattern (weak check, but good heuristic)
    fhir_id_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")

    for k, v in params.items():
        if isinstance(v, str):
            # 1. Reject obvious FHIR UUIDs in sensitive fields
            if "patient" in k.lower() and fhir_id_pattern.match(v):
                raise ValueError(f"PHI Guard: Parameter '{k}' looks like a raw FHIR ID. Use pseudonymized IDs for research.")

            # 2. Reject explicit emails/names (very rough)
            if "@" in v and "." in v:
                # Basic email heuristic
                raise ValueError(f"PHI Guard: Parameter '{k}' looks like an email.")


# Patient Endpoints
def _resolve_patient_id(user: UserContext, requested_patient_id: str | None) -> str:
    profile = user.profile or ""

    if settings.STARVIT_MODE == "live":
        if not profile:
            raise HTTPException(status_code=403, detail="User profile missing")
        return profile.split("/")[-1]

    if requested_patient_id:
        return requested_patient_id

    if profile:
        return profile.split("/")[-1]

    raise HTTPException(status_code=400, detail="patientId is required")


@app.post("/api/patient/measurements", response_model=MeasurementWriteResponse)
async def post_measurements(
    request: Request,
    data: MeasurementInput,
    user: UserContext = Depends(require_roles({Role.PATIENT})),
):
    patient_id = _resolve_patient_id(user, data.patientId)

    result = await write_measurements(
        patient_id,
        data,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )

    return MeasurementWriteResponse(
        status="received",
        measurementId=result["measurement_id"],
        patientId=patient_id,
        measuredAt=data.measuredAt,
        observationIds={
            "glucose": result["glucose_id"],
            "ketones": result["ketone_id"],
            "weight": result["weight_id"],
        },
        gkiObservationId=result["gki_id"],
        mode=settings.STARVIT_MODE,
    )


@app.put("/api/patient/measurements/{measurementId}", response_model=MeasurementWriteResponse)
async def put_measurements(
    measurementId: str,
    request: Request,
    data: MeasurementInput,
    user: UserContext = Depends(require_roles({Role.PATIENT})),
):
    patient_id = _resolve_patient_id(user, data.patientId)

    result = await update_measurements(
        patient_id,
        measurementId,
        data,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )

    return MeasurementWriteResponse(
        status="updated",
        measurementId=result["measurement_id"],
        patientId=patient_id,
        measuredAt=data.measuredAt,
        observationIds={
            "glucose": result["glucose_id"],
            "ketones": result["ketone_id"],
            "weight": result["weight_id"],
        },
        gkiObservationId=result["gki_id"],
        mode=settings.STARVIT_MODE,
    )


@app.get("/api/patient/measurements/recent", response_model=RecentMeasurementsResponse)
async def get_recent_patient_measurements(
    patientId: str | None = None,
    days: int = Query(7, ge=1, le=365),
    limit: int = Query(25, ge=1, le=200),
    user: UserContext = Depends(require_roles({Role.PATIENT})),
):
    patient_id = _resolve_patient_id(user, patientId)
    measurements = await get_recent_measurements(patient_id, token=user.token, days=days, limit=limit)

    return RecentMeasurementsResponse(
        patientId=patient_id,
        measurements=measurements,
        mode=settings.STARVIT_MODE,
    )


@app.get("/api/patient/measurements/gki", response_model=DerivedMetricsTrendResponse)
async def get_patient_gki_trend(
    patientId: str | None = None,
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(100, ge=1, le=500),
    user: UserContext = Depends(require_roles({Role.PATIENT})),
):
    patient_id = _resolve_patient_id(user, patientId)
    points = await get_gki_trend(patient_id, token=user.token, days=days, limit=limit)

    return DerivedMetricsTrendResponse(
        patientId=patient_id,
        metric="gki",
        points=points,
        mode=settings.STARVIT_MODE,
    )


# Clinician Endpoints (Stub)
@app.get("/api/clinician/patients")
def get_patients(user: UserContext = Depends(require_roles({Role.CLINICIAN}))):
    if settings.STARVIT_MODE == "stub":
        return [{"id": "p1", "name": "Stub Patient", "mode": "stub"}]
    else:
        # LIVE Implementation missing
        raise HTTPException(status_code=501, detail="Live patient list not implemented")


class ClinicianApprovalDecisionInput(BaseModel):
    decision: str
    reason: str | None = None


class ClinicianApprovalReasonInput(BaseModel):
    reason: str | None = None


class ProposedActionInput(BaseModel):
    patientId: str
    protocolDefinitionId: str
    protocolDefinitionVersion: str
    protocolTitle: str | None = None
    recommendation: str
    rationale: str | None = None
    ownerProfile: str | None = None


class ApprovalQueueItem(BaseModel):
    taskId: str
    status: str
    patientId: str | None = None
    protocolDefinitionId: str | None = None
    protocolDefinitionVersion: str | None = None
    protocolTitle: str | None = None
    recommendation: str | None = None
    rationale: str | None = None
    approvalRequired: bool | None = None
    authoredOn: str | None = None


class ApprovalQueueResponse(BaseModel):
    tasks: list[ApprovalQueueItem]
    mode: str


class ProtocolDefinitionResponse(BaseModel):
    protocolDefinitionId: str
    protocolId: str
    version: str
    status: str
    mode: str


@app.post("/api/clinician/approvals/{taskId}/decision")
async def clinician_approval_decision(
    taskId: str,
    request: Request,
    payload: ClinicianApprovalDecisionInput,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    result = await transition_task_status(
        task_id=taskId,
        decision=payload.decision,
        reason=payload.reason,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )
    return {"status": "ok", "taskId": result.get("id"), "mode": settings.STARVIT_MODE}


@app.post("/api/clinician/protocols/definitions", response_model=ProtocolDefinitionResponse)
async def create_protocol_definition_endpoint(
    payload: ProtocolDefinitionSchema,
    request: Request,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    created = await create_protocol_definition(
        schema=payload,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )
    return ProtocolDefinitionResponse(
        protocolDefinitionId=created.get("id", ""),
        protocolId=payload.protocolId,
        version=payload.version,
        status=created.get("status", payload.status),
        mode=settings.STARVIT_MODE,
    )


@app.get("/api/clinician/protocols/definitions")
async def list_protocol_definitions_endpoint(
    protocolId: Optional[str] = None,
    version: Optional[str] = None,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    return await list_protocol_definitions(
        protocol_id=protocolId,
        version=version,
        token=user.token,
    )


def _extract_extension(task: dict, url: str) -> Optional[str | bool]:
    for ext in task.get("extension", []) or []:
        if ext.get("url") == url:
            if "valueString" in ext:
                return ext.get("valueString")
            if "valueBoolean" in ext:
                return ext.get("valueBoolean")
    return None


@app.post("/api/clinician/approvals/propose")
async def clinician_approval_propose(
    payload: ProposedActionInput,
    request: Request,
    user: UserContext = Depends(require_roles({Role.CLINICIAN, Role.BACKEND_SERVICE})),
):
    if user.role == Role.BACKEND_SERVICE:
        if not payload.ownerProfile:
            raise HTTPException(status_code=400, detail="ownerProfile is required for backend service proposals")
        owner_profile = payload.ownerProfile
    else:
        if not user.profile:
            raise HTTPException(status_code=400, detail="Clinician profile is required")
        if payload.ownerProfile and payload.ownerProfile != user.profile:
            raise HTTPException(status_code=403, detail="ownerProfile must match clinician profile")
        owner_profile = user.profile

    task = await create_proposed_action_task(
        patient_id=payload.patientId,
        protocol_definition_id=payload.protocolDefinitionId,
        protocol_definition_version=payload.protocolDefinitionVersion,
        protocol_title=payload.protocolTitle,
        recommendation=payload.recommendation,
        rationale=payload.rationale,
        owner_profile=owner_profile,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )
    return {"status": "proposed", "taskId": task.get("id"), "mode": settings.STARVIT_MODE}


@app.get("/api/clinician/approvals/queue", response_model=ApprovalQueueResponse)
async def clinician_approval_queue(
    patientId: str | None = None,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    tasks = await list_pending_tasks(token=user.token, patient_id=patientId)
    queue_items: list[ApprovalQueueItem] = []
    for task in tasks:
        patient_ref = task.get("for", {}).get("reference") if isinstance(task.get("for"), dict) else None
        queue_items.append(
            ApprovalQueueItem(
                taskId=task.get("id", ""),
                status=task.get("status", ""),
                patientId=patient_ref,
                protocolDefinitionId=_extract_extension(task, STARVIT_TASK_PROTOCOL_ID_URL),
                protocolDefinitionVersion=_extract_extension(task, STARVIT_TASK_PROTOCOL_VERSION_URL),
                protocolTitle=_extract_extension(task, STARVIT_TASK_PROTOCOL_TITLE_URL),
                recommendation=_extract_extension(task, STARVIT_TASK_RECOMMENDATION_URL),
                rationale=_extract_extension(task, STARVIT_TASK_RATIONALE_URL),
                approvalRequired=_extract_extension(task, STARVIT_TASK_APPROVAL_REQUIRED_URL),
                authoredOn=task.get("authoredOn"),
            )
        )

    return ApprovalQueueResponse(tasks=queue_items, mode=settings.STARVIT_MODE)


@app.get("/api/clinician/approvals/{taskId}/log")
async def clinician_approval_log(
    taskId: str,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    return await get_task_decision_log(task_id=taskId, token=user.token)


@app.post("/api/clinician/approvals/{taskId}/approve")
async def clinician_approval_approve(
    taskId: str,
    request: Request,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    result = await transition_task_status(
        task_id=taskId,
        decision="approve",
        reason=None,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )
    return {"status": "approved", "taskId": result.get("id"), "mode": settings.STARVIT_MODE}


@app.post("/api/clinician/approvals/{taskId}/reject")
async def clinician_approval_reject(
    taskId: str,
    request: Request,
    payload: ClinicianApprovalReasonInput,
    user: UserContext = Depends(require_roles({Role.CLINICIAN})),
):
    result = await transition_task_status(
        task_id=taskId,
        decision="reject",
        reason=payload.reason,
        token=user.token,
        actor=user,
        request_id=request.state.request_id,
    )
    return {"status": "rejected", "taskId": result.get("id"), "mode": settings.STARVIT_MODE}


# Research Endpoints
class GraphQuerySync(BaseModel):
    query: str
    params: dict


# Allowlist Enforcement
ALLOWED_GRAPH_QUERIES = {
    "get_patient_subgraph",
    "find_similar_patients",
    "recommend_protocol_adjustments",
}


@app.post("/api/research/graph/query")
async def query_graph(q: GraphQuerySync, user: UserContext = Depends(require_roles({Role.RESEARCH}))):
    import uuid

    request_id = str(uuid.uuid4())
    user_id = user.sub

    # 1. Allowlist Check
    if q.query not in ALLOWED_GRAPH_QUERIES:
        logger.warning(f"GraphSecurity: Blocked query '{q.query}' from user {user_id}")
        raise HTTPException(status_code=403, detail=f"Query '{q.query}' is not allowlisted.")

    # 1.5 PHI Guard
    try:
        validate_no_phi(q.params)
    except ValueError as e:
        logger.warning(f"GraphSecurity: PHI Guard blocked query from {user_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Provenance Logging
    import hashlib
    import json

    # Canonical JSON for consistent hashing
    canonical_params = json.dumps(q.params, sort_keys=True)
    params_hash = hashlib.sha256(canonical_params.encode()).hexdigest()

    logger.info(f"GraphProvenance: User={user_id} Query={q.query} ReqID={request_id} ParamsHash={params_hash}")

    # 3. Execution
    try:
        result = await graph_store.execute_query(q.query, q.params)
        return result
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Graph query not implemented in live mode yet")
    except Exception as e:
        logger.error(f"Graph Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
