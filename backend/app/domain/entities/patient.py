"""
Patient domain entity.

IMPORTANT: In this repository all patient records are SYNTHETIC — generated
by Faker or the biosensor simulator for demonstration purposes only. Nothing
here represents or should ever be populated with real personal health
information (PHI).
"""
from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import date, datetime
from uuid import UUID, uuid4


class Sex(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNDISCLOSED = "undisclosed"


@dataclass
class Patient:
    mrn: str  # synthetic medical record number
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex
    is_synthetic: bool = True
    contact_email: str | None = None
    notes: str | None = None
    id: UUID = field(default_factory=uuid4)
    created_by: UUID | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
