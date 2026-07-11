"""
EQUIDX AI — Biosensor Simulator microservice.

Generates realistic synthetic biosensor signals over REST (single waveform
pull) and WebSocket (live streaming, e.g. for a device-connection demo in
the dashboard). No real hardware or patient data is involved anywhere here.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

from simulator.device_profiles import PROFILES
from simulator.signal_generator import generate_waveform

app = FastAPI(
    title="EQUIDX AI — Biosensor Simulator",
    description="Generates synthetic biosensor signals for demo/prototype purposes only.",
    version="0.1.0",
)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


class WaveformRequest(BaseModel):
    sample_type: str
    duration_sec: float = 10.0
    seed: int | None = None


@app.get("/health")
async def health():
    return {"status": "ok", "service": "equidx-biosensor-simulator"}


@app.get("/api/v1/devices")
async def list_devices():
    return {k: v.name for k, v in PROFILES.items()}


@app.post("/api/v1/waveform")
async def waveform(payload: WaveformRequest):
    return generate_waveform(payload.sample_type, payload.duration_sec, payload.seed)


@app.websocket("/ws/stream/{sample_type}")
async def stream(websocket: WebSocket, sample_type: str):
    """Streams a new short waveform chunk roughly once a second — a stand-in
    for a device pushing live readings to the dashboard."""
    await websocket.accept()
    import asyncio

    try:
        tick = 0
        while True:
            chunk = generate_waveform(sample_type, duration_sec=1.0, seed=tick)
            await websocket.send_json(chunk)
            tick += 1
            await asyncio.sleep(1.0)
    except WebSocketDisconnect:
        pass
