"""
GraphQL schema (Strawberry) exposing read-oriented queries over the same
application services used by the REST API — demonstrating the dual
REST + GraphQL API surface requested for research/analytics consumers who
want to shape their own queries.
"""
from __future__ import annotations

from typing import Optional
from uuid import UUID

import strawberry
from strawberry.types import Info

from app.infrastructure.db.repositories.patient_repository import SqlPatientRepository
from app.infrastructure.db.repositories.report_repository import SqlReportRepository
from app.infrastructure.db.repositories.sample_repository import SqlSampleRepository


@strawberry.type
class PatientType:
    id: strawberry.ID
    mrn: str
    first_name: str
    last_name: str
    sex: str
    is_synthetic: bool


@strawberry.type
class SampleType:
    id: strawberry.ID
    patient_id: strawberry.ID
    sample_type: str
    barcode: str
    status: str


@strawberry.type
class ReportType:
    id: strawberry.ID
    sample_id: strawberry.ID
    model_name: str
    model_version: str
    disclaimer: str
    reviewed: bool


@strawberry.type
class Query:
    @strawberry.field
    async def patients(self, info: Info, search: Optional[str] = None, limit: int = 50) -> list[PatientType]:
        session = info.context["db"]
        repo = SqlPatientRepository(session)
        patients = await repo.list(limit=limit, search=search)
        return [
            PatientType(
                id=strawberry.ID(str(p.id)), mrn=p.mrn, first_name=p.first_name,
                last_name=p.last_name, sex=p.sex.value, is_synthetic=p.is_synthetic,
            )
            for p in patients
        ]

    @strawberry.field
    async def samples(self, info: Info, patient_id: Optional[str] = None) -> list[SampleType]:
        session = info.context["db"]
        repo = SqlSampleRepository(session)
        samples = await repo.list_by_patient(UUID(patient_id)) if patient_id else await repo.list()
        return [
            SampleType(
                id=strawberry.ID(str(s.id)), patient_id=strawberry.ID(str(s.patient_id)),
                sample_type=s.sample_type.value, barcode=s.barcode, status=s.status.value,
            )
            for s in samples
        ]

    @strawberry.field
    async def reports_for_sample(self, info: Info, sample_id: str) -> list[ReportType]:
        session = info.context["db"]
        repo = SqlReportRepository(session)
        reports = await repo.list_by_sample(UUID(sample_id))
        return [
            ReportType(
                id=strawberry.ID(str(r.id)), sample_id=strawberry.ID(str(r.sample_id)),
                model_name=r.model_name, model_version=r.model_version,
                disclaimer=r.disclaimer, reviewed=r.reviewed,
            )
            for r in reports
        ]


schema = strawberry.Schema(query=Query)
