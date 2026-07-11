"""In-app notification endpoints."""
from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.dto.schemas import NotificationOut
from app.application.services.notification_service import NotificationService
from app.core.deps import CurrentUser, get_current_user, get_notification_repository
from app.infrastructure.db.repositories.notification_repository import SqlNotificationRepository

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationOut])
async def list_notifications(
    unread_only: bool = False,
    current_user: CurrentUser = Depends(get_current_user),
    notif_repo: SqlNotificationRepository = Depends(get_notification_repository),
):
    service = NotificationService(notif_repo)
    return await service.list_for_user(UUID(current_user.id), unread_only=unread_only)


@router.post("/{notification_id}/read", status_code=204)
async def mark_read(
    notification_id: UUID,
    current_user: CurrentUser = Depends(get_current_user),
    notif_repo: SqlNotificationRepository = Depends(get_notification_repository),
):
    await NotificationService(notif_repo).mark_read(notification_id)
