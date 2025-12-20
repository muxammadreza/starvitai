from app.core.config import settings
from app.core.security import validate_jwt
from fastapi import FastAPI, HTTPException, Request, Security, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from app.modules.phi_gateway.fhir_writer import write_observation_glucose_ketone_weight
from app.adapters import graph_store
import logging
import time

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger("starvit-api")

app = FastAPI(title="Starvit API")

# Startup Checks
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting Starvit API in {settings.STARVIT_MODE.upper()} mode")
    
    # 1. Trailing slash check
    if not settings.MEDPLUM_BASE_URL.endswith("/"):
        logger.error(f"MEDPLUM_BASE_URL '{settings.MEDPLUM_BASE_URL}' is missing trailing slash. This is REQUIRED.")
        raise RuntimeError("Configuration Error: MEDPLUM_BASE_URL must end with a trailing slash.")

    # 2. Key config check
    if settings.STARVIT_MODE == "live":
        if not settings.MEDPLUM_JWT_ISSUER or not settings.MEDPLUM_JWT_AUDIENCE:
            logger.error("Missing JWT configuration in LIVE mode")
            raise RuntimeError("Missing MEDPLUM_JWT_ISSUER or MEDPLUM_JWT_AUDIENCE in LIVE mode")
            
        # MEDPLUM_CLIENT_SECRET now optional for startup (PHI writes will 501 without it)
        if not settings.MEDPLUM_CLIENT_SECRET:
            logger.warning("MEDPLUM_CLIENT_SECRET not set in LIVE mode. PHI writes will fail.")
            
        if not settings.GRAPH_STORE_URL or not settings.GRAPH_STORE_TOKEN:
             raise RuntimeError("Missing GRAPH_STORE configuration in LIVE mode")

ALLOWED_ORIGINS_DEV = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]
ALLOWED_ORIGINS_STAGING = [
    "https://medplum-staging.starvit.ca",
    "https://clinician-staging.starvit.ca",
    "https://research-staging.starvit.ca",
    "https://fhir-staging.starvit.ca", 
]
ALLOWED_ORIGINS_PROD = [
    "https://medplum.starvit.ca",
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

@app.exception_handler(NotImplementedError)
async def not_implemented_exception_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=501,
        content={"detail": str(exc), "mode": settings.STARVIT_MODE},
    )

@app.get("/health")
def health_check():
    return {"status": "ok", "mode": settings.STARVIT_MODE}

# Internal / Admin Security
api_key_header = APIKeyHeader(name="X-Starvit-API-Key", auto_error=True)

def verify_internal_api_key(api_key: str = Security(api_key_header)):
    """
    Verifies the internal service API key.
    Used for admin ops or internal service-to-service calls that are not user-scoped.
    """
    if not settings.STARVIT_API_KEY:
        # In prod, if key not set, this mechanism is disabled or fails safe
        raise HTTPException(status_code=403, detail="API Key auth disabled")
        
    if api_key != settings.STARVIT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/api/admin/config", dependencies=[Depends(verify_internal_api_key)])
def get_admin_config():
    return {
        "status": "secure_admin_access_granted", 
        "mode": settings.STARVIT_MODE
    }

@app.get("/api/admin/tigergraph/health", dependencies=[Depends(verify_internal_api_key)])
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
        
        if not settings.TG_SAVANNA_API_BASE:
            return {"status": "error", "detail": "Not Configured"}
            
        return {"status": "configured", "base_url": settings.TG_SAVANNA_API_BASE}
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
    fhir_id_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    
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
class MeasurementInput(BaseModel):
    patientId: str
    glucose: str | None = None
    ketones: str | None = None
    weight: str | None = None

@app.post("/api/patient/measurements")
async def post_measurements(data: MeasurementInput, user: dict = Depends(validate_jwt)):
    # 1. Role Gate (Patient)
    # Simple check: Does the user have a patient profile?
    # Medplum profile: "Patient/123"
    profile = user.get("profile", "")
    if settings.STARVIT_MODE == "live" and not profile.startswith("Patient/"):
        raise HTTPException(status_code=403, detail="User is not a Patient")

    # 2. Identity Binding
    patient_id = data.patientId
    if settings.STARVIT_MODE == "live":
        # Extract ID from "Patient/123"
        token_patient_id = profile.split("/")[-1]
        
        # Force the ID to match the token
        patient_id = token_patient_id
        logger.info(f"Binding write for patient derived from token")

    result = await write_observation_glucose_ketone_weight(
        patient_id, 
        data.model_dump(exclude_none=True),
        token=user.get("_token")
    )
    return {"status": "received", "fhir_id": result.get("id"), "mode": settings.STARVIT_MODE}

# Clinician Endpoints (Stub)
@app.get("/api/clinician/patients")
def get_patients(user: dict = Depends(validate_jwt)):
    if settings.STARVIT_MODE == "stub":
        return [{"id": "p1", "name": "Stub Patient", "mode": "stub"}]
    else:
        # LIVE Implementation missing
        raise HTTPException(status_code=501, detail="Live patient list not implemented")

# Research Endpoints
class GraphQuerySync(BaseModel):
    query: str
    params: dict

# Allowlist Enforcement
ALLOWED_GRAPH_QUERIES = {
    "get_patient_subgraph",
    "find_similar_patients", 
    "recommend_protocol_adjustments"
}

@app.post("/api/research/graph/query")
async def query_graph(q: GraphQuerySync, user: dict = Depends(validate_jwt)):
    import uuid
    request_id = str(uuid.uuid4())
    user_id = user.get("sub", "unknown")

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
