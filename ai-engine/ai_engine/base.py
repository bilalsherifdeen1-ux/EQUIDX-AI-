"""
Base abstractions for the modular AI framework.

Every diagnostic domain (urinalysis, HbA1c, blood chemistry, metabolic
panel, HIV screening) implements the same four-stage pipeline contract:

    preprocessing -> training -> inference -> evaluation

by subclassing `BaseDiagnosticModel`. This keeps every model interchangeable
behind a common interface (Strategy pattern), which is what lets
`ai_engine.pipeline.InferencePipeline` dispatch to the right model purely
from a `sample_type` string.

ALL MODELS ARE PLACEHOLDERS trained on synthetic data (see
ai_engine/datasets/synthetic_data_generator.py). They exist to demonstrate
the shape of a real diagnostic-AI pipeline, not to produce clinically valid
output.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class InferenceResult:
    findings: dict[str, Any]
    confidence_scores: dict[str, float]
    model_name: str
    model_version: str
    disclaimer: str = (
        "Placeholder research-prototype model output generated from synthetic "
        "data. Not a medical diagnosis. Not for clinical use."
    )


@dataclass
class EvaluationResult:
    metrics: dict[str, float] = field(default_factory=dict)
    n_samples: int = 0


class BaseDiagnosticModel(ABC):
    """Contract every diagnostic domain module must implement."""

    name: str = "base"
    version: str = "0.1.0"

    @abstractmethod
    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        """Clean / transform a raw biosensor signal into model-ready features."""

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Fit the model on synthetic training data."""

    @abstractmethod
    def predict(self, X: np.ndarray) -> InferenceResult:
        """Run inference and return findings with confidence scores."""

    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        """Compute evaluation metrics against a synthetic held-out set."""

    def save(self, path: str) -> None:
        import joblib
        joblib.dump(self, path)

    @staticmethod
    def load(path: str) -> "BaseDiagnosticModel":
        import joblib
        return joblib.load(path)
