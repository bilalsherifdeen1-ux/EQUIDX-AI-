"""
Seeds the database with synthetic demo data: an admin user, a handful of
clinician/researcher accounts, synthetic patients, and sample records.

Run with: `python -m app.infrastructure.db.seed`
All data generated here is synthetic (Faker) — see README disclaimer.
"""
import asyncio
import random
from datetime import date

from faker import Faker

from app.core.security import hash_password
from app.domain.entities.patient import Patient, Sex
from app.domain.entities.sample import Sample, SampleType
from app.domain.entities.user import User, UserRole
from app.infrastructure.db.repositories.patient_repository import SqlPatientRepository
from app.infrastructure.db.repositories.sample_repository import SqlSampleRepository
from app.infrastructure.db.repositories.user_repository import SqlUserRepository
from app.infrastructure.db.session import AsyncSessionLocal

fake = Faker()


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        users = SqlUserRepository(session)
        patients = SqlPatientRepository(session)
        samples = SqlSampleRepository(session)

        admin = await users.create(
            User(email="admin@equidx.ai", hashed_password=hash_password("ChangeMe123!"),
                 full_name="EQUIDX Admin", role=UserRole.ADMIN)
        )
        clinician = await users.create(
            User(email="clinician@equidx.ai", hashed_password=hash_password("ChangeMe123!"),
                 full_name="Dr. Jordan Rivera", role=UserRole.CLINICIAN)
        )
        await users.create(
            User(email="researcher@equidx.ai", hashed_password=hash_password("ChangeMe123!"),
                 full_name="Dr. Alex Kim", role=UserRole.RESEARCHER)
        )

        for _ in range(25):
            patient = await patients.create(
                Patient(
                    mrn=f"SYN-{fake.unique.bothify('????####').upper()}",
                    first_name=fake.first_name(), last_name=fake.last_name(),
                    date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    sex=random.choice(list(Sex)), created_by=admin.id,
                )
            )
            for _ in range(random.randint(1, 3)):
                sample_type = random.choice(list(SampleType))
                await samples.create(
                    Sample(
                        patient_id=patient.id, sample_type=sample_type,
                        barcode=f"EQX-{sample_type.value[:3].upper()}-{fake.unique.bothify('########').upper()}",
                        collected_by=clinician.id,
                    )
                )

        print("Seed complete: 3 users, 25 synthetic patients, associated samples.")


if __name__ == "__main__":
    asyncio.run(seed())
