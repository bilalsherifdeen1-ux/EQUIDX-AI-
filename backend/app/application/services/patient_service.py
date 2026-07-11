"""Application service for patient record management (synthetic/demo data)."""
from __future__ import annotations

from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domain.entities.patient import Patient
from app.domain.repositories.patient_repository import PatientRepository


class PatientService:
    def __init__(self, patient_repository: PatientRepository):
        self.repo = patient_repository

    async def register_patient(self, patient: Patient) -> Patient:
        patient.is_synthetic = True  # enforced: this platform never stores real PHI
        return await self.repo.create(patient)

    async def get_patient(self, patient_id: UUID) -> Patient:
        patient = await self.repo.get_by_id(patient_id)
        if not patient:
            raise NotFoundError(f"Patient {patient_id} not found")
        return patient

    async def list_patients(self, skip: int = 0, limit: int = 50, search: str | None = None) -> list[Patient]:
        return await self.repo.list(skip=skip, limit=limit, search=search)

    async def update_patient(self, patient: Patient) -> Patient:
        return await self.repo.update(patient)

    async def delete_patient(self, patient_id: UUID) -> None:
        await self.repo.delete(patient_id)
