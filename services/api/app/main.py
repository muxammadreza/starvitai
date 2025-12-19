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

@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    # Skip auth for health check
    if request.url.path == "/health":
        return await call_next(request)
        
    api_key = request.headers.get("X-API-KEY")
    if not api_key or api_key != settings.STARVIT_API_KEY:
        from fastapi import Response
        return Response(content="Unauthorized", status_code=401)
        
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
async def post_measurements(data: MeasurementInput):
    result = await write_observation_glucose_ketone_weight(
        data.patientId, 
        data.model_dump(exclude_none=True)
    )
    return {"status": "received", "fhir_id": result.get("id")}

# Clinician Endpoints (Stub)
@app.get("/api/clinician/patients")
def get_patients():
    return [{"id": "p1", "name": "Stub Patient"}]

# Research Endpoints (Stub)
class GraphQuerySync(BaseModel):
    query: str
    params: dict

@app.post("/api/research/graph/query")
async def query_graph(q: GraphQuerySync):
    # Enforce allowlist check here in real implementation
    return await graph_store.execute_query(q.query, q.params)
