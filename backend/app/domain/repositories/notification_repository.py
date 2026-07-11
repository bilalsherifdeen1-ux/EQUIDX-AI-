from __future__ import annotations

from typing import Protocol
from uuid import UUID

from app.domain.entities.notification import Notification


class NotificationRepository(Protocol):
    async def create(self, notification: Notification) -> Notification: ...
    async def list_for_user(self, user_id: UUID, unread_only: bool = False) -> list[Notification]: ...
    async def mark_read(self, notification_id: UUID) -> None: ...
