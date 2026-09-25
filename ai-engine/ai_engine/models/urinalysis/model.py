"""
Urinalysis placeholder model — random forest classifier over pH, specific
gravity, protein, glucose, leukocyte estimate, urine creatinine, and UPCR.

v0.3.0: fixed the same stateless-normalization bug as blood_chemistry —
scaler is now fit once on training data and reused at inference.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler, clip_outliers

FEATURE_NAMES = [
    "ph", "specific_gravity", "protein_mg_dl", "glucose_mg_dl",
    "leukocytes", "urine_creatinine_mg_dl", "upcr_mg_g",
]


class UrinalysisModel(BaseDiagnosticModel):
    name = "urinalysis-rf-placeholder"
    version = "0.3.0"

    def __init__(self):
        self.clf = RandomForestClassifier(n_estimators=150, max_depth=6, random_state=42)
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return self.scaler.transform(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        X_clipped = clip_outliers(X)
        Xp = self.scaler.fit_transform(X_clipped)
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

        protein, glucose, leukocytes, upcr = raw[2], raw[3], raw[4], raw[6]
        if pred == 1:
            if protein > 30 or glucose > 130 or leukocytes > 5:
                findings["flag"] = "abnormal_raw_value"
            elif upcr > 200:
                findings["flag"] = "proteinuria_upcr_only"
            else:
                findings["flag"] = "abnormal"
        else:
            findings["flag"] = "within_expected_range"

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
                "recall_sensitivity": round(float(recall_score(y, preds)), 4),
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
