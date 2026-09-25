"""
Metabolic panel placeholder model — XGBoost classifier over glucose,
calcium, CO2, albumin, and albumin-corrected calcium.

v0.3.0: same stateful-scaler fix as the other domains.
"""
from __future__ import annotations

import numpy as np
import xgboost as xgb
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler

FEATURE_NAMES = ["glucose_mg_dl", "calcium_mg_dl", "co2_meq_l", "albumin_g_dl", "corrected_calcium_mg_dl"]


class MetabolicPanelModel(BaseDiagnosticModel):
    name = "metabolic-panel-xgboost-placeholder"
    version = "0.3.0"

    def __init__(self):
        self.clf = xgb.XGBClassifier(n_estimators=180, max_depth=4, learning_rate=0.1, eval_metric="logloss")
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return self.scaler.transform(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        Xp = self.scaler.fit_transform(X)
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

        glucose, corrected_ca = raw[0], raw[4]
        if pred == 1:
            if glucose > 126:
                findings["flag"] = "elevated_glucose_flag"
            elif corrected_ca < 8.5 or corrected_ca > 10.5:
                findings["flag"] = "corrected_calcium_flag"
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


def train_and_get_model() -> MetabolicPanelModel:
    from ai_engine.datasets.synthetic_data_generator import generate_metabolic_panel_data

    X, y = generate_metabolic_panel_data(n=3000)
    model = MetabolicPanelModel()
    model.train(X, y)
    return model
