"""
HTTP client the backend uses to call the ai-engine service.

REBUILT: previously this called POST /api/v1/infer with no body (or an
empty features dict), which is why ai-engine always fell back to sampling
a fresh synthetic row per request regardless of the actual sample. Now it
fetches a real biosensor panel first and forwards its readings.
"""
from __future__ import annotations

import httpx

from app.core.config import settings  # AI_ENGINE_BASE_URL, BIOSENSOR_SIMULATOR_BASE_URL


async def get_simulated_panel(sample_type: str, seed: int | None = None) -> dict:
    async with httpx.AsyncClient(base_url=settings.BIOSENSOR_SIMULATOR_BASE_URL, timeout=10.0) as client:
        params = {"sample_type": sample_type}
        if seed is not None:
            params["seed"] = seed
        resp = await client.post("/api/v1/panel", params=params)
        resp.raise_for_status()
        return resp.json()


async def run_inference(sample_type: str, sample_id: str, readings: dict[str, float] | None = None) -> dict:
    async with httpx.AsyncClient(base_url=settings.AI_ENGINE_BASE_URL, timeout=15.0) as client:
        resp = await client.post(
            "/api/v1/infer",
            json={"sample_type": sample_type, "sample_id": sample_id, "readings": readings},
        )
        resp.raise_for_status()
        return resp.json()
