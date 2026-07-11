"""User domain entity. Pure Python — no ORM/framework dependency, per Clean
Architecture: the domain layer must not know how it is persisted or served."""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CLINICIAN = "clinician"
    RESEARCHER = "researcher"
    LAB_TECH = "lab_tech"
    PATIENT = "patient"


@dataclass
class User:
    email: str
    hashed_password: str
    full_name: str
    role: UserRole = UserRole.RESEARCHER
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
