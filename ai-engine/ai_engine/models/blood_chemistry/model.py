"""
Blood chemistry placeholder model — gradient-boosted classifier flagging
electrolyte/renal-function abnormalities from synthetic sodium, potassium,
creatinine, and BUN values.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import clip_outliers, normalize

FEATURE_NAMES = ["sodium_meq_l", "potassium_meq_l", "creatinine_mg_dl", "bun_mg_dl"]


class BloodChemistryModel(BaseDiagnosticModel):
    name = "blood-chemistry-gbc-placeholder"
    version = "0.1.0"

    def __init__(self):
        self.clf = GradientBoostingClassifier(n_estimators=150, max_depth=3, random_state=42)
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return normalize(clip_outliers(raw_signal))

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        Xp = self.preprocess(X)
        self.clf.fit(Xp, y)
        self._fitted = True

    def predict(self, X: np.ndarray) -> InferenceResult:
        if not self._fitted:
            raise RuntimeError("Model has not been trained/loaded")
        Xp = self.preprocess(X)
        proba = self.clf.predict_proba(Xp)[0]
        pred = int(np.argmax(proba))
        raw = X[0]
        findings = {name: round(float(val), 2) for name, val in zip(FEATURE_NAMES, raw)}
        findings["flag"] = "renal_function_flag" if pred == 1 else "within_expected_range"
        return InferenceResult(
            findings=findings,
            confidence_scores={"flag": round(float(proba[pred]), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        Xp = self.preprocess(X)
        preds = self.clf.predict(Xp)
        probs = self.clf.predict_proba(Xp)[:, 1]
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(y, preds)), 4),
                "f1": round(float(f1_score(y, preds)), 4),
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
