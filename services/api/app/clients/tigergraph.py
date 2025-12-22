import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class TigerGraphClient:
    def execute_query(self, query_name: str, params: dict):
        if settings.STARVIT_MODE == "stub":
            logger.warning(f"STUB: Executing TigerGraph query {query_name} (Mode: stub)")
            return {
                "mode": "stub",
                "query": query_name,
                "results": [{"id": "stub_node_1", "type": "Patient", "attributes": {"mock": True}}],
            }

        # LIVE MODE - Real Implementation
        token = settings.GRAPH_STORE_TOKEN
        url = settings.GRAPH_STORE_URL

        if not token or not url:
            raise RuntimeError("GRAPH_STORE configuration missing in live mode")

        # In a real implementation, we would use httpx or similar here
        # For now, we raise NotImplementedError if the real client isn't fully coded,
        # OR we leave the print but fail if connection fails.
        # Requirement: "live: any unimplemented integration must fail closed (HTTP 501)"

        # Simulating "Unimplemented Real Client" for MVP skeleton if actual HTTP logic isn't here yet.
        # But let's look at what was there: just a print.
        # So in LIVE mode, since we haven't written the real HTTP code yet, we MUST fail.

        raise NotImplementedError("TigerGraph live integration not yet implemented")


tigergraph_client = TigerGraphClient()
