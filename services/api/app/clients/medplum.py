import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger("starvit-medplum-client")


async def fetch_auth_me(token: str) -> Dict[str, Any]:
    if not settings.MEDPLUM_AUTH_ME_URL:
        raise RuntimeError("MEDPLUM_AUTH_ME_URL is not configured")

    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(settings.MEDPLUM_AUTH_ME_URL, headers=headers, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
