"""Application service for the notification system (in-app; email/SMS
adapters can be added under infrastructure/notifications later)."""
from __future__ import annotations

from uuid import UUID

from app.domain.entities.notification import Notification, NotificationType
from app.domain.repositories.notification_repository import NotificationRepository


class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.repo = notification_repository

    async def notify(self, user_id: UUID, type: NotificationType, title: str, body: str) -> Notification:
        notification = Notification(user_id=user_id, type=type, title=title, body=body)
        return await self.repo.create(notification)

    async def list_for_user(self, user_id: UUID, unread_only: bool = False) -> list[Notification]:
        return await self.repo.list_for_user(user_id, unread_only=unread_only)

    async def mark_read(self, notification_id: UUID) -> None:
        await self.repo.mark_read(notification_id)
