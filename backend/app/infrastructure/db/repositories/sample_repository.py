from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.sample import Sample, SampleStatus, SampleType
from app.infrastructure.db.models.orm_models import SampleModel


def _to_entity(m: SampleModel) -> Sample:
    return Sample(
        id=m.id, patient_id=m.patient_id, sample_type=SampleType(m.sample_type), barcode=m.barcode,
        status=SampleStatus(m.status), collected_by=m.collected_by, device_id=m.device_id,
        raw_signal_ref=m.raw_signal_ref, created_at=m.created_at, updated_at=m.updated_at,
    )


class SqlSampleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sample: Sample) -> Sample:
        m = SampleModel(
            id=sample.id, patient_id=sample.patient_id, sample_type=sample.sample_type.value,
            barcode=sample.barcode, status=sample.status.value, collected_by=sample.collected_by,
            device_id=sample.device_id, raw_signal_ref=sample.raw_signal_ref,
        )
        self.session.add(m)
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)

    async def get_by_id(self, sample_id: UUID) -> Sample | None:
        m = await self.session.get(SampleModel, sample_id)
        return _to_entity(m) if m else None

    async def get_by_barcode(self, barcode: str) -> Sample | None:
        result = await self.session.execute(select(SampleModel).where(SampleModel.barcode == barcode))
        m = result.scalar_one_or_none()
        return _to_entity(m) if m else None

    async def list_by_patient(self, patient_id: UUID) -> list[Sample]:
        result = await self.session.execute(select(SampleModel).where(SampleModel.patient_id == patient_id))
        return [_to_entity(m) for m in result.scalars().all()]

    async def list(self, skip: int = 0, limit: int = 50) -> list[Sample]:
        result = await self.session.execute(select(SampleModel).offset(skip).limit(limit))
        return [_to_entity(m) for m in result.scalars().all()]

    async def update(self, sample: Sample) -> Sample:
        m = await self.session.get(SampleModel, sample.id)
        if m is None:
            raise ValueError("Sample not found")
        m.status = sample.status.value
        m.raw_signal_ref = sample.raw_signal_ref
        await self.session.commit()
        await self.session.refresh(m)
        return _to_entity(m)
