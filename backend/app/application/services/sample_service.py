"""Application service for sample registration and lifecycle tracking."""
from __future__ import annotations

import secrets
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.entities.sample import Sample, SampleStatus
from app.domain.repositories.sample_repository import SampleRepository


def generate_barcode(sample_type: str) -> str:
    return f"EQX-{sample_type[:3].upper()}-{secrets.token_hex(4).upper()}"


class SampleService:
    def __init__(self, sample_repository: SampleRepository):
        self.repo = sample_repository

    async def register_sample(self, sample: Sample) -> Sample:
        if not sample.barcode:
            sample.barcode = generate_barcode(sample.sample_type.value)
        return await self.repo.create(sample)

    async def get_sample(self, sample_id: UUID) -> Sample:
        sample = await self.repo.get_by_id(sample_id)
        if not sample:
            raise NotFoundError(f"Sample {sample_id} not found")
        return sample

    async def list_samples(self, skip: int = 0, limit: int = 50) -> list[Sample]:
        return await self.repo.list(skip=skip, limit=limit)

    async def list_for_patient(self, patient_id: UUID) -> list[Sample]:
        return await self.repo.list_by_patient(patient_id)

    async def update_status(self, sample_id: UUID, status: SampleStatus) -> Sample:
        sample = await self.get_sample(sample_id)
        sample.status = status
        return await self.repo.update(sample)

    async def attach_signal_reference(self, sample_id: UUID, storage_key: str) -> Sample:
        sample = await self.get_sample(sample_id)
        sample.raw_signal_ref = storage_key
        sample.status = SampleStatus.RECEIVED
        return await self.repo.update(sample)
