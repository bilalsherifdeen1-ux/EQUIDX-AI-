"""
EQUIDX AI — Analytics microservice.

Serves aggregate/rollup data for the research dashboard's analytics view
(patient/sample counts, sample status breakdown, per-domain distribution).
Deliberately read-only against the shared Postgres instance.
"""
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from analytics_service.aggregations import build_overview

app = FastAPI(
    title="EQUIDX AI — Analytics Service",
    description="Aggregation service powering the research analytics dashboard.",
    version="0.1.0",
)
Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "equidx-analytics"}


@app.get("/api/v1/analytics/overview")
async def overview():
    try:
        return await build_overview()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Analytics data unavailable: {e}")
