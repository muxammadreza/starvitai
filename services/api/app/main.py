from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.modules.phi_gateway.fhir_writer import write_observation_glucose_ketone_weight
from app.clients.tigergraph import tigergraph_client

app = FastAPI(title="Starvit API")

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
def query_graph(q: GraphQuerySync):
    # Enforce allowlist check here in real implementation
    return tigergraph_client.execute_query(q.query, q.params)
