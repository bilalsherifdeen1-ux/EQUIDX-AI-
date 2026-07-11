import pytest

from simulator.signal_generator import generate_waveform


def test_generate_waveform_shape():
    result = generate_waveform("urinalysis", duration_sec=2.0, seed=1)
    assert len(result["timestamps"]) == len(result["values"])
    assert result["sample_type"] == "urinalysis"


def test_generate_waveform_unknown_type_raises():
    with pytest.raises(ValueError):
        generate_waveform("not_real")


@pytest.mark.parametrize("sample_type", ["urinalysis", "hba1c", "blood_chemistry", "metabolic_panel", "hiv_screening"])
def test_generate_waveform_all_types(sample_type):
    result = generate_waveform(sample_type, duration_sec=1.0, seed=42)
    assert len(result["values"]) > 0
