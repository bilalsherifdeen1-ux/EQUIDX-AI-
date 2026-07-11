"""
InferencePipeline — dispatches a sample_type string to the correct
diagnostic domain model, lazily training (on synthetic data) and caching an
in-memory instance per domain. In a real deployment, `_get_model` would load
a persisted, versioned artifact (see BaseDiagnosticModel.save/load) from
object storage instead of training on the fly.
"""
from __future__ import annotations

import numpy as np

from ai_engine.common.base import InferenceResult
from ai_engine.datasets.synthetic_data_generator import GENERATORS
from ai_engine.models.blood_chemistry.model import train_and_get_model as train_blood_chemistry
from ai_engine.models.hba1c.model import train_and_get_model as train_hba1c
from ai_engine.models.hiv_screening.model import train_and_get_model as train_hiv_screening
from ai_engine.models.metabolic_panel.model import train_and_get_model as train_metabolic_panel
from ai_engine.models.urinalysis.model import train_and_get_model as train_urinalysis

_TRAINERS = {
    "urinalysis": train_urinalysis,
    "hba1c": train_hba1c,
    "blood_chemistry": train_blood_chemistry,
    "metabolic_panel": train_metabolic_panel,
    "hiv_screening": train_hiv_screening,
}

_model_cache: dict[str, object] = {}


def _get_model(sample_type: str):
    if sample_type not in _TRAINERS:
        raise ValueError(f"Unknown sample_type '{sample_type}'. Valid: {list(_TRAINERS)}")
    if sample_type not in _model_cache:
        _model_cache[sample_type] = _TRAINERS[sample_type]()
    return _model_cache[sample_type]


def run_inference(sample_type: str, features: dict[str, float] | None = None) -> InferenceResult:
    """Runs inference for a given domain. If explicit `features` aren't
    supplied (typical for this demo, since we don't have a real device
    feeding real values), a single synthetic feature row is sampled to
    stand in for a live biosensor reading."""
    model = _get_model(sample_type)
    if features:
        X = np.array([list(features.values())], dtype=float)
    else:
        generator = GENERATORS[sample_type]
        X, _ = generator(n=1)
    return model.predict(X)


def run_evaluation(sample_type: str, n_samples: int = 500) -> dict:
    model = _get_model(sample_type)
    generator = GENERATORS[sample_type]
    X, y = generator(n=n_samples, seed=123)
    result = model.evaluate(X, y)
    return {"metrics": result.metrics, "n_samples": result.n_samples}
