"""Sample registration and tracking endpoints."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.application.dto.schemas import SampleCreate, SampleOut, SampleStatusUpdate
from app.application.services.audit_service import AuditService
from app.application.services.sample_service import SampleService, generate_barcode
from app.core.deps import (
    CurrentUser, get_audit_repository, get_current_user, get_sample_repository, require_roles,
)
from app.core.exceptions import NotFoundError
from app.domain.entities.sample import Sample
from app.domain.entities.user import UserRole
from app.infrastructure.db.repositories.audit_repository import SqlAuditLogRepository
from app.infrastructure.db.repositories.sample_repository import SqlSampleRepository

router = APIRouter(prefix="/samples", tags=["Samples"])


@router.post("", response_model=SampleOut, status_code=status.HTTP_201_CREATED)
async def register_sample(
    payload: SampleCreate,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN, UserRole.CLINICIAN, UserRole.LAB_TECH)),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = SampleService(sample_repo)
    sample = Sample(
        patient_id=payload.patient_id, sample_type=payload.sample_type,
        barcode=generate_barcode(payload.sample_type.value), device_id=payload.device_id,
        collected_by=UUID(current_user.id),
    )
    created = await service.register_sample(sample)
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="sample.create", resource_type="sample",
        resource_id=str(created.id), ip_address=request.client.host if request.client else None,
    )
    return created


@router.get("", response_model=list[SampleOut])
async def list_samples(
    skip: int = 0, limit: int = 50,
    current_user: CurrentUser = Depends(get_current_user),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
):
    return await SampleService(sample_repo).list_samples(skip=skip, limit=limit)


@router.get("/{sample_id}", response_model=SampleOut)
async def get_sample(
    sample_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
):
    try:
        return await SampleService(sample_repo).get_sample(sample_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{sample_id}/status", response_model=SampleOut)
async def update_sample_status(
    sample_id: UUID,
    payload: SampleStatusUpdate,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN, UserRole.CLINICIAN, UserRole.LAB_TECH)),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = SampleService(sample_repo)
    try:
        updated = await service.update_status(sample_id, payload.status)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="sample.status_update", resource_type="sample",
        resource_id=str(sample_id), metadata={"new_status": payload.status.value},
        ip_address=request.client.host if request.client else None,
    )
    return updated


@router.get("/patient/{patient_id}", response_model=list[SampleOut])
async def list_samples_for_patient(
    patient_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    sample_repo: SqlSampleRepository = Depends(get_sample_repository),
):
    return await SampleService(sample_repo).list_for_patient(patient_id)
