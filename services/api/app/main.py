from app.core.config import settings
from fastapi import FastAPI, HTTPException, Request, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from pydantic import BaseModel
from app.modules.phi_gateway.fhir_writer import write_observation_glucose_ketone_weight
from app.adapters import graph_store

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Starvit API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://admin.starvit.ca",
        "https://clinician.starvit.ca",
        "https://research.starvit.ca",
        "https://app.starvit.ca",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth implementation (OAuth2 Resource Server)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
import jwt

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        # 1. Fetch Medplum's public keys
        # Ensure trailing slash logic for JWKS URL construction
        base_url = settings.MEDPLUM_BASE_URL
        if not base_url.endswith("/"):
            base_url += "/"
        jwks_url = f"{base_url}.well-known/jwks.json"
        
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # 2. Decode with strict validation
        # We enforce that 'iss' claim matches our MEDPLUM_BASE_URL exactly.
        # Note: If Medplum issues tokens with a different string, this will fail 401.
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={
                "verify_exp": True,
                "verify_iss": True, 
                "require": ["exp", "iss"],
            },
            issuer=base_url  # Must match exactly
        )
        return payload
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Skip auth for health check and OPTIONS (CORS)
    if request.url.path == "/health" or request.method == "OPTIONS":
        return await call_next(request)
        
    # Validation happens in dependencies for routes, but for global safety 
    # we could check here, OR just rely on Depends(get_current_user) in routes.
    # The user requested removing the specific API Key middleware.
    # We will rely on route dependencies for granularity, but since we have "stub" routes
    # let's protected them globally or adding Depends to them.
    # For now, let's just proceed without the global blocking middleware to allow 
    # Depends to handle 401s more naturally.
    return await call_next(request)
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Internal / Admin Security
api_key_header = APIKeyHeader(name="X-Starvit-API-Key", auto_error=True)

def verify_internal_api_key(api_key: str = Security(api_key_header)):
    """
    Verifies the internal service API key.
    Used for admin ops or internal service-to-service calls that are not user-scoped.
    """
    if api_key != settings.STARVIT_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/api/admin/config", dependencies=[Depends(verify_internal_api_key)])
def get_admin_config():
    """
    Example internal-only endpoint protected by STARVIT_API_KEY.
    """
    return {"status": "secure_admin_access_granted"}


# Patient Endpoints
class MeasurementInput(BaseModel):
    patientId: str
    glucose: str | None = None
    ketones: str | None = None
    weight: str | None = None

@app.post("/api/patient/measurements")
async def post_measurements(data: MeasurementInput, user: dict = Depends(get_current_user)):
    result = await write_observation_glucose_ketone_weight(
        data.patientId, 
        data.model_dump(exclude_none=True)
    )
    return {"status": "received", "fhir_id": result.get("id")}

# Clinician Endpoints (Stub)
@app.get("/api/clinician/patients")
def get_patients(user: dict = Depends(get_current_user)):
    return [{"id": "p1", "name": "Stub Patient"}]

# Research Endpoints (Stub)
class GraphQuerySync(BaseModel):
    query: str
    params: dict

ALLOWED_GRAPH_QUERIES = {
    "get_patient_subgraph",
    "find_similar_patients", 
    "recommend_protocol_adjustments"
}

@app.post("/api/research/graph/query")
async def query_graph(q: GraphQuerySync, user: dict = Depends(get_current_user)):
    if q.query not in ALLOWED_GRAPH_QUERIES:
         raise HTTPException(status_code=403, detail=f"Query '{q.query}' is not allowlisted.")
         
    # Enforce allowlist check here in real implementation
    return await graph_store.execute_query(q.query, q.params)
