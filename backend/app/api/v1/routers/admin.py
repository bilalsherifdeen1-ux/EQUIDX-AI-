"""Admin portal endpoints — user management and audit log access. All
routes require the ADMIN role via the require_roles RBAC dependency."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.schemas import AuditLogOut, UserOut
from app.application.services.audit_service import AuditService
from app.core.deps import CurrentUser, get_audit_repository, get_user_repository, require_roles
from app.domain.entities.user import UserRole
from app.infrastructure.db.repositories.audit_repository import SqlAuditLogRepository
from app.infrastructure.db.repositories.user_repository import SqlUserRepository

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[UserOut])
async def list_users(
    skip: int = 0, limit: int = 50,
    _: CurrentUser = Depends(require_roles(UserRole.ADMIN)),
    user_repo: SqlUserRepository = Depends(get_user_repository),
):
    return await user_repo.list(skip=skip, limit=limit)


@router.patch("/users/{user_id}/deactivate", response_model=UserOut)
async def deactivate_user(
    user_id: UUID,
    _: CurrentUser = Depends(require_roles(UserRole.ADMIN)),
    user_repo: SqlUserRepository = Depends(get_user_repository),
):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_active = False
    return await user_repo.update(user)


@router.patch("/users/{user_id}/role", response_model=UserOut)
async def change_user_role(
    user_id: UUID, role: UserRole,
    _: CurrentUser = Depends(require_roles(UserRole.ADMIN)),
    user_repo: SqlUserRepository = Depends(get_user_repository),
):
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.role = role
    return await user_repo.update(user)


@router.get("/audit-logs", response_model=list[AuditLogOut])
async def audit_logs(
    skip: int = 0, limit: int = 100,
    _: CurrentUser = Depends(require_roles(UserRole.ADMIN)),
    audit_repo: SqlAuditLogRepository = Depends(get_audit_repository),
):
    return await AuditService(audit_repo).list_recent(skip=skip, limit=limit)
