"""
Bridges biosensor-simulator's raw per-channel readings to the full feature
vector each domain model expects (raw channels + derived interaction
features, in the exact order each model's FEATURE_NAMES requires).

This is the piece that was missing before this rebuild: previously,
`/api/v1/infer` never received real signal data at all — it always
sampled a fresh synthetic row internally (see the "sample simulator and
ai-engine aren't wired together" gap flagged earlier in this project).
Now, when the caller supplies `readings` (raw channel values, as returned
by biosensor-simulator's `generate_panel()["readings"]`), this module
computes the same derived features
(ai_engine.datasets.synthetic_data_generator computes them at training
time) from those real readings, so training-time and inference-time
feature engineering stay identical — a common, easy-to-miss source of
train/serve skew.
"""
from __future__ import annotations

import numpy as np


def extract_blood_chemistry_features(readings: dict[str, float]) -> np.ndarray:
    sodium = readings["sodium_meq_l"]
    potassium = readings["potassium_meq_l"]
    creatinine = readings["creatinine_mg_dl"]
    bun = readings["bun_mg_dl"]
    ratio = bun / creatinine if creatinine else 0.0
    return np.array([[sodium, potassium, creatinine, bun, ratio]])


def extract_urinalysis_features(readings: dict[str, float]) -> np.ndarray:
    ph = readings["ph"]
    sg = readings["specific_gravity"]
    protein = readings["protein_mg_dl"]
    glucose = readings["glucose_mg_dl"]
    leukocytes = readings["leukocytes"]
    urine_creatinine = readings["urine_creatinine_mg_dl"]
    upcr = (protein / urine_creatinine) * 1000 if urine_creatinine else 0.0
    return np.array([[ph, sg, protein, glucose, leukocytes, urine_creatinine, upcr]])


def extract_hba1c_features(readings: dict[str, float]) -> np.ndarray:
    hba1c = readings["hba1c_percent"]
    glucose = readings["fasting_glucose_mg_dl"]
    return np.array([[hba1c, glucose]])


def extract_metabolic_panel_features(readings: dict[str, float]) -> np.ndarray:
    glucose = readings["glucose_mg_dl"]
    calcium = readings["calcium_mg_dl"]
    co2 = readings["co2_meq_l"]
    albumin = readings["albumin_g_dl"]
    corrected_calcium = calcium + 0.8 * (4.0 - albumin)  # Payne formula, BMJ 1973
    return np.array([[glucose, calcium, co2, albumin, corrected_calcium]])


def extract_hiv_screening_features(readings: dict[str, float]) -> np.ndarray:
    screen = readings["ag_ab_screen_od_ratio"]
    differentiation = readings["differentiation_assay_signal"]
    return np.array([[screen, differentiation]])


EXTRACTORS = {
    "blood_chemistry": extract_blood_chemistry_features,
    "urinalysis": extract_urinalysis_features,
    "hba1c": extract_hba1c_features,
    "metabolic_panel": extract_metabolic_panel_features,
    "hiv_screening": extract_hiv_screening_features,
}


def extract_features(sample_type: str, readings: dict[str, float]) -> np.ndarray:
    if sample_type not in EXTRACTORS:
        raise ValueError(f"Unknown sample_type '{sample_type}'. Valid: {list(EXTRACTORS)}")
    missing = set(_required_channels(sample_type)) - set(readings)
    if missing:
        raise ValueError(f"Missing required channel readings for '{sample_type}': {sorted(missing)}")
    return EXTRACTORS[sample_type](readings)


def _required_channels(sample_type: str) -> list[str]:
    return {
        "blood_chemistry": ["sodium_meq_l", "potassium_meq_l", "creatinine_mg_dl", "bun_mg_dl"],
        "urinalysis": ["ph", "specific_gravity", "protein_mg_dl", "glucose_mg_dl", "leukocytes", "urine_creatinine_mg_dl"],
        "hba1c": ["hba1c_percent", "fasting_glucose_mg_dl"],
        "metabolic_panel": ["glucose_mg_dl", "calcium_mg_dl", "co2_meq_l", "albumin_g_dl"],
        "hiv_screening": ["ag_ab_screen_od_ratio", "differentiation_assay_signal"],
    }[sample_type]
