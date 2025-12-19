class TigerGraphClient:
    def execute_query(self, query_name: str, params: dict):
        print(f"STUB: Executing TigerGraph query {query_name} with {params}")
        return {"results": []}

tigergraph_client = TigerGraphClient()
