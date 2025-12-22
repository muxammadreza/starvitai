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

class GcpHealthcareStore(FhirStore):
    def __init__(self):
        self.project = settings.GCP_PROJECT_ID
        self.location = settings.GCP_LOCATION
        self.dataset = settings.FHIR_DATASET_ID
        self.store = settings.FHIR_STORE_ID
        
        # Base URL for clinical FHIR store
        if self.project and self.location and self.dataset and self.store:
            self.base_url = f"https://healthcare.googleapis.com/v1/projects/{self.project}/locations/{self.location}/datasets/{self.dataset}/fhirStores/{self.store}/fhir"
        else:
            self.base_url = ""

    async def create_resource(self, resource_type: str, data: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        if settings.STARVIT_MODE == "stub":
             logger.info(f"[GcpHealthcareStore STUB] POST {resource_type}")
             return {"id": "stub-id", "resourceType": resource_type, **data, "mode": "stub"}
        
        if not token:
             raise NotImplementedError("GCP Healthcare API write requires user token (OAuth2)")
             
        url = f"{self.base_url}/{resource_type}"
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
                logger.error(f"GCP Healthcare error: {e.response.text}")
                raise e

    async def search_resources(self, resource_type: str, search_params: Dict[str, Any], token: Optional[str] = None) -> List[Dict[str, Any]]:
        if settings.STARVIT_MODE == "stub":
            logger.info(f"[GcpHealthcareStore STUB] GET {resource_type} params={search_params}")
            return [{"resourceType": resource_type, "id": "stub-search", "mode": "stub"}]

        if not token:
             raise NotImplementedError("GCP Healthcare API search requires user token (OAuth2)")

        url = f"{self.base_url}/{resource_type}"
        headers = {
             "Authorization": f"Bearer {token}",
             "Content-Type": "application/fhir+json"
        }
        
        async with httpx.AsyncClient() as client:
             try:
                 resp = await client.get(url, params=search_params, headers=headers)
                 resp.raise_for_status()
                 data = resp.json()
                 if "entry" in data:
                     return [e["resource"] for e in data["entry"]]
                 return []
             except httpx.HTTPStatusError as e:
                 logger.error(f"GCP Healthcare search error: {e.response.text}")
                 raise e

class TigerGraphStore(GraphStore):
    def __init__(self):
        self.api_base = settings.TG_API_BASE
        self.api_key = settings.TG_API_KEY
        self.graph_name = settings.TG_GRAPH_NAME

    async def execute_query(self, query_name: str, params: Dict[str, Any]) -> Any:
        if settings.STARVIT_MODE == "stub":
            logger.info(f"[TigerGraphStore STUB] Query {query_name}")
            return {
                "results": [{"stub": "result", "query": query_name}],
                "mode": "stub"
            }

        if not self.api_base or not self.api_key:
             raise NotImplementedError("TigerGraph Savanna config missing for LIVE mode")
             
        url = f"{self.api_base.rstrip('/')}/query/{self.graph_name}/{query_name}"
        
        headers = {
             "Authorization": f"Bearer {self.api_key}",
             "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
             try:
                 resp = await client.post(url, json=params, headers=headers, timeout=10.0)
                 resp.raise_for_status()
                 return resp.json()
             except httpx.HTTPStatusError as e:
                 logger.error(f"TigerGraph Savanna error: {e.response.text}")
                 raise e

class PostgresAnalyticsStore(AnalyticsStore):
    def __init__(self):
        pass

    async def query_cohort(self, cohort_def: Dict[str, Any]):
        if settings.STARVIT_MODE == "stub":
            logger.info("[AnalyticsStore STUB] Cohort Query")
            return {"count": 100, "mode": "stub"}
        
        raise NotImplementedError("Analytics live query not implemented")

# --- Singleton Instances ---
fhir_store = GcpHealthcareStore()
graph_store = TigerGraphStore()
analytics_store = PostgresAnalyticsStore()
