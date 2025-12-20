from app.core.config import settings
from app.core.security import validate_jwt
from fastapi import FastAPI, HTTPException, Request, Security, Depends
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
        logger.warning(f"MEDPLUM_BASE_URL '{settings.MEDPLUM_BASE_URL}' is missing trailing slash. This may cause issues.")
        # We can auto-correct in code, but user requested 'Ensure ... at startup'
    
    # 2. Key config check
    if settings.STARVIT_MODE == "live":
        if not settings.MEDPLUM_JWT_ISSUER or not settings.MEDPLUM_JWT_AUDIENCE:
            logger.error("Missing JWT configuration in LIVE mode")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://admin.starvit.ca",
        "https://clinician.starvit.ca",
        "https://research.starvit.ca",
        "https://app.starvit.ca", # Patient app
        "https://fhir-staging.starvit.ca",
        "https://admin-staging.starvit.ca",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


# Patient Endpoints
class MeasurementInput(BaseModel):
    patientId: str
    glucose: str | None = None
    ketones: str | None = None
    weight: str | None = None

@app.post("/api/patient/measurements")
async def post_measurements(data: MeasurementInput, user: dict = Depends(validate_jwt)):
    # In live mode, ensure we have a valid user from JWT and PHI gateway works
    result = await write_observation_glucose_ketone_weight(
        data.patientId, 
        data.model_dump(exclude_none=True)
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
    request_id = str(time.time()) # Simple ID
    user_id = user.get("sub", "unknown")

    # 1. Allowlist Check
    if q.query not in ALLOWED_GRAPH_QUERIES:
        logger.warning(f"GraphSecurity: Blocked query '{q.query}' from user {user_id}")
        raise HTTPException(status_code=403, detail=f"Query '{q.query}' is not allowlisted.")

    # 2. Provenance Logging
    logger.info(f"GraphProvenance: User={user_id} Query={q.query} ReqID={request_id} ParamsHash={hash(str(q.params))}")

    # 3. Execution
    try:
        result = await graph_store.execute_query(q.query, q.params)
        return result
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Graph query not implemented in live mode yet")
    except Exception as e:
        logger.error(f"Graph Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
