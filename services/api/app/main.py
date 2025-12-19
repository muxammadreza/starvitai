from fastapi import FastAPI, HTTPException, Request
from app.core.config import settings
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
        "https://app.starvit.ca",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        # MVP: Decode without signature verification for now (trusting internal gateway/LB or just parsing)
        # TODO: Implement full JWKS signature verification against Medplum's public keys
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception as e:
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

@app.post("/api/research/graph/query")
async def query_graph(q: GraphQuerySync, user: dict = Depends(get_current_user)):
    # Enforce allowlist check here in real implementation
    return await graph_store.execute_query(q.query, q.params)
