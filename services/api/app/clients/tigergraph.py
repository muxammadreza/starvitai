from app.core.config import settings

class TigerGraphClient:
    def execute_query(self, query_name: str, params: dict):
        # Stub implementation - printing real auth header intent
        # In real impl: headers = {"Authorization": f"Bearer {settings.GRAPH_STORE_TOKEN}"}
        print(f"STUB: Executing TigerGraph query {query_name} with Bearer Auth (Token len={len(settings.GRAPH_STORE_TOKEN) if hasattr(settings, 'GRAPH_STORE_TOKEN') and settings.GRAPH_STORE_TOKEN else 0})")
        return {"results": []}

tigergraph_client = TigerGraphClient()
