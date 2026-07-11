from __future__ import annotations

from typing import Protocol

from app.domain.entities.audit_log import AuditLog


class AuditLogRepository(Protocol):
    async def create(self, entry: AuditLog) -> AuditLog: ...
    async def list(self, skip: int = 0, limit: int = 100) -> list[AuditLog]: ...
