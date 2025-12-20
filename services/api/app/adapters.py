import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings

logger = logging.getLogger("starvit-adapters")

# --- Interfaces (Ports) ---

class FhirStore(ABC):
    @abstractmethod
    async def create_resource(self, resource_type: str, data: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def search_resources(self, resource_type: str, search_params: Dict[str, Any], token: Optional[str] = None) -> List[Dict[str, Any]]:
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
        
        # Check config strictly? No, main.py checks minimal config.
        # But we can check self.client_secret before use.

    async def _get_token(self):
        if settings.STARVIT_MODE == "stub":
            return "stub-token"

        # LIVE MODE
        if not self.client_secret:
            logger.error("Attempted PHI write without MEDPLUM_CLIENT_SECRET")
            raise NotImplementedError("Medplum writer configuration missing (CLIENT_SECRET)")

        # Implement real OAuth flow logic here or fail
        if not self.token:
             # Placeholder for real logic
             pass
        
        raise NotImplementedError("Medplum live auth not implemented")

    async def create_resource(self, resource_type: str, data: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        if settings.STARVIT_MODE == "stub":
             logger.info(f"[MedplumStore STUB] POST {resource_type}") # No PHI in logs
             return {"id": "stub-id", "resourceType": resource_type, **data, "mode": "stub"}
        
        if not token:
             raise NotImplementedError("Medplum live write requires user token")
             
        url = f"{self.base_url}/fhir/R4/{resource_type}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=data, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Medplum error: {e.response.text}")
                raise

    async def search_resources(self, resource_type: str, search_params: Dict[str, Any], token: Optional[str] = None) -> List[Dict[str, Any]]:
        if settings.STARVIT_MODE == "stub":
            logger.info(f"[MedplumStore STUB] GET {resource_type} params={search_params}")
            return [{"resourceType": resource_type, "id": "stub-search", "mode": "stub"}]

        if not token:
             # If we are in LIVE mode, we MUST have a user token for PHI access.
             # We do NOT use a service token for general searches to avoid PHI leakage.
             raise NotImplementedError("Medplum live search requires user token")

        url = f"{self.base_url}/fhir/R4/{resource_type}"
        headers = {
             "Authorization": f"Bearer {token}",
             "Content-Type": "application/fhir+json"
        }
        
        async with httpx.AsyncClient() as client:
             try:
                 resp = await client.get(url, params=search_params, headers=headers)
                 resp.raise_for_status()
                 data = resp.json()
                 # FHIR Bundle handling
                 if "entry" in data:
                     return [e["resource"] for e in data["entry"]]
                 return []
             except httpx.HTTPStatusError as e:
                 logger.error(f"Medplum search error: {e.response.text}")
                 raise e

class TigerGraphStore(GraphStore):
    def __init__(self):
        self.base_url = settings.GRAPH_STORE_URL.rstrip('/') if settings.GRAPH_STORE_URL else ""
        self.token = settings.GRAPH_STORE_TOKEN

    async def execute_query(self, query_name: str, params: Dict[str, Any]) -> Any:
        if settings.STARVIT_MODE == "stub":
            logger.info(f"[TigerGraphStore STUB] Query {query_name}")
            return {
                "results": [{"stub": "result", "query": query_name}],
                "mode": "stub"
            }

        # LIVE MODE (Savanna)
        api_base = settings.TG_SAVANNA_API_BASE
        api_key = settings.TG_SAVANNA_API_KEY
        
        if not api_base or not api_key:
             raise NotImplementedError("TigerGraph Savanna config (API_BASE, API_KEY) missing for LIVE mode")
             
        # Savanna REST API structure for custom queries:
        # POST {api_base}/query/{graph_name}/{query_name}
        # But commonly managed services expose endpoints like:
        # https://<domain>/restpp/query/<graph_name>/<query_name>
        # We assume TG_SAVANNA_API_BASE is the full base up to /restpp or equivalent.
        # If the user provides "https://api.tgcloud.io/v4/...", we append accordingly.
        
        # Construct URL (assuming standard TigerGraph REST++ endpoint structure)
        # We might need a graph name in config, or assume "StarvitGraph" or similar.
        # For now, we append /query/{query_name} to the base.
        url = f"{api_base.rstrip('/')}/query/{query_name}"
        
        headers = {
             "x-api-key": api_key,
             "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
             try:
                 # TG queries usually take params as query args (GET) or JSON body (POST).
                 # We prefer POST for complex params.
                 resp = await client.post(url, json=params, headers=headers, timeout=10.0)
                 resp.raise_for_status()
                 return resp.json()
             except httpx.HTTPStatusError as e:
                 logger.error(f"TigerGraph Savanna error: {e.response.text}")
                 raise e
             except Exception as e:
                 logger.error(f"TigerGraph connection error: {e}")
                 raise e

class PostgresAnalyticsStore(AnalyticsStore):
    def __init__(self):
        self.conn_str = settings.ANALYTICS_STORE_URL

    async def query_cohort(self, cohort_def: Dict[str, Any]):
        if settings.STARVIT_MODE == "stub":
            logger.info("[AnalyticsStore STUB] Cohort Query")
            return {"count": 100, "mode": "stub"}
        
        # LIVE MODE
        if not self.conn_str:
            raise NotImplementedError("ANALYTICS_STORE_URL missing for LIVE mode")

        raise NotImplementedError("Analytics live query not implemented")

# --- Singleton Instances ---
fhir_store = MedplumStore()
graph_store = TigerGraphStore()
analytics_store = PostgresAnalyticsStore()
