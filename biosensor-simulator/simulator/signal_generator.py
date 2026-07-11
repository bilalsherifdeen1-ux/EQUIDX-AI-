"""
Generates realistic-looking synthetic biosensor signal waveforms: baseline +
low-frequency drift + Gaussian noise + occasional artifact spikes, matching
the shape (not the clinical validity) of a real analog sensor readout.
"""
from __future__ import annotations

import numpy as np

from simulator.device_profiles import PROFILES, DeviceProfile


def generate_waveform(
    sample_type: str, duration_sec: float = 10.0, seed: int | None = None, spike_probability: float = 0.02,
) -> dict:
    if sample_type not in PROFILES:
        raise ValueError(f"Unknown sample_type '{sample_type}'. Valid: {list(PROFILES)}")
    profile: DeviceProfile = PROFILES[sample_type]
    rng = np.random.default_rng(seed)

    n_points = max(2, int(duration_sec * profile.sample_rate_hz))
    t = np.linspace(0, duration_sec, n_points)

    drift = profile.drift_per_sec * t
    noise = rng.normal(0, profile.noise_std, n_points)
    signal = profile.baseline + drift + noise

    spikes = rng.random(n_points) < spike_probability
    signal[spikes] += rng.normal(0, profile.noise_std * 6, spikes.sum())

    return {
        "device": profile.name,
        "sample_type": sample_type,
        "sample_rate_hz": profile.sample_rate_hz,
        "duration_sec": duration_sec,
        "timestamps": t.tolist(),
        "values": signal.tolist(),
    }
