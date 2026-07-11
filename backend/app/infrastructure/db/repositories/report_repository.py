from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.report import DiagnosticReport
from app.infrastructure.db.models.orm_models import ReportModel


def _to_entity(m: ReportModel) -> DiagnosticReport:
    return DiagnosticReport(
        id=m.id, sample_id=m.sample_id, model_name=m.model_name, model_version=m.model_version,
        findings=m.findings, confidence_scores=m.confidence_scores, generated_by=m.generated_by,
        disclaimer=m.disclaimer, reviewed=m.reviewed, reviewed_by=m.reviewed_by, created_at=m.created_at,
    )


class SqlReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, report: DiagnosticReport) -> DiagnosticReport:
        m = ReportModel(
            id=report.id, sample_id=report.sample_id, model_name=report.model_name,
            model_version=report.model_version, findings=report.findings,
            confidence_scores=report.confidence_scores, generated_by=report.generated_by,
            disclaimer=report.disclaimer, reviewed=report.reviewed, reviewed_by=report.reviewed_by,
        )
        self.session.add(m)
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def get_by_id(self, report_id: UUID) -> DiagnosticReport | None:
        m = await self.session.get(ReportModel, report_id)
        return _to_entity(m) if m else None

    async def list_by_sample(self, sample_id: UUID) -> list[DiagnosticReport]:
        result = await self.session.execute(select(ReportModel).where(ReportModel.sample_id == sample_id))
        return [_to_entity(m) for m in result.scalars().all()]

    async def list(self, skip: int = 0, limit: int = 50) -> list[DiagnosticReport]:
        result = await self.session.execute(select(ReportModel).offset(skip).limit(limit))
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, report: DiagnosticReport) -> DiagnosticReport:
        m = await self.session.get(ReportModel, report.id)
        if m is None:
            raise ValueError("Report not found")
        m.reviewed = report.reviewed
        m.reviewed_by = report.reviewed_by
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)
