"""SQLAlchemy ORM models. These are intentionally separate from the domain
dataclasses in app/domain/entities — repositories translate between the two
so the domain layer stays persistence-agnostic."""
import enum
import uuid
from datetime import date, datetime

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.session import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="researcher")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PatientModel(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mrn: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[date] = mapped_column(Date)
    sex: Mapped[str] = mapped_column(String(20))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    samples: Mapped[list["SampleModel"]] = relationship(back_populates="patient")


class SampleModel(Base):
    __tablename__ = "samples"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("patients.id"))
    sample_type: Mapped[str] = mapped_column(String(50))
    barcode: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(30), default="registered")
    collected_by: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    raw_signal_ref: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    patient: Mapped["PatientModel"] = relationship(back_populates="samples")
    reports: Mapped[list["ReportModel"]] = relationship(back_populates="sample")


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sample_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("samples.id"))
    model_name: Mapped[str] = mapped_column(String(100))
    model_version: Mapped[str] = mapped_column(String(50))
    findings: Mapped[dict] = mapped_column(JSON)
    confidence_scores: Mapped[dict] = mapped_column(JSON)
    generated_by: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    disclaimer: Mapped[str] = mapped_column(Text)
    reviewed: Mapped[bool] = mapped_column(Boolean, default=False)
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    sample: Mapped["SampleModel"] = relationship(back_populates="reports")


class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_id: Mapped[uuid.UUID | None] = mapped_column(PG_UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    resource_type: Mapped[str] = mapped_column(String(100))
    resource_id: Mapped[str] = mapped_column(String(100))
    log_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    ip_address: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(255))
    body: Mapped[str] = mapped_column(Text)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
