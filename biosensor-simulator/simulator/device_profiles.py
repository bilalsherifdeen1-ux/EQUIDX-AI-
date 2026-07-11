"""
Device signal profiles: parametrize what a "realistic" synthetic waveform
looks like per biosensor/assay type — baseline, noise amplitude, drift, and
sampling rate. These numbers are illustrative only, tuned to produce
visually plausible demo signals, not calibrated to any real device.
"""
from dataclasses import dataclass


@dataclass
class DeviceProfile:
    name: str
    sample_rate_hz: float
    baseline: float
    noise_std: float
    drift_per_sec: float


PROFILES: dict[str, DeviceProfile] = {
    "urinalysis": DeviceProfile("EQX-Uro1 optical strip reader", sample_rate_hz=10, baseline=0.5, noise_std=0.03, drift_per_sec=0.0005),
    "hba1c": DeviceProfile("EQX-Gly2 electrochemical sensor", sample_rate_hz=5, baseline=5.6, noise_std=0.08, drift_per_sec=0.001),
    "blood_chemistry": DeviceProfile("EQX-Chem3 ion-selective panel", sample_rate_hz=20, baseline=140.0, noise_std=0.6, drift_per_sec=0.002),
    "metabolic_panel": DeviceProfile("EQX-Met4 microfluidic panel", sample_rate_hz=15, baseline=95.0, noise_std=1.5, drift_per_sec=0.003),
    "hiv_screening": DeviceProfile("EQX-Immuno5 lateral-flow reader", sample_rate_hz=2, baseline=0.3, noise_std=0.05, drift_per_sec=0.0002),
}
