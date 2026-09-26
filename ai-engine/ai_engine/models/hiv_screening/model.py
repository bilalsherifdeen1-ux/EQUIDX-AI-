"""
HIV screening placeholder model — 3-class PyTorch net mirroring the real
CDC 2014 two-stage HIV testing algorithm (screen + differentiation),
including the discordant "refer to NAT" category. See
ai_engine/datasets/synthetic_data_generator.py for full sourcing.

v0.4.0: rebuilt from single-assay binary to two-assay 3-class. Same
stateful-scaler fix as the other domains.
"""
from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, f1_score, recall_score

from ai_engine.common.base import BaseDiagnosticModel, EvaluationResult, InferenceResult
from ai_engine.preprocessing.signal_preprocessing import FittedScaler

LABELS = {
    0: "non_reactive",
    1: "reactive_concordant_recommend_clinical_confirmation",
    2: "reactive_discordant_recommend_NAT",
}


class _TwoAssayNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16), nn.ReLU(),
            nn.Linear(16, 16), nn.ReLU(),
            nn.Linear(16, 3),  # 3-class logits
        )

    def forward(self, x):
        return self.net(x)


class HIVScreeningModel(BaseDiagnosticModel):
    name = "hiv-screening-torch-placeholder"
    version = "0.4.0"

    def __init__(self):
        self.net = _TwoAssayNet()
        self.scaler = FittedScaler()
        self._fitted = False

    def preprocess(self, raw_signal: np.ndarray) -> np.ndarray:
        return self.scaler.transform(raw_signal)

    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 120, lr: float = 0.01) -> None:
        Xp = torch.tensor(self.scaler.fit_transform(X), dtype=torch.float32)
        yt = torch.tensor(y, dtype=torch.long)
        optimizer = torch.optim.Adam(self.net.parameters(), lr=lr)
        loss_fn = nn.CrossEntropyLoss()

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
            proba = torch.softmax(self.net(Xp), dim=1).numpy()[0]
        pred = int(np.argmax(proba))
        findings = {
            "ag_ab_screen_od_ratio": round(float(X[0][0]), 3),
            "differentiation_assay_signal": round(float(X[0][1]), 3),
            "flag": LABELS[pred],
        }
        return InferenceResult(
            findings=findings,
            confidence_scores={"flag": round(float(proba[pred]), 4)},
            model_name=self.name,
            model_version=self.version,
        )

    def evaluate(self, X: np.ndarray, y: np.ndarray) -> EvaluationResult:
        self.net.eval()
        with torch.no_grad():
            Xp = torch.tensor(self.preprocess(X), dtype=torch.float32)
            proba = torch.softmax(self.net(Xp), dim=1).numpy()
        preds = np.argmax(proba, axis=1)
        return EvaluationResult(
            metrics={
                "accuracy": round(float(accuracy_score(y, preds)), 4),
                "f1_macro": round(float(f1_score(y, preds, average="macro", zero_division=0)), 4),
                "recall_macro": round(float(recall_score(y, preds, average="macro", zero_division=0)), 4),
            },
            n_samples=len(y),
        )


def train_and_get_model() -> HIVScreeningModel:
    from ai_engine.datasets.synthetic_data_generator import generate_hiv_screening_data

    X, y = generate_hiv_screening_data(n=3000)
    model = HIVScreeningModel()
    model.train(X, y)
    return model
