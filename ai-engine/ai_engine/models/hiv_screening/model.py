"""
HIV screening placeholder model — a small PyTorch net over a synthetic
immunoassay optical-density (OD) ratio.

v0.3.0: fixed the same stateless-normalization bug. A positive flag is
always framed as "reactive — requires confirmatory testing," matching real
screening-test reporting conventions and the low-PPV-at-low-prevalence
reality documented in ai_engine/datasets/synthetic_data_generator.py.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, recall_score, roc_auc_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler


class _ODClassifierNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, 8), nn.ReLU(),
            nn.Linear(8, 8), nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x):
        return self.net(x)


class HIVScreeningModel(BaseDiagnosticModel):
    name = "hiv-screening-torch-placeholder"
    version = "0.3.0"

    def __init__(self):
        self.net = _ODClassifierNet()
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        X = raw_signal.reshape(-1, 1) if raw_signal.ndim == 1 else raw_signal
        return self.scaler.transform(X)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 60, lr: float = 0.01) -> None:
        X2 = X.reshape(-1, 1) if X.ndim == 1 else X
        Xp = torch.tensor(self.scaler.fit_transform(X2), dtype=torch.float32)
        yt = torch.tensor(y.reshape(-1, 1), dtype=torch.float32)
        optimizer = torch.optim.Adam(self.net.parameters(), lr=lr)
        loss_fn = nn.BCEWithLogitsLoss()

        self.net.train()
        for _ in range(epochs):
            optimizer.zero_grad()
            logits = self.net(Xp)
            loss = loss_fn(logits, yt)
            loss.backward()
            optimizer.step()
        self._fitted = True

    def predict(self, X: np.ndarray) -> InferenceResult:
        if not self._fitted:
            raise RuntimeError("Model has not been trained/loaded")
        self.net.eval()
        with torch.no_grad():
            Xp = torch.tensor(self.preprocess(X), dtype=torch.float32)
            prob_reactive = torch.sigmoid(self.net(Xp)).item()

        flag = "reactive_requires_confirmatory_testing" if prob_reactive >= 0.5 else "non_reactive"
        findings = {"od_ratio": round(float(X[0][0]), 3), "flag": flag}
        confidence = prob_reactive if flag.startswith("reactive") else 1 - prob_reactive
        return InferenceResult(
            findings=findings,
            confidence_scores={"flag": round(float(confidence), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        self.net.eval()
        with torch.no_grad():
            Xp = torch.tensor(self.preprocess(X), dtype=torch.float32)
            probs = torch.sigmoid(self.net(Xp)).numpy().flatten()
        preds = (probs >= 0.5).astype(int)
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(y, preds)), 4),
                "f1": round(float(f1_score(y, preds, zero_division=0)), 4),
                "recall_sensitivity": round(float(recall_score(y, preds, zero_division=0)), 4),
                "roc_auc": round(float(roc_auc_score(y, probs)), 4),
            },
            n_samples=len(y),
        )


def train_and_get_model() -> HIVScreeningModel:
    from ai_engine.datasets.synthetic_data_generator import generate_hiv_screening_data

    X, y = generate_hiv_screening_data(n=3000)
    model = HIVScreeningModel()
    model.train(X, y)
    return model
