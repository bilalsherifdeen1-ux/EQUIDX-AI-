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
    name: str = "base"
    version: str = "0.1.0"

    @abstractmethod
    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray: ...

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray) -> None: ...

    @abstractmethod
    def predict(self, X: np.ndarray) -> InferenceResult: ...

    @abstractmethod
    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult: ...
