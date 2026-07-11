"""
Synthetic dataset generation for all five diagnostic domains.

Every dataset here is procedurally generated with NumPy and carries no
relationship to real patients or real assay data. Distributions are loosely
inspired by publicly known clinical reference ranges purely to make demo
outputs look plausible — they are NOT calibrated against real assay data
and must never be treated as such.
"""
from __future__ import annotations

import numpy as np


def generate_urinalysis_data(n: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    ph = rng.normal(6.0, 1.0, n)
    specific_gravity = rng.normal(1.02, 0.005, n)
    protein_mg_dl = rng.exponential(15, n)
    glucose_mg_dl = rng.exponential(10, n)
    leukocytes = rng.poisson(2, n)
    X = np.column_stack([ph, specific_gravity, protein_mg_dl, glucose_mg_dl, leukocytes])
    y = (protein_mg_dl > 30) | (glucose_mg_dl > 25) | (leukocytes > 5)
    return X, y.astype(int)


def generate_hba1c_data(n: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    hba1c_pct = rng.normal(5.6, 1.1, n).clip(3.5, 14.0)
    fasting_glucose = 28.7 * hba1c_pct - 46.7 + rng.normal(0, 10, n)
    X = np.column_stack([hba1c_pct, fasting_glucose])
    y = (hba1c_pct >= 6.5).astype(int)  # 0=normal/prediabetic band, 1=diabetic range (synthetic heuristic)
    return X, y


def generate_blood_chemistry_data(n: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    sodium = rng.normal(140, 3, n)
    potassium = rng.normal(4.2, 0.4, n)
    creatinine = rng.normal(0.9, 0.3, n).clip(0.3, 5.0)
    bun = rng.normal(14, 5, n).clip(2, 60)
    X = np.column_stack([sodium, potassium, creatinine, bun])
    y = ((creatinine > 1.3) | (bun > 25)).astype(int)
    return X, y


def generate_metabolic_panel_data(n: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    glucose = rng.normal(95, 20, n).clip(50, 400)
    calcium = rng.normal(9.5, 0.5, n)
    co2 = rng.normal(24, 3, n)
    albumin = rng.normal(4.2, 0.4, n)
    X = np.column_stack([glucose, calcium, co2, albumin])
    y = (glucose > 125).astype(int)
    return X, y


def generate_hiv_screening_data(n: int = 2000, seed: int = 42):
    """Synthetic immunoassay-style optical density (OD) ratios. Base rate is
    deliberately low to mimic a real screening population."""
    rng = np.random.default_rng(seed)
    is_positive = rng.random(n) < 0.03
    od_ratio = np.where(
        is_positive,
        rng.normal(3.5, 1.2, n).clip(1.1, 8.0),
        rng.normal(0.3, 0.2, n).clip(0.01, 1.0),
    )
    X = od_ratio.reshape(-1, 1)
    y = is_positive.astype(int)
    return X, y


GENERATORS = {
    "urinalysis": generate_urinalysis_data,
    "hba1c": generate_hba1c_data,
    "blood_chemistry": generate_blood_chemistry_data,
    "metabolic_panel": generate_metabolic_panel_data,
    "hiv_screening": generate_hiv_screening_data,
}
