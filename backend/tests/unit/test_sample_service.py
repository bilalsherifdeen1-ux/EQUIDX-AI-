"""Unit tests for SampleService covering barcode generation and status
transitions."""
import pytest

from app.application.services.sample_service import SampleService, generate_barcode
from app.domain.entities.sample import Sample, SampleStatus, SampleType


class FakeSampleRepository:
    def __init__(self):
        self.samples: dict = {}

    async def create(self, sample: Sample) -> Sample:
        self.samples[sample.id] = sample
        return sample

    async def get_by_id(self, sample_id):
        return self.samples.get(sample_id)

    async def get_by_barcode(self, barcode):
        return next((s for s in self.samples.values() if s.barcode == barcode), None)

    async def list_by_patient(self, patient_id):
        return [s for s in self.samples.values() if s.patient_id == patient_id]

    async def list(self, skip=0, limit=50):
        return list(self.samples.values())

    async def update(self, sample: Sample) -> Sample:
        self.samples[sample.id] = sample
        return sample


def test_generate_barcode_format():
    barcode = generate_barcode("urinalysis")
    assert barcode.startswith("EQX-URI-")


@pytest.mark.asyncio
async def test_register_sample_assigns_barcode():
    import uuid

    repo = FakeSampleRepository()
    service = SampleService(repo)
    sample = Sample(patient_id=uuid.uuid4(), sample_type=SampleType.HBA1C, barcode="")
    created = await service.register_sample(sample)
    assert created.barcode.startswith("EQX-HBA")


@pytest.mark.asyncio
async def test_update_status_transitions():
    import uuid

    repo = FakeSampleRepository()
    service = SampleService(repo)
    sample = await service.register_sample(
        Sample(patient_id=uuid.uuid4(), sample_type=SampleType.BLOOD_CHEMISTRY, barcode="")
    )
    updated = await service.update_status(sample.id, SampleStatus.PROCESSING)
    assert updated.status == SampleStatus.PROCESSING
