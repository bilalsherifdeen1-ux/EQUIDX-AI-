"""
Per-domain biosensor channel definitions.

REBUILT: the original version had one generic waveform profile per
sample_type. This version defines one channel per RAW biomarker each
ai-engine domain model actually consumes (see
ai-engine/ai_engine/models/*/model.py FEATURE_NAMES) — derived features
(BUN:creatinine ratio, UPCR, corrected calcium) are computed downstream in
the AI engine, not simulated as their own channel.

Two distinct kinds of variability are modeled, and conflating them was a
mistake in an earlier draft of this file:
  - POPULATION variability (patient-to-patient): how much a given
    biomarker's true value varies across different people. This must
    match ai_engine's synthetic_data_generator.py population parameters,
    or the simulator would hand the AI models data outside the
    distribution they were trained on.
  - SENSOR jitter (point-to-point): the small noise a real biosensor
    reading wobbles by around a person's one true value while the strip
    stabilizes. This is a much smaller, separate number, used only for
    generating a visually realistic waveform.

DOCUMENTED ARCHITECTURAL TRADE-OFF: biosensor-simulator and ai-engine are
separate containers with no shared code (that's the point of the
microservice split). But the interaction terms blood_chemistry and
urinalysis's classification rely on (BUN tracking creatinine, urine
creatinine tracking specific gravity) reflect one patient's physiology, so
this file intentionally duplicates the correlation logic from
ai_engine/datasets/synthetic_data_generator.py in
`CORRELATED_CHANNEL_GROUPS` below. If that generator's correlation
formulas change, this file needs a matching update — flagged in both
files' docstrings.
"""
from dataclasses import dataclass
from typing import Callable, Literal


@dataclass
class ChannelSpec:
    device_name: str
    sample_rate_hz: float
    population_mean: float
    population_std: float
    distribution: Literal["normal", "exponential", "poisson"] = "normal"
    clip_min: float | None = None
    clip_max: float | None = None
    sensor_noise_std: float = 0.0  # point-to-point waveform jitter; set per-channel below


def _with_sensor_noise(spec: ChannelSpec, fraction: float = 0.06) -> ChannelSpec:
    spec.sensor_noise_std = spec.population_std * fraction
    return spec


DOMAIN_CHANNELS: dict[str, dict[str, ChannelSpec]] = {
    "blood_chemistry": {
        "sodium_meq_l": _with_sensor_noise(ChannelSpec("EQX-Chem3 Na ISE", 10, 141.0, 3.0, clip_min=120, clip_max=160)),
        "potassium_meq_l": _with_sensor_noise(ChannelSpec("EQX-Chem3 K ISE", 10, 4.2, 0.4, clip_min=2.5, clip_max=7.0)),
        "creatinine_mg_dl": _with_sensor_noise(ChannelSpec("EQX-Chem3 creatinine enzymatic", 5, 0.9, 0.25, clip_min=0.3, clip_max=5.0)),
        "bun_mg_dl": ChannelSpec("EQX-Chem3 urease/GLDH", 5, 13.0, 1.0, sensor_noise_std=0.6),  # dependent — see CORRELATED_CHANNEL_GROUPS
    },
    "urinalysis": {
        "ph": _with_sensor_noise(ChannelSpec("EQX-Uro1 pH strip", 5, 6.0, 1.0, clip_min=4.5, clip_max=9.0)),
        "specific_gravity": _with_sensor_noise(ChannelSpec("EQX-Uro1 refractometer", 5, 1.016, 0.007, clip_min=1.001, clip_max=1.035)),
        "protein_mg_dl": _with_sensor_noise(ChannelSpec("EQX-Uro1 protein error-of-indicators", 5, 9.0, 9.0, distribution="exponential", clip_min=0, clip_max=300)),
        "glucose_mg_dl": _with_sensor_noise(ChannelSpec("EQX-Uro1 glucose oxidase", 5, 8.0, 8.0, distribution="exponential", clip_min=0, clip_max=400)),
        "leukocytes": ChannelSpec("EQX-Uro1 esterase strip", 5, 1.5, 1.5, distribution="poisson", sensor_noise_std=0.1),
        "urine_creatinine_mg_dl": ChannelSpec("EQX-Uro1 creatinine strip", 5, 100.0, 40.0, clip_min=5, clip_max=400, sensor_noise_std=5.0),  # dependent
    },
    "hba1c": {
        "hba1c_percent": _with_sensor_noise(ChannelSpec("EQX-Gly2 boronate affinity", 2, 5.6, 1.1, clip_min=3.5, clip_max=14.0)),
        "fasting_glucose_mg_dl": ChannelSpec("EQX-Gly2 glucose oxidase", 5, 92.0, 30.0, clip_min=50, clip_max=400, sensor_noise_std=3.0),  # dependent
    },
    "metabolic_panel": {
        "glucose_mg_dl": _with_sensor_noise(ChannelSpec("EQX-Met4 glucose oxidase", 5, 92.0, 18.0, clip_min=50, clip_max=400)),
        "calcium_mg_dl": _with_sensor_noise(ChannelSpec("EQX-Met4 arsenazo III", 5, 9.4, 0.6, clip_min=5.0, clip_max=14.0)),
        "co2_meq_l": _with_sensor_noise(ChannelSpec("EQX-Met4 CO2 electrode", 5, 26.0, 2.5, clip_min=10, clip_max=40)),
        "albumin_g_dl": _with_sensor_noise(ChannelSpec("EQX-Met4 BCG dye-binding", 5, 4.2, 0.5, clip_min=1.0, clip_max=6.0)),
    },
    "hiv_screening": {
        # Bimodal (reactive vs non-reactive) — handled specially in
        # signal_generator.py rather than as a single normal distribution.
        "ag_ab_screen_od_ratio": ChannelSpec("EQX-Immuno5 4th-gen Ag/Ab", 2, 0.3, 0.2, clip_min=0.01, clip_max=8.0, sensor_noise_std=0.03),
        "differentiation_assay_signal": ChannelSpec("EQX-Immuno5 differentiation reflex", 2, 0.25, 0.18, clip_min=0.01, clip_max=8.0, sensor_noise_std=0.03),
    },
}

# driver -> dependent correlation, mirroring ai_engine's generator exactly
# (see module docstring: intentionally duplicated, kept in sync manually).
CORRELATED_CHANNEL_GROUPS: dict[str, dict] = {
    "blood_chemistry": {
        "driver": "creatinine_mg_dl",
        "dependent": "bun_mg_dl",
        "relationship": lambda creatinine: 13.0 * (creatinine / 0.9),
        "dependent_noise_std": 0.28,
    },
    "urinalysis": {
        "driver": "specific_gravity",
        "dependent": "urine_creatinine_mg_dl",
        "relationship": lambda sg: (sg - 1.000) * 9000,
        "dependent_noise_std": 0.3,
    },
    "hba1c": {
        "driver": "hba1c_percent",
        "dependent": "fasting_glucose_mg_dl",
        "relationship": lambda hba1c: 28.7 * hba1c - 46.7,
        "dependent_noise_std": 0.08,
    },
}
