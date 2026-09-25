"""
Shared signal-preprocessing utilities.

CRITICAL FIX (see project discussion): the original `normalize()` here
z-scored whatever batch was passed to it against *that batch's own* mean
and standard deviation. That is correct when scoring a large batch (e.g.
`evaluate()`), but every real inference call passes exactly one row — and
for a single row, mean == that row's own values, so every feature
collapses to (x - x) / 1 = 0, identically, no matter what the actual
reading was. In effect, every prediction ignored the input entirely.

The fix: preprocessing must be **stateful**. Fit the scaling statistics
once on the training set (`FittedScaler.fit`), store them on the model
instance, and reuse those *same* stored statistics both for training and
for every future inference call (`FittedScaler.transform`) — this is the
standard pattern behind `sklearn.preprocessing.StandardScaler`, and it's
what every domain model below now uses instead of the old stateless
`normalize()` function.
"""
from __future__ import annotations

import numpy as np


class FittedScaler:
    """Z-score scaler that remembers the mean/std it was fit with, so a
    single later row is scaled against the *training* distribution, not
    against itself."""

    def __init__(self):
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None

    def fit(self, X: np.ndarray) -> "FittedScaler":
        self.mean_ = X.mean(axis=0)
        std = X.std(axis=0)
        self.std_ = np.where(std == 0, 1.0, std)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.std_ is None:
            raise RuntimeError("FittedScaler.transform called before fit()")
        return (X - self.mean_) / self.std_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


def clip_outliers(signal: np.ndarray, n_std: float = 4.0) -> np.ndarray:
    """Clip values beyond n_std standard deviations. Safe to compute
    per-batch for training but must NOT be applied per-single-row at
    inference time. Models below only call this during `train()`, never
    inside the code path `predict()` uses.
    """
    mean, std = signal.mean(axis=0), signal.std(axis=0)
    lower, upper = mean - n_std * std, mean + n_std * std
    return np.clip(signal, lower, upper)


def extract_summary_features(signal: np.ndarray) -> dict[str, float]:
    return {
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
        "min": float(np.min(signal)),
        "max": float(np.max(signal)),
        "peak_to_peak": float(np.ptp(signal)),
    }
