"""
Urinalysis placeholder model — random forest classifier predicting an
abnormal-flag from synthetic urinalysis features (pH, specific gravity,
protein, glucose, leukocyte estimate).

Pipeline stages are explicit methods per the BaseDiagnosticModel contract:
`preprocess` -> `train` -> `predict` -> `evaluate`.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import clip_outliers, normalize

FEATURE_NAMES = ["ph", "specific_gravity", "protein_mg_dl", "glucose_mg_dl", "leukocytes"]


class UrinalysisModel(BaseDiagnosticModel):
    name = "urinalysis-rf-placeholder"
    version = "0.1.0"

    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42)
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
        findings = {
            "ph": round(float(raw[0]), 2),
            "specific_gravity": round(float(raw[1]), 4),
            "protein_mg_dl": round(float(raw[2]), 1),
            "glucose_mg_dl": round(float(raw[3]), 1),
            "leukocytes_per_hpf": round(float(raw[4]), 1),
            "flag": "abnormal" if pred == 1 else "within_expected_range",
        }
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


def train_and_get_model() -> UrinalysisModel:
    from ai_engine.datasets.synthetic_data_generator import generate_urinalysis_data

    X, y = generate_urinalysis_data(n=3000)
    model = UrinalysisModel()
    model.train(X, y)
    return model
