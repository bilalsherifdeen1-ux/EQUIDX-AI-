"""Pydantic request/response DTOs (API boundary schemas). Kept separate from
domain entities so API contracts can evolve independently of the domain model."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.domain.entities.patient import Sex
from app.domain.entities.sample import SampleStatus, SampleType
from app.domain.entities.user import UserRole


# ---- Auth ----
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: UserRole = UserRole.RESEARCHER


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ---- Patients ----
class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex
    contact_email: EmailStr | None = None
    notes: str | None = None


class PatientOut(BaseModel):
    id: UUID
    mrn: str
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex
    is_synthetic: bool
    contact_email: EmailStr | None
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Samples ----
class SampleCreate(BaseModel):
    patient_id: UUID
    sample_type: SampleType
    device_id: str | None = None


class SampleOut(BaseModel):
    id: UUID
    patient_id: UUID
    sample_type: SampleType
    barcode: str
    status: SampleStatus
    device_id: str | None
    raw_signal_ref: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class SampleStatusUpdate(BaseModel):
    status: SampleStatus


# ---- Reports ----
class ReportOut(BaseModel):
    id: UUID
    sample_id: UUID
    model_name: str
    model_version: str
    findings: dict[str, Any]
    confidence_scores: dict[str, float]
    disclaimer: str
    reviewed: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Notifications ----
class NotificationOut(BaseModel):
    id: UUID
    type: str
    title: str
    body: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Audit ----
class AuditLogOut(BaseModel):
    id: UUID
    actor_id: UUID | None
    action: str
    resource_type: str
    resource_id: str
    metadata: dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
