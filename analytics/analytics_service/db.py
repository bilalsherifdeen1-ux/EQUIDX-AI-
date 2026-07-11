"""Read-mostly async DB access for the analytics service — talks to the
same Postgres database as the backend, but never writes to transactional
tables (separation of read/aggregate workloads from the OLTP path)."""
import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://equidx:equidx_dev_password@postgres:5432/equidx"
)
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)


async def fetch_counts() -> dict:
    async with engine.connect() as conn:
        patients = (await conn.execute(text("SELECT count(*) FROM patients"))).scalar_one_or_none() or 0
        samples = (await conn.execute(text("SELECT count(*) FROM samples"))).scalar_one_or_none() or 0
        reports = (await conn.execute(text("SELECT count(*) FROM reports"))).scalar_one_or_none() or 0
        by_status = await conn.execute(text("SELECT status, count(*) FROM samples GROUP BY status"))
        by_type = await conn.execute(text("SELECT sample_type, count(*) FROM samples GROUP BY sample_type"))
        return {
            "total_patients": patients,
            "total_samples": samples,
            "total_reports": reports,
            "samples_by_status": {row[0]: row[1] for row in by_status},
            "samples_by_type": {row[0]: row[1] for row in by_type},
        }
