"""
Composition-root style dependency wiring for FastAPI's `Depends`.

This is where interfaces (domain repository protocols) get bound to concrete
implementations (SQLAlchemy repositories). Swapping persistence technology
later means changing only this file, not the routers or services that
consume the repositories.
"""
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.security import decode_token
from app.domain.entities.user import UserRole
from app.infrastructure.db.session import get_session
from app.infrastructure.db.repositories.audit_repository import SqlAuditLogRepository
from app.infrastructure.db.repositories.patient_repository import SqlPatientRepository
from app.infrastructure.db.repositories.sample_repository import SqlSampleRepository
from app.infrastructure.db.repositories.report_repository import SqlReportRepository
from app.infrastructure.db.repositories.user_repository import SqlUserRepository
from app.infrastructure.db.repositories.notification_repository import SqlNotificationRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db(session: AsyncSession = Depends(get_session)) -> AsyncGenerator[AsyncSession, None]:
    yield session


def get_user_repository(db: AsyncSession = Depends(get_db)) -> SqlUserRepository:
    return SqlUserRepository(db)


def get_patient_repository(db: AsyncSession = Depends(get_db)) -> SqlPatientRepository:
    return SqlPatientRepository(db)


def get_sample_repository(db: AsyncSession = Depends(get_db)) -> SqlSampleRepository:
    return SqlSampleRepository(db)


def get_report_repository(db: AsyncSession = Depends(get_db)) -> SqlReportRepository:
    return SqlReportRepository(db)


def get_audit_repository(db: AsyncSession = Depends(get_db)) -> SqlAuditLogRepository:
    return SqlAuditLogRepository(db)


def get_notification_repository(db: AsyncSession = Depends(get_db)) -> SqlNotificationRepository:
    return SqlNotificationRepository(db)


class CurrentUser:
    def __init__(self, id: str, email: str, role: UserRole):
        self.id = id
        self.email = email
        self.role = role


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception
    sub = payload.get("sub")
    role = payload.get("role")
    if sub is None or role is None:
        raise credentials_exception
    return CurrentUser(id=sub, email=payload.get("email", ""), role=UserRole(role))


def require_roles(*roles: UserRole):
    """RBAC dependency factory — usage: `Depends(require_roles(UserRole.ADMIN))`."""

    async def _checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return current_user

    return _checker
