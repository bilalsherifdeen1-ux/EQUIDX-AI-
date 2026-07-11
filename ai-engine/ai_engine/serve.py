"""
EQUIDX AI — AI Engine microservice.

Exposes the modular diagnostic AI framework (preprocessing -> training ->
inference -> evaluation) over HTTP for the backend to call. This service is
intentionally separate from the core backend so model workloads can be
scaled, versioned, and (eventually) GPU-scheduled independently.

RESEARCH PROTOTYPE — every model here is a placeholder trained on synthetic
data. See ai_engine/datasets/synthetic_data_generator.py.
"""
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

from ai_engine.common.schemas import EvaluateResponse, InferenceRequest, InferenceResponse, TrainRequest
from ai_engine.datasets.synthetic_data_generator import GENERATORS
from ai_engine.pipeline import _TRAINERS, _model_cache, run_evaluation, run_inference

app = FastAPI(
    title="EQUIDX AI — AI Engine",
    description="Modular placeholder diagnostic AI framework. Research prototype only.",
    version="0.1.0",
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "equidx-ai-engine", "domains": list(GENERATORS)}


@app.get("/api/v1/domains")
async def list_domains():
    return {"domains": list(GENERATORS)}


@app.post("/api/v1/infer", response_model=InferenceResponse)
async def infer(payload: InferenceRequest):
    try:
        result = run_inference(payload.sample_type, payload.features)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return InferenceResponse(
        model_name=result.model_name, model_version=result.model_version,
        findings=result.findings, confidence_scores=result.confidence_scores,
        disclaimer=result.disclaimer,
    )


@app.post("/api/v1/train")
async def train(payload: TrainRequest):
    """Forces (re)training of a domain's model on freshly generated
    synthetic data, replacing the cached instance."""
    if payload.sample_type not in _TRAINERS:
        raise HTTPException(status_code=400, detail=f"Unknown sample_type '{payload.sample_type}'")
    _model_cache[payload.sample_type] = _TRAINERS[payload.sample_type]()
    return {"status": "trained", "sample_type": payload.sample_type}


@app.get("/api/v1/evaluate/{sample_type}", response_model=EvaluateResponse)
async def evaluate(sample_type: str, n_samples: int = 500):
    try:
        result = run_evaluation(sample_type, n_samples=n_samples)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Unknown sample_type '{sample_type}'")
    return EvaluateResponse(sample_type=sample_type, metrics=result["metrics"], n_samples=result["n_samples"])
