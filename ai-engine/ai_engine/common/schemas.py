"""Pydantic schemas for the ai-engine's own inference HTTP API."""
from typing import Any

from pydantic import BaseModel


class InferenceRequest(BaseModel):
    sample_type: str
    sample_id: str
    readings: dict[str, float] | None = None  # raw channel values from biosensor-simulator; omit for synthetic fallback


class InferenceResponse(BaseModel):
    model_name: str
    model_version: str
    findings: dict[str, Any]
    confidence_scores: dict[str, float]
    disclaimer: str
    used_real_readings: bool  # False means the synthetic-fallback path was used, not a real/simulated signal


class TrainRequest(BaseModel):
    sample_type: str
    n_synthetic_samples: int = 2000


class EvaluateResponse(BaseModel):
    sample_type: str
    metrics: dict[str, float]
    n_samples: int
