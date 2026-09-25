"""
Blood chemistry placeholder model — gradient-boosted classifier flagging
electrolyte/renal-function abnormalities from synthetic sodium, potassium,
creatinine, BUN, and BUN:creatinine ratio values.

v0.3.0: fixes a critical preprocessing bug (see
ai_engine/preprocessing/signal_preprocessing.py) where single-row inference
was silently zeroed out. Scaling statistics are now fit once during
train() and reused via self.scaler at inference time.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler, clip_outliers

FEATURE_NAMES = ["sodium_meq_l", "potassium_meq_l", "creatinine_mg_dl", "bun_mg_dl", "bun_creatinine_ratio"]


class BloodChemistryModel(BaseDiagnosticModel):
    name = "blood-chemistry-gbc-placeholder"
    version = "0.3.0"

    def __init__(self):
        self.clf = GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=42)
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        # Uses the scaler's STORED training statistics — safe for both a
        # 3000-row training batch and a single inference row.
        return self.scaler.transform(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        X_clipped = clip_outliers(X)
        Xp = self.scaler.fit_transform(X_clipped)  # fit ONCE, here, on training data
        self.clf.fit(Xp, y)
        self._fitted = True

    def predict(self, X: np.ndarray) -> InferenceResult:
        if not self._fitted:
            raise RuntimeError("Model has not been trained/loaded")
        Xp = self.preprocess(X)  # transform only — reuses training-fit statistics
        proba = self.clf.predict_proba(Xp)[0]
        pred = int(np.argmax(proba))
        raw = X[0]
        findings = {name: round(float(val), 2) for name, val in zip(FEATURE_NAMES, raw)}

        creatinine, bun, ratio = raw[2], raw[3], raw[4]
        if pred == 1:
            if creatinine > 1.2 or bun > 20:
                findings["flag"] = "intrinsic_renal_pattern"
            elif ratio > 20:
                findings["flag"] = "prerenal_pattern_ratio_only"
            else:
                findings["flag"] = "renal_function_flag"
        else:
            findings["flag"] = "within_expected_range"

        return InferenceResult(
            findings=findings,
            confidence_scores={"flag": round(float(proba[pred]), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        Xp = self.preprocess(X)  # reuses training-fit statistics, not batch-relative
        preds = self.clf.predict(Xp)
        probs = self.clf.predict_proba(Xp)[:, 1]
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(y, preds)), 4),
                "f1": round(float(f1_score(y, preds)), 4),
                "recall_sensitivity": round(float(recall_score(y, preds)), 4),
                "roc_auc": round(float(roc_auc_score(y, probs)), 4),
            },
            n_samples=len(y),
        )


def train_and_get_model() -> BloodChemistryModel:
    from ai_engine.datasets.synthetic_data_generator import generate_blood_chemistry_data

    X, y = generate_blood_chemistry_data(n=3000)
    model = BloodChemistryModel()
    model.train(X, y)
    return model
