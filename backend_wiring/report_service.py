"""
ReportService — generates a diagnostic report for a sample.

REBUILT: `generate_report()` now actually pulls a biosensor reading before
calling the AI engine, instead of calling /api/v1/infer with nothing and
silently getting back a prediction on an unrelated synthetic row. This
was the "simulator and ai-engine aren't wired together" gap identified
earlier in this project.

In this prototype, `get_simulated_panel()` calls biosensor-simulator's
synthetic panel generator rather than a physical device — there is no
physical device yet (see project stage: software prototype). When a real
biosensor cartridge exists, only `get_simulated_panel`'s call target
changes (real device driver instead of biosensor-simulator's REST
endpoint); everything downstream of `readings` is unchanged, since
ai-engine's /api/v1/infer already treats `readings` as "whatever the
sample's real channel values were," real or simulated.
"""
from __future__ import annotations

from app.domain.entities.report import DiagnosticReport
from app.domain.entities.sample import Sample
from app.infrastructure.clients.ai_engine_client import get_simulated_panel, run_inference


class ReportService:
    async def generate_report(self, sample: Sample) -> DiagnosticReport:
        panel = await get_simulated_panel(sample.sample_type)
        inference = await run_inference(
            sample_type=sample.sample_type,
            sample_id=str(sample.id),
            readings=panel["readings"],
        )

        return DiagnosticReport(
            sample_id=sample.id,
            model_name=inference["model_name"],
            model_version=inference["model_version"],
            findings=inference["findings"],
            confidence_scores=inference["confidence_scores"],
            disclaimer=inference["disclaimer"],
            used_real_readings=inference["used_real_readings"],
            raw_channel_readings=panel["readings"],  # audit trail: what the "device" actually reported
        )
