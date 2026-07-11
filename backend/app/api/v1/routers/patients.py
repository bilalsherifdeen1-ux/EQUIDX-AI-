"""Patient record management endpoints. All data is synthetic/demo — see
app/domain/entities/patient.py."""
import secrets
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.application.dto.schemas import PatientCreate, PatientOut
from app.application.services.audit_service import AuditService
from app.application.services.patient_service import PatientService
from app.core.deps import CurrentUser, get_audit_repository, get_current_user, get_patient_repository, require_roles
from app.core.exceptions import NotFoundError
from app.domain.entities.patient import Patient
from app.domain.entities.user import UserRole
from app.infrastructure.db.repositories.audit_repository import SqlAuditLogRepository
from app.infrastructure.db.repositories.patient_repository import SqlPatientRepository

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(
    payload: PatientCreate,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN, UserRole.CLINICIAN, UserRole.RESEARCHER, UserRole.LAB_TECH)),
    patient_repo: SqlPatientRepository = Depends(get_patient_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = PatientService(patient_repo)
    patient = Patient(
        mrn=f"SYN-{secrets.token_hex(4).upper()}",
        first_name=payload.first_name, last_name=payload.last_name,
        date_of_birth=payload.date_of_birth, sex=payload.sex,
        contact_email=payload.contact_email, notes=payload.notes,
        created_by=UUID(current_user.id),
    )
    created = await service.register_patient(patient)
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="patient.create", resource_type="patient",
        resource_id=str(created.id), ip_address=request.client.host if request.client else None,
    )
    return created


@router.get("", response_model=list[PatientOut])
async def list_patients(
    skip: int = 0, limit: int = Query(50, le=200), search: str | None = None,
    current_user: CurrentUser = Depends(get_current_user),
    patient_repo: SqlPatientRepository = Depends(get_patient_repository),
):
    service = PatientService(patient_repo)
    return await service.list_patients(skip=skip, limit=limit, search=search)


@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(
    patient_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    patient_repo: SqlPatientRepository = Depends(get_patient_repository),
):
    service = PatientService(patient_repo)
    try:
        return await service.get_patient(patient_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: UUID,
    request: Request,
    current_user: CurrentUser = Depends(require_roles(UserRole.ADMIN)),
    patient_repo: SqlPatientRepository = Depends(get_patient_repository),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    service = PatientService(patient_repo)
    await service.delete_patient(patient_id)
    await AuditService(audit_repo).record(
        actor_id=UUID(current_user.id), action="patient.delete", resource_type="patient",
        resource_id=str(patient_id), ip_address=request.client.host if request.client else None,
    )
