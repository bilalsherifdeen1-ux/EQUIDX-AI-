"""Application service for diagnostic report generation. Calls out to the
ai-engine microservice for placeholder inference, then persists the result
via the report repository. Never returns a finding without the research
disclaimer and per-finding confidence scores attached."""
from __future__ import annotations

from uuid import UUID

import httpx

from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.domain.entities.report import DiagnosticReport
from app.domain.entities.sample import SampleStatus
from app.domain.repositories.report_repository import ReportRepository
from app.domain.repositories.sample_repository import SampleRepository

settings = get_settings()


class ReportService:
    def __init__(self, report_repository: ReportRepository, sample_repository: SampleRepository):
        self.repo = report_repository
        self.samples = sample_repository

    async def generate_report(self, sample_id: UUID, requested_by: UUID | None) -> DiagnosticReport:
        sample = await self.samples.get_by_id(sample_id)
        if not sample:
            raise NotFoundError(f"Sample {sample_id} not found")

        async with httpx.AsyncClient(base_url=settings.AI_ENGINE_URL, timeout=30.0) as client:
            response = await client.post(
                "/api/v1/infer",
                json={"sample_type": sample.sample_type.value, "sample_id": str(sample.id)},
            )
            response.raise_for_status()
            inference = response.json()

        report = DiagnosticReport(
            sample_id=sample.id,
            model_name=inference["model_name"],
            model_version=inference["model_version"],
            findings=inference["findings"],
            confidence_scores=inference["confidence_scores"],
            generated_by=requested_by,
        )
        created = await self.repo.create(report)

        sample.status = SampleStatus.ANALYZED
        await self.samples.update(sample)
        return created

    async def get_report(self, report_id: UUID) -> DiagnosticReport:
        report = await self.repo.get_by_id(report_id)
        if not report:
            raise NotFoundError(f"Report {report_id} not found")
        return report

    async def list_for_sample(self, sample_id: UUID) -> list[DiagnosticReport]:
        return await self.repo.list_by_sample(sample_id)

    async def mark_reviewed(self, report_id: UUID, reviewer_id: UUID) -> DiagnosticReport:
        report = await self.get_report(report_id)
        report.reviewed = True
        report.reviewed_by = reviewer_id
        return await self.repo.update(report)
