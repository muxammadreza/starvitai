import httpx
from app.core.config import settings

class MedplumClient:
    def __init__(self):
        self.base_url = settings.MEDPLUM_BASE_URL
        self.token = None

    async def get_token(self):
        # Stub: Implement proper OAuth2 client credentials flow
        # resp = await httpx.post(...)
        self.token = "stub-token"
        return self.token

    async def create_observation(self, resource: dict):
        if not self.token:
            await self.get_token()
        
        # Real implementation would POST to /fhir/R4/Observation
        # async with httpx.AsyncClient() as client:
        #     return await client.post(...)
        # print(f"STUB: Creating observation in Medplum: {resource}") # REMOVED for PHI safety
        return {"id": "stub-id", "resourceType": "Observation"}

medplum_client = MedplumClient()
