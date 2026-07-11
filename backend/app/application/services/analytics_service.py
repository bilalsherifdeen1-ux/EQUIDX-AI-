"""Application-layer facade the backend uses to talk to the standalone
`analytics` microservice for dashboard aggregates."""
from __future__ import annotations

import httpx

from app.core.config import get_settings

settings = get_settings()


class AnalyticsClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "http://analytics:8300"

    async def get_overview(self) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            resp = await client.get("/api/v1/analytics/overview")
            resp.raise_for_status()
            return resp.json()
