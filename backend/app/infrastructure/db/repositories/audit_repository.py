from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.audit_log import AuditLog
from app.infrastructure.db.models.orm_models import AuditLogModel


def _to_entity(m: AuditLogModel) -> AuditLog:
    return AuditLog(
        id=m.id, actor_id=m.actor_id, action=m.action, resource_type=m.resource_type,
        resource_id=m.resource_id, metadata=m.log_metadata, ip_address=m.ip_address, created_at=m.created_at,
    )


class SqlAuditLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entry: AuditLog) -> AuditLog:
        m = AuditLogModel(
            id=entry.id, actor_id=entry.actor_id, action=entry.action, resource_type=entry.resource_type,
            resource_id=entry.resource_id, log_metadata=entry.metadata, ip_address=entry.ip_address,
        )
        self.session.add(m)
        await self.session.commit()
        return _to_entity(m)

    async def list(self, skip: int = 0, limit: int = 100) -> list[AuditLog]:
        result = await self.session.execute(
            select(AuditLogModel).order_by(AuditLogModel.created_at.desc()).offset(skip).limit(limit)
        )
        return [_to_entity(m) for m in result.scalars().all()]
