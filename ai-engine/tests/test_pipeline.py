"""Integration-style tests for the InferencePipeline dispatch layer."""
import pytest

from ai_engine.pipeline import run_evaluation, run_inference


def test_run_inference_unknown_domain_raises():
    with pytest.raises(ValueError):
        run_inference("not_a_real_domain")


@pytest.mark.parametrize(
    "domain", ["urinalysis", "hba1c", "blood_chemistry", "metabolic_panel", "hiv_screening"]
)
def test_run_inference_all_domains(domain):
    result = run_inference(domain)
    assert result.model_name
    assert result.findings


def test_run_evaluation_urinalysis():
    result = run_evaluation("urinalysis", n_samples=200)
    assert result["n_samples"] == 200
    assert "accuracy" in result["metrics"]
