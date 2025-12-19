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
        # Stub: Implement proper OAuth2 client credentials flow
        # In a real implementation, we'd cache the token and refresh if expired
        if self.token:
            return self.token
        
        # Simple basic auth stub for now or mock token
        # Real world: POST /oauth2/token
        self.token = "stub-token" 
        return self.token

    async def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        # await self._get_token()
        # headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}/fhir/R4/{resource_type}"
        print(f"[MedplumStore] POST {url} with {data}")
        # async with httpx.AsyncClient() as client:
        #    resp = await client.post(url, json=data, headers=headers)
        #    resp.raise_for_status()
        #    return resp.json()
        return {"id": "stub-id", "resourceType": resource_type, **data}

    async def search_resources(self, resource_type: str, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/fhir/R4/{resource_type}"
        print(f"[MedplumStore] GET {url} with {search_params}")
        return []

class TigerGraphStore(GraphStore):
    def __init__(self):
        self.base_url = settings.GRAPH_STORE_URL.rstrip('/')
        self.token = settings.GRAPH_STORE_TOKEN

    async def execute_query(self, query_name: str, params: Dict[str, Any]) -> Any:
        url = f"{self.base_url}/query/{query_name}"
        print(f"[TigerGraphStore] POST {url} with {params}")
        # async with httpx.AsyncClient() as client:
        #     # TigerGraph uses GSQL-Token header usually
        #     headers = {"Authorization": f"Bearer {self.token}"}
        #     resp = await client.post(url, json=params, headers=headers)
        #     return resp.json()
        return {"results": [{"stub": "result"}]}

class PostgresAnalyticsStore(AnalyticsStore):
    def __init__(self):
        self.conn_str = settings.ANALYTICS_STORE_URL

    async def query_cohort(self, cohort_def: Dict[str, Any]):
        print(f"[PostgresAnalyticsStore] Processing cohort def: {cohort_def}")
        return None

# --- Singleton Instances ---
fhir_store = MedplumStore()
graph_store = TigerGraphStore()
analytics_store = PostgresAnalyticsStore()
