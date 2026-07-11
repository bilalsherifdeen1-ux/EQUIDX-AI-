"""Concrete SQLAlchemy implementation of PatientRepository."""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.patient import Patient, Sex
from app.infrastructure.db.models.orm_models import PatientModel


def _to_entity(m: PatientModel) -> Patient:
    return Patient(
        id=m.id, mrn=m.mrn, first_name=m.first_name, last_name=m.last_name,
        date_of_birth=m.date_of_birth, sex=Sex(m.sex), is_synthetic=m.is_synthetic,
        contact_email=m.contact_email, notes=m.notes, created_by=m.created_by,
        created_at=m.created_at, updated_at=m.updated_at,
    )


class SqlPatientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, patient: Patient) -> Patient:
        m = PatientModel(
            id=patient.id, mrn=patient.mrn, first_name=patient.first_name, last_name=patient.last_name,
            date_of_birth=patient.date_of_birth, sex=patient.sex.value, is_synthetic=patient.is_synthetic,
            contact_email=patient.contact_email, notes=patient.notes, created_by=patient.created_by,
        )
        self.session.add(m)
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def get_by_id(self, patient_id: UUID) -> Patient | None:
        m = await self.session.get(PatientModel, patient_id)
        return _to_entity(m) if m else None

    async def get_by_mrn(self, mrn: str) -> Patient | None:
        result = await self.session.execute(select(PatientModel).where(PatientModel.mrn == mrn))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list(self, skip: int = 0, limit: int = 50, search: str | None = None) -> list[Patient]:
        query = select(PatientModel)
        if search:
            like = f"%{search}%"
            query = query.where(
                or_(PatientModel.first_name.ilike(like), PatientModel.last_name.ilike(like), PatientModel.mrn.ilike(like))
            )
        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, patient: Patient) -> Patient:
        m = await self.session.get(PatientModel, patient.id)
        if m is None:
            raise ValueError("Patient not found")
        m.first_name = patient.first_name
        m.last_name = patient.last_name
        m.contact_email = patient.contact_email
        m.notes = patient.notes
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def delete(self, patient_id: UUID) -> None:
        m = await self.session.get(PatientModel, patient_id)
        if m:
            await self.session.delete(m)
            await self.session.commit()
