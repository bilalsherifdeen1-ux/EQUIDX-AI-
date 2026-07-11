"""Notification entity for the in-app / email notification service."""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


class NotificationType(str, enum.Enum):
    REPORT_READY = "report_ready"
    SAMPLE_STATUS_CHANGE = "sample_status_change"
    SYSTEM = "system"


@dataclass
class Notification:
    user_id: UUID
    type: NotificationType
    title: str
    body: str
    read: bool = False
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
