from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings

# --- Interfaces (Ports) ---

class FhirStore(ABC):
    @abstractmethod
    async def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def search_resources(self, resource_type: str, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

class GraphStore(ABC):
    @abstractmethod
    async def execute_query(self, query_name: str, params: Dict[str, Any]) -> Any:
        pass

class AnalyticsStore(ABC):
    @abstractmethod
    async def query_cohort(self, cohort_def: Dict[str, Any]) -> Any:
        pass

# --- Adapters (Implementation) ---

class MedplumStore(FhirStore):
    def __init__(self):
        self.base_url = settings.MEDPLUM_BASE_URL.rstrip('/')
        self.client_id = settings.MEDPLUM_CLIENT_ID
        self.client_secret = settings.MEDPLUM_CLIENT_SECRET
        self.token = None

    async def _get_token(self):
        if settings.STARVIT_MODE == "stub":
            return "stub-token"

        # LIVE MODE
        # Implement real OAuth flow logic here or fail
        if not self.token:
             # Placeholder for real logic
             pass
        # Failing closed for now if not implemented in live
        # raise NotImplementedError("Medplum live auth not implemented yet") 
        # (Assuming the user wants 'fail closed' for UNIMPLEMENTED things, but we might want to keep the skeletal structure working if possible? 
        # The prompt says: "any unimplemented integration must fail closed (HTTP 501)")
        # So yes, if we haven't written the real code, we fail.
        raise NotImplementedError("Medplum live auth not implemented")

    async def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if settings.STARVIT_MODE == "stub":
             print(f"[MedplumStore STUB] POST {resource_type} {data}")
             return {"id": "stub-id", "resourceType": resource_type, **data, "mode": "stub"}
        
        url = f"{self.base_url}/fhir/R4/{resource_type}"
        # Real implementation would go here
        raise NotImplementedError("Medplum live create_resource not implemented")

    async def search_resources(self, resource_type: str, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if settings.STARVIT_MODE == "stub":
            print(f"[MedplumStore STUB] GET {resource_type} {search_params}")
            return [{"resourceType": resource_type, "id": "stub-search", "mode": "stub"}]

        url = f"{self.base_url}/fhir/R4/{resource_type}"
        raise NotImplementedError("Medplum live search_resources not implemented")

class TigerGraphStore(GraphStore):
    def __init__(self):
        self.base_url = settings.GRAPH_STORE_URL.rstrip('/') if settings.GRAPH_STORE_URL else ""
        self.token = settings.GRAPH_STORE_TOKEN

    async def execute_query(self, query_name: str, params: Dict[str, Any]) -> Any:
        if settings.STARVIT_MODE == "stub":
            print(f"[TigerGraphStore STUB] Query {query_name} Params {params}")
            return {
                "results": [{"stub": "result", "query": query_name}],
                "mode": "stub"
            }

        # LIVE MODE
        if not self.base_url or not self.token:
            raise RuntimeError("GRAPH_STORE config missing for LIVE mode")
            
        url = f"{self.base_url}/query/{query_name}"
        # Real implementation would go here
        raise NotImplementedError("TigerGraph live execute_query not implemented")

class PostgresAnalyticsStore(AnalyticsStore):
    def __init__(self):
        self.conn_str = settings.ANALYTICS_STORE_URL

    async def query_cohort(self, cohort_def: Dict[str, Any]):
        if settings.STARVIT_MODE == "stub":
            print(f"[AnalyticsStore STUB] Cohort {cohort_def}")
            return {"count": 100, "mode": "stub"}
        
        # LIVE MODE
        # Real implementation using asyncpg or sqlalchemy
        raise NotImplementedError("Analytics live query not implemented")

# --- Singleton Instances ---
fhir_store = MedplumStore()
graph_store = TigerGraphStore()
analytics_store = PostgresAnalyticsStore()
