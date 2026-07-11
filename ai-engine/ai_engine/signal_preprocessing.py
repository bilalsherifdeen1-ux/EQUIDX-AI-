"""
Shared signal-preprocessing utilities used across diagnostic domains before
features are handed to a model. Kept separate from any single model so
preprocessing logic (denoising, normalization, windowing) is reusable and
independently testable — mirrors a real biosensor pipeline's separation of
signal conditioning from classification/regression.
"""
from __future__ import annotations

import numpy as np


def normalize(signal: np.ndarray) -> np.ndarray:
    """Z-score normalize a 1D or 2D array of signal features."""
    mean = signal.mean(axis=0)
    std = signal.std(axis=0)
    std[std == 0] = 1.0
    return (signal - mean) / std


def moving_average_denoise(signal: np.ndarray, window: int = 5) -> np.ndarray:
    """Simple moving-average smoothing to reduce sensor noise."""
    if signal.ndim == 1:
        kernel = np.ones(window) / window
        return np.convolve(signal, kernel, mode="same")
    return np.apply_along_axis(lambda s: moving_average_denoise(s, window), axis=0, arr=signal)


def clip_outliers(signal: np.ndarray, n_std: float = 4.0) -> np.ndarray:
    """Clip values beyond n_std standard deviations to reduce the effect of
    sensor glitches/artifacts on downstream inference."""
    mean, std = signal.mean(axis=0), signal.std(axis=0)
    lower, upper = mean - n_std * std, mean + n_std * std
    return np.clip(signal, lower, upper)


def extract_summary_features(signal: np.ndarray) -> dict[str, float]:
    """Reduce a raw biosensor waveform to summary statistics — a stand-in
    for more sophisticated domain-specific feature extraction (e.g. peak
    detection, spectral features) in a production system."""
    return {
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
        "min": float(np.min(signal)),
        "max": float(np.max(signal)),
        "peak_to_peak": float(np.ptp(signal)),
    }
