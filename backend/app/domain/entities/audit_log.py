"""Audit log entity — an immutable record of who did what to which resource,
required for any research/clinical-adjacent system."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass
class AuditLog:
    actor_id: UUID | None
    action: str  # e.g. "patient.create", "sample.update", "report.view"
    resource_type: str
    resource_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    ip_address: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
