"""Application service that centralizes audit-log writes so every mutating
action across the API funnels through one place (see app/middleware/audit.py
for the HTTP-level hook)."""
from __future__ import annotations

from typing import Any
from uuid import UUID

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_repository import AuditLogRepository


class AuditService:
    def __init__(self, audit_repository: AuditLogRepository):
        self.repo = audit_repository

    async def record(
        self, actor_id: UUID | None, action: str, resource_type: str, resource_id: str,
        metadata: dict[str, Any] | None = None, ip_address: str | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            actor_id=actor_id, action=action, resource_type=resource_type,
            resource_id=resource_id, metadata=metadata or {}, ip_address=ip_address,
        )
        return await self.repo.create(entry)

    async def list_recent(self, skip: int = 0, limit: int = 100) -> list[AuditLog]:
        return await self.repo.list(skip=skip, limit=limit)
