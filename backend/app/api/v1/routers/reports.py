"""Diagnostic report generation endpoints — triggers AI inference (via the
ai-engine service) and returns a report with confidence scores + disclaimer.
Clearly a "Research Prototype" surface; see disclaimer text in
app/domain/entities/report.py."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.dto.schemas import ReportOut
from app.application.services.audit_service import AuditService
from app.application.services.report_service import ReportService
from app.core.deps import (
    CurrentUser, get_audit_repository, get_current_user, get_report_repository, get_sample_repository, require_roles,
)
from app.core.exceptions import NotFoundError
from app.domain.entities.user import UserRole
from app.infrastructure.db.repositories.audit_repository import SqlAuditLogRepository
from app.infrastructure.db.repositories.report_repository import SqlReportRepository
from app.infrastructure.db.repositories.sample_repository import SqlSampleRepository

router = APIRouter(prefix="/reports", tags=["Diagnostic Reports (Research Prototype)"])


@router.post("/generate/{sample_id}", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
async def generate_report(
    sample_id: UUID,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN, UserRole.CLINICIAN, UserRole.RESEARCHER)),
    report_repo: SqlReportRepository = Depends(get_report_repository),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = ReportService(report_repo, sample_repo)
    try:
        report = await service.generate_report(sample_id, requested_by=UUID(current_user.id))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="report.generate", resource_type="report",
        resource_id=str(report.id), ip_address=request.client.host if request.client else None,
    )
    return report


@router.get("/{report_id}", response_model=ReportOut)
async def get_report(
    report_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    report_repo: SqlReportRepository = Depends(get_report_repository),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
):
    service = ReportService(report_repo, sample_repo)
    try:
        return await service.get_report(report_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/sample/{sample_id}", response_model=list[ReportOut])
async def list_reports_for_sample(
    sample_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    report_repo: SqlReportRepository = Depends(get_report_repository),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
):
    service = ReportService(report_repo, sample_repo)
    return await service.list_for_sample(sample_id)


@router.post("/{report_id}/review", response_model=ReportOut)
async def mark_report_reviewed(
    report_id: UUID,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN, UserRole.CLINICIAN)),
    report_repo: SqlReportRepository = Depends(get_report_repository),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = ReportService(report_repo, sample_repo)
    try:
        report = await service.mark_reviewed(report_id, reviewer_id=UUID(current_user.id))
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="report.review", resource_type="report",
        resource_id=str(report_id), ip_address=request.client.host if request.client else None,
    )
    return report
