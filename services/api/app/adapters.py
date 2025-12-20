import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from app.core.config import settings

logger = logging.getLogger("starvit-adapters")

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

    async def create_resource(self, resource_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if settings.STARVIT_MODE == "stub":
             logger.info(f"[MedplumStore STUB] POST {resource_type}") # No PHI in logs
             return {"id": "stub-id", "resourceType": resource_type, **data, "mode": "stub"}
        
        # token = await self._get_token() # This will raise if secret missing
        url = f"{self.base_url}/fhir/R4/{resource_type}"
        raise NotImplementedError("Medplum live create_resource not implemented")

    async def search_resources(self, resource_type: str, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if settings.STARVIT_MODE == "stub":
            logger.info(f"[MedplumStore STUB] GET {resource_type}")
            return [{"resourceType": resource_type, "id": "stub-search", "mode": "stub"}]

        url = f"{self.base_url}/fhir/R4/{resource_type}"
        raise NotImplementedError("Medplum live search_resources not implemented")

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

        # LIVE MODE
        if not self.base_url or not self.token:
            raise NotImplementedError("GRAPH_STORE config missing for LIVE mode")
            
        url = f"{self.base_url}/query/{query_name}"
        raise NotImplementedError("TigerGraph live execute_query not implemented")

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
