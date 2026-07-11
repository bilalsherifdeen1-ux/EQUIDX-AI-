"""
EQUIDX AI — Mobile API (Backend-for-Frontend).

A thin gateway tuned for mobile clients: smaller, flattened payloads,
aggressive caching hints, and endpoints shaped around mobile screens (a
patient-summary card, a sample list, a single "my latest report" call)
rather than the fully general REST surface exposed by `backend/`.

This service holds no business logic of its own — it composes calls to the
core backend API and reshapes the responses.
"""
import os

import httpx
from fastapi import FastAPI, Header, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

app = FastAPI(
    title="EQUIDX AI — Mobile API (BFF)",
    description="Mobile-optimized gateway in front of the core backend API. Research prototype.",
    version="0.1.0",
)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "equidx-mobile-api"}


@app.get("/api/v1/mobile/patients/{patient_id}/summary")
async def patient_summary(patient_id: str, authorization: str = Header(...)):
    headers = {"Authorization": authorization}
    async with httpx.AsyncClient(base_url=BACKEND_URL, timeout=10.0) as client:
        patient_resp = await client.get(f"/api/v1/patients/{patient_id}", headers=headers)
        if patient_resp.status_code != 200:
            raise HTTPException(status_code=patient_resp.status_code, detail="Could not load patient")
        samples_resp = await client.get(f"/api/v1/samples/patient/{patient_id}", headers=headers)

    patient = patient_resp.json()
    samples = samples_resp.json() if samples_resp.status_code == 200 else []
    return {
        "id": patient["id"],
        "name": f"{patient['first_name']} {patient['last_name']}",
        "mrn": patient["mrn"],
        "sample_count": len(samples),
        "latest_sample_status": samples[-1]["status"] if samples else None,
        "is_synthetic": patient["is_synthetic"],
    }


@app.get("/api/v1/mobile/notifications/unread-count")
async def unread_notification_count(authorization: str = Header(...)):
    headers = {"Authorization": authorization}
    async with httpx.AsyncClient(base_url=BACKEND_URL, timeout=10.0) as client:
        resp = await client.get("/api/v1/notifications", params={"unread_only": True}, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail="Could not load notifications")
    return {"unread_count": len(resp.json())}
