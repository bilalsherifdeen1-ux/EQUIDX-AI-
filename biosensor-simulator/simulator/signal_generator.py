"""
Generates a coherent multi-channel synthetic biosensor panel: one waveform
per raw biomarker channel for a domain, with population-level values drawn
so that correlated channels (BUN with creatinine, urine creatinine with
specific gravity, fasting glucose with HbA1c) move together for one
simulated "patient" per call — see device_profiles.py for why this
matters and the documented trade-off involved.

For HIV screening, which is bimodal rather than normally distributed
around one population mean, `_draw_hiv_targets()` handles the screen/
differentiation pairing directly (mirrors
ai_engine.datasets.synthetic_data_generator.generate_hiv_screening_data,
intentionally duplicated — see device_profiles.py docstring).
"""
from __future__ import annotations

import numpy as np

from simulator.device_profiles import DOMAIN_CHANNELS, CORRELATED_CHANNEL_GROUPS, ChannelSpec


def _draw_population_value(spec: ChannelSpec, rng: np.random.Generator) -> float:
    if spec.distribution == "exponential":
        val = rng.exponential(spec.population_mean)
    elif spec.distribution == "poisson":
        val = rng.poisson(spec.population_mean)
    else:
        val = rng.normal(spec.population_mean, spec.population_std)
    if spec.clip_min is not None or spec.clip_max is not None:
        lo = spec.clip_min if spec.clip_min is not None else -np.inf
        hi = spec.clip_max if spec.clip_max is not None else np.inf
        val = float(np.clip(val, lo, hi))
    return float(val)


def _draw_hiv_targets(rng: np.random.Generator, scenario: str | None) -> dict[str, float]:
    """scenario: None (random per NAIIS 2018 prevalence), 'non_reactive',
    'reactive_concordant', or 'reactive_discordant' — lets a demo request a
    specific case rather than waiting on a ~1.4% random draw."""
    if scenario is None:
        is_positive = rng.random() < 0.014
        is_acute = is_positive and (rng.random() < 0.12)
    else:
        is_positive = scenario in ("reactive_concordant", "reactive_discordant")
        is_acute = scenario == "reactive_discordant"

    screen = rng.normal(3.5, 1.2) if is_positive else rng.normal(0.3, 0.2)
    screen = float(np.clip(screen, 0.01, 8.0))

    if is_positive and not is_acute:
        differentiation = rng.normal(3.2, 1.0)
    else:
        differentiation = rng.normal(0.25, 0.18)
    differentiation = float(np.clip(differentiation, 0.01, 8.0))

    return {"ag_ab_screen_od_ratio": screen, "differentiation_assay_signal": differentiation}


def _draw_targets(sample_type: str, rng: np.random.Generator, scenario: str | None = None) -> dict[str, float]:
    if sample_type == "hiv_screening":
        return _draw_hiv_targets(rng, scenario)

    channels = DOMAIN_CHANNELS[sample_type]
    correlation = CORRELATED_CHANNEL_GROUPS.get(sample_type)
    dependent_name = correlation["dependent"] if correlation else None

    targets: dict[str, float] = {}
    for name, spec in channels.items():
        if name == dependent_name:
            continue  # computed after the driver, below
        targets[name] = _draw_population_value(spec, rng)

    if correlation:
        driver_val = targets[correlation["driver"]]
        central = correlation["relationship"](driver_val)
        noise_factor = rng.normal(1.0, correlation["dependent_noise_std"])
        dep_spec = channels[correlation["dependent"]]
        dep_val = central * noise_factor
        if dep_spec.clip_min is not None or dep_spec.clip_max is not None:
            lo = dep_spec.clip_min if dep_spec.clip_min is not None else -np.inf
            hi = dep_spec.clip_max if dep_spec.clip_max is not None else np.inf
            dep_val = float(np.clip(dep_val, lo, hi))
        targets[correlation["dependent"]] = float(dep_val)

    return targets


def generate_panel(
    sample_type: str, duration_sec: float = 6.0, seed: int | None = None, scenario: str | None = None,
) -> dict:
    """Returns {sample_type, channels: {name: {device, sample_rate_hz,
    timestamps, values}}, readings: {name: final_value}} — `readings` is
    the steady-state extracted value per channel (last point of each
    waveform, matching how a real strip reader reports one settled
    number), ready to hand to the AI engine's feature-extraction step.
    """
    if sample_type not in DOMAIN_CHANNELS:
        raise ValueError(f"Unknown sample_type '{sample_type}'. Valid: {list(DOMAIN_CHANNELS)}")

    rng = np.random.default_rng(seed)
    targets = _draw_targets(sample_type, rng, scenario)

    channels_out = {}
    readings = {}
    channel_specs = (
        {"ag_ab_screen_od_ratio": DOMAIN_CHANNELS["hiv_screening"]["ag_ab_screen_od_ratio"],
         "differentiation_assay_signal": DOMAIN_CHANNELS["hiv_screening"]["differentiation_assay_signal"]}
        if sample_type == "hiv_screening" else DOMAIN_CHANNELS[sample_type]
    )

    for name, spec in channel_specs.items():
        target = targets[name]
        n_points = max(2, int(duration_sec * spec.sample_rate_hz))
        t = np.linspace(0, duration_sec, n_points)
        # Waveform settles toward `target` (sensor stabilizing), with small
        # point-to-point jitter — NOT population variability, which was
        # already used to pick `target` itself.
        settle = 1.0 - np.exp(-t / max(duration_sec * 0.2, 0.3))
        jitter = rng.normal(0, spec.sensor_noise_std or target * 0.02, n_points)
        values = target * (0.85 + 0.15 * settle) + jitter

        channels_out[name] = {
            "device": spec.device_name,
            "sample_rate_hz": spec.sample_rate_hz,
            "timestamps": t.tolist(),
            "values": values.tolist(),
        }
        readings[name] = float(values[-1])  # last point = settled reading

    return {"sample_type": sample_type, "channels": channels_out, "readings": readings}
