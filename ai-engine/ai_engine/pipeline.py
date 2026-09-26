"""
InferencePipeline — dispatches a sample_type string to the correct
diagnostic domain model, lazily training (on synthetic data) and caching
an in-memory instance per domain.

REBUILT: `run_inference` now actually uses real signal data when it's
given `readings` (raw per-channel values from biosensor-simulator's
`generate_panel()["readings"]`) — routed through
`ai_engine.preprocessing.feature_extraction` so the same derived-feature
logic (BUN:creatinine ratio, UPCR, corrected calcium) is applied
identically to what training used. Previously this function ALWAYS
sampled a fresh synthetic row internally regardless of what was passed
in — the simulator and the AI engine were never actually connected end to
end. `readings=None` still falls back to that synthetic-sampling behavior
(useful for demos without a live device), but it is now the fallback, not
the only path.
"""
from __future__ import annotations

import numpy as np

from ai_engine.common.base import InferenceResult
from ai_engine.datasets.synthetic_data_generator import GENERATORS
from ai_engine.preprocessing.feature_extraction import extract_features
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


def run_inference(sample_type: str, readings: dict[str, float] | None = None) -> InferenceResult:
    """
    readings: raw per-channel values from a real (or simulated) biosensor
    reading, e.g. {"sodium_meq_l": 141.2, "potassium_meq_l": 4.1,
    "creatinine_mg_dl": 0.9, "bun_mg_dl": 13.5} for blood_chemistry. When
    provided, this is the actual signal the model scores. When omitted, a
    synthetic row is sampled instead (demo/fallback mode only — NOT
    connected to any real or simulated device reading).
    """
    model = _get_model(sample_type)
    if readings:
        X = extract_features(sample_type, readings)
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
