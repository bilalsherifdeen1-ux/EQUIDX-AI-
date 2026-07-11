"""
HbA1c placeholder model — XGBoost classifier over synthetic HbA1c% and
estimated average glucose, predicting a research-only risk band.
"""
from __future__ import annotations

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import normalize

BANDS = {0: "normal", 1: "prediabetic_range", 2: "diabetic_range"}


def _band_from_hba1c(hba1c: np.ndarray) -> np.ndarray:
    return np.select([hba1c < 5.7, hba1c < 6.5], [0, 1], default=2)


class HbA1cModel(BaseDiagnosticModel):
    name = "hba1c-xgboost-placeholder"
    version = "0.1.0"

    def __init__(self):
        self.clf = xgb.XGBClassifier(
            n_estimators=200, max_depth=4, learning_rate=0.08,
            objective="multi:softprob", num_class=3, eval_metric="mlogloss",
        )
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return normalize(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        # y here is the binary diabetic-range flag from the generator; we
        # derive the 3-band label directly from HbA1c% for a richer output.
        hba1c_col = X[:, 0]
        bands = _band_from_hba1c(hba1c_col)
        Xp = self.preprocess(X)
        self.clf.fit(Xp, bands)
        self._fitted = True

    def predict(self, X: np.ndarray) -> InferenceResult:
        if not self._fitted:
            raise RuntimeError("Model has not been trained/loaded")
        Xp = self.preprocess(X)
        proba = self.clf.predict_proba(Xp)[0]
        band = int(np.argmax(proba))
        raw = X[0]
        findings = {
            "hba1c_percent": round(float(raw[0]), 2),
            "estimated_average_glucose_mg_dl": round(float(raw[1]), 1),
            "band": BANDS[band],
        }
        return InferenceResult(
            findings=findings,
            confidence_scores={"band": round(float(proba[band]), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        bands = _band_from_hba1c(X[:, 0])
        Xp = self.preprocess(X)
        preds = self.clf.predict(Xp)
        proba = self.clf.predict_proba(Xp)
        try:
            auc = roc_auc_score(bands, proba, multi_class="ovr")
        except ValueError:
            auc = float("nan")
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(bands, preds)), 4),
                "f1_macro": round(float(f1_score(bands, preds, average="macro")), 4),
                "roc_auc_ovr": round(float(auc), 4) if auc == auc else -1.0,
            },
            n_samples=len(bands),
        )


def train_and_get_model() -> HbA1cModel:
    from ai_engine.datasets.synthetic_data_generator import generate_hba1c_data

    X, y = generate_hba1c_data(n=3000)
    model = HbA1cModel()
    model.train(X, y)
    return model
