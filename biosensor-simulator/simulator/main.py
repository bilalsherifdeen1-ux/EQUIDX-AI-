"""
EQUIDX AI — Biosensor Simulator service.

REBUILT: exposes one waveform per raw biomarker channel per domain
(see device_profiles.py), not one generic signal per sample_type. Adds
POST /api/v1/panel, the endpoint the backend now calls before every
diagnostic report — see backend's report_service.py / ai_engine_client.py
for the consumer side of this wiring.
"""
from fastapi import FastAPI, HTTPException

from simulator.device_profiles import DOMAIN_CHANNELS
from simulator.signal_generator import generate_panel

app = FastAPI(
    title="EQUIDX AI — Biosensor Simulator",
    description="Synthetic multi-channel biosensor signal generator. Not a physical device.",
    version="0.2.0",
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "equidx-biosensor-simulator", "domains": list(DOMAIN_CHANNELS)}


@app.get("/api/v1/domains")
async def list_domains():
    return {domain: list(channels) for domain, channels in DOMAIN_CHANNELS.items()}


@app.post("/api/v1/panel")
async def panel(sample_type: str, duration_sec: float = 6.0, seed: int | None = None, scenario: str | None = None):
    """
    scenario is only meaningful for hiv_screening: None (random, weighted
    by NAIIS 2018 prevalence), 'non_reactive', 'reactive_concordant', or
    'reactive_discordant' — lets a demo/QA request a specific case
    instead of waiting on a random ~1.4% draw.
    """
    try:
        return generate_panel(sample_type, duration_sec=duration_sec, seed=seed, scenario=scenario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
