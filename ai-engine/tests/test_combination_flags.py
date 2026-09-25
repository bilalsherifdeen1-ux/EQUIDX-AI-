"""
Regression tests for two things established during rebuild:

1. Each domain's label can be positive while every individual raw
   biomarker is within its own reference range (the "combination beats
   threshold" property blood_chemistry and urinalysis were rebuilt to
   have).
2. The single-row predict() path actually uses the real input — guards
   against the stateless-normalize() bug regressing.
"""
import numpy as np
import pytest

from ai_engine.datasets.synthetic_data_generator import (
    generate_blood_chemistry_data,
    generate_urinalysis_data,
)
from ai_engine.models.blood_chemistry.model import train_and_get_model as train_blood_chemistry
from ai_engine.models.urinalysis.model import train_and_get_model as train_urinalysis


def test_blood_chemistry_has_combination_only_positive_rows():
    X, y = generate_blood_chemistry_data(n=5000, seed=42)
    sodium, potassium, creatinine, bun = X[:, 0], X[:, 1], X[:, 2], X[:, 3]
    all_individually_normal = (
        (sodium >= 136) & (sodium <= 146)
        & (potassium >= 3.5) & (potassium <= 5.0)
        & (creatinine >= 0.6) & (creatinine <= 1.2)
        & (bun >= 7) & (bun <= 20)
    )
    combo_only = all_individually_normal & (y == 1)
    assert combo_only.sum() > 0, "expected some ratio-only positive rows"


def test_urinalysis_has_combination_only_positive_rows():
    X, y = generate_urinalysis_data(n=5000, seed=42)
    protein, glucose, leukocytes = X[:, 2], X[:, 3], X[:, 4]
    all_individually_normal = (protein <= 30) & (glucose <= 130) & (leukocytes <= 5)
    combo_only = all_individually_normal & (y == 1)
    assert combo_only.sum() > 0, "expected some UPCR-only positive rows"


def test_single_row_predict_is_not_zeroed():
    """Regression test for the stateless-normalize() bug: two very
    different single rows must not produce identical scaled features."""
    model = train_blood_chemistry()
    normal_row = np.array([[141.0, 4.2, 0.9, 14.0, 15.6]])
    abnormal_row = np.array([[110.0, 7.5, 3.8, 55.0, 14.5]])

    normal_scaled = model.preprocess(normal_row)
    abnormal_scaled = model.preprocess(abnormal_row)
    assert not np.allclose(normal_scaled, 0.0), "single-row scaling collapsed to zero"
    assert not np.allclose(normal_scaled, abnormal_scaled), "different inputs produced identical output"


def test_ratio_only_case_is_caught_by_real_predict_path():
    model = train_blood_chemistry()
    X, y = generate_blood_chemistry_data(n=5000, seed=42)
    sodium, potassium, creatinine, bun = X[:, 0], X[:, 1], X[:, 2], X[:, 3]
    all_individually_normal = (
        (sodium >= 136) & (sodium <= 146)
        & (potassium >= 3.5) & (potassium <= 5.0)
        & (creatinine >= 0.6) & (creatinine <= 1.2)
        & (bun >= 7) & (bun <= 20)
    )
    combo_idx = np.where(all_individually_normal & (y == 1))[0]
    assert len(combo_idx) > 0

    caught = sum(
        1 for i in combo_idx[:50]
        if model.predict(X[i:i+1]).findings["flag"] != "within_expected_range"
    )
    # Not claiming perfection — this is a placeholder model on synthetic
    # data — but it must catch the clear majority now that it can see the
    # real feature values.
    assert caught / 50 > 0.8
