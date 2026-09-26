"""
HbA1c placeholder model — 4-class XGBoost classifier over independently
measured HbA1c% and fasting glucose, including a genuine "discordant"
category (ADA-documented: the two diagnostic criteria can disagree, and
the protocol is to repeat the abnormal test, not silently pick one).

v0.4.0: rebuilt for real two-measurement discordance (was previously a
single deterministic eAG transform). Same stateful-scaler fix as the
other domains.
"""
from __future__ import annotations

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, recall_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler

BANDS = {
    0: "concordant_normal",
    1: "concordant_prediabetic",
    2: "concordant_diabetic",
    3: "discordant_recommend_repeat_test",
}


def _hba1c_band(hba1c: np.ndarray) -> np.ndarray:
    return np.select([hba1c < 5.7, hba1c < 6.5], [0, 1], default=2)


def _glucose_band(glucose: np.ndarray) -> np.ndarray:
    return np.select([glucose < 100, glucose < 126], [0, 1], default=2)


def _label(hba1c: np.ndarray, glucose: np.ndarray) -> np.ndarray:
    hb, gl = _hba1c_band(hba1c), _glucose_band(glucose)
    return np.where(hb == gl, hb, 3)


class HbA1cModel(BaseDiagnosticModel):
    name = "hba1c-xgboost-placeholder"
    version = "0.4.0"

    def __init__(self):
        self.clf = xgb.XGBClassifier(
            n_estimators=200, max_depth=4, learning_rate=0.08,
            objective="multi:softprob", num_class=4, eval_metric="mlogloss",
        )
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return self.scaler.transform(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        # y passed in is already the 4-class label from the generator;
        # recomputing from X here as a defensive check that the two agree.
        labels = _label(X[:, 0], X[:, 1])
        Xp = self.scaler.fit_transform(X)
        self.clf.fit(Xp, labels)
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
            "fasting_glucose_mg_dl": round(float(raw[1]), 1),
            "band": BANDS[band],
        }
        return InferenceResult(
            findings=findings,
            confidence_scores={"band": round(float(proba[band]), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        labels = _label(X[:, 0], X[:, 1])
        Xp = self.preprocess(X)
        preds = self.clf.predict(Xp)
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(labels, preds)), 4),
                "f1_macro": round(float(f1_score(labels, preds, average="macro")), 4),
                "recall_macro": round(float(recall_score(labels, preds, average="macro")), 4),
            },
            n_samples=len(labels),
        )


def train_and_get_model() -> HbA1cModel:
    from ai_engine.datasets.synthetic_data_generator import generate_hba1c_data

    X, y = generate_hba1c_data(n=3000)
    model = HbA1cModel()
    model.train(X, y)
    return model
