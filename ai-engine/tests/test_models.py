"""Unit tests for each diagnostic domain model — verifies the
preprocess/train/predict/evaluate contract holds and outputs always include
confidence scores and the research disclaimer."""
import pytest

from ai_engine.models.blood_chemistry.model import train_and_get_model as train_blood_chemistry
from ai_engine.models.hba1c.model import train_and_get_model as train_hba1c
from ai_engine.models.hiv_screening.model import train_and_get_model as train_hiv_screening
from ai_engine.models.metabolic_panel.model import train_and_get_model as train_metabolic_panel
from ai_engine.models.urinalysis.model import train_and_get_model as train_urinalysis
from ai_engine.datasets.synthetic_data_generator import GENERATORS


@pytest.mark.parametrize(
    "trainer,domain",
    [
        (train_urinalysis, "urinalysis"),
        (train_hba1c, "hba1c"),
        (train_blood_chemistry, "blood_chemistry"),
        (train_metabolic_panel, "metabolic_panel"),
        (train_hiv_screening, "hiv_screening"),
    ],
)
def test_model_predicts_with_disclaimer_and_confidence(trainer, domain):
    model = trainer()
    X, _ = GENERATORS[domain](n=1, seed=7)
    result = model.predict(X)
    assert result.disclaimer  # never empty
    assert "not" in result.disclaimer.lower()
    assert len(result.confidence_scores) > 0
    for score in result.confidence_scores.values():
        assert 0.0 <= score <= 1.0


@pytest.mark.parametrize(
    "trainer,domain",
    [
        (train_urinalysis, "urinalysis"),
        (train_hba1c, "hba1c"),
        (train_blood_chemistry, "blood_chemistry"),
        (train_metabolic_panel, "metabolic_panel"),
        (train_hiv_screening, "hiv_screening"),
    ],
)
def test_model_evaluate_returns_metrics(trainer, domain):
    model = trainer()
    X, y = GENERATORS[domain](n=300, seed=99)
    result = model.evaluate(X, y)
    assert result.n_samples == 300
    assert "accuracy" in result.metrics
