from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.notification import Notification, NotificationType
from app.infrastructure.db.models.orm_models import NotificationModel


def _to_entity(m: NotificationModel) -> Notification:
    return Notification(
        id=m.id, user_id=m.user_id, type=NotificationType(m.type), title=m.title,
        body=m.body, read=m.read, created_at=m.created_at,
    )


class SqlNotificationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        m = NotificationModel(
            id=notification.id, user_id=notification.user_id, type=notification.type.value,
            title=notification.title, body=notification.body, read=notification.read,
        )
        self.session.add(m)
        await self.session.commit()
        return _to_entity(m)

    async def list_for_user(self, user_id: UUID, unread_only: bool = False) -> list[Notification]:
        query = select(NotificationModel).where(NotificationModel.user_id == user_id)
        if unread_only:
            query = query.where(NotificationModel.read.is_(False))
        result = await self.session.execute(query.order_by(NotificationModel.created_at.desc()))
        return [_to_entity(m) for m in result.scalars().all()]

    async def mark_read(self, notification_id: UUID) -> None:
        m = await self.session.get(NotificationModel, notification_id)
        if m:
            m.read = True
            await self.session.commit()
