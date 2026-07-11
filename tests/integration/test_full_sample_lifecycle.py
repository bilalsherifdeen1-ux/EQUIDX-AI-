"""
End-to-end integration test across backend + ai-engine: register a
synthetic patient, register a sample, generate a placeholder diagnostic
report, and verify the disclaimer/confidence-score contract holds.

Requires the docker-compose stack to be running (`docker compose up -d`).
Skips gracefully if the backend isn't reachable, so this doesn't break CI
runs that only test individual services in isolation.
"""
import os

import httpx
import pytest

BACKEND_URL = os.getenv("EQUIDX_BACKEND_URL", "http://localhost:8000")


def _backend_reachable() -> bool:
    try:
        httpx.get(f"{BACKEND_URL}/health", timeout=2.0)
        return True
    except httpx.HTTPError:
        return False


pytestmark = pytest.mark.skipif(not _backend_reachable(), reason="backend not reachable — start docker compose stack")


@pytest.mark.asyncio
async def test_full_patient_sample_report_lifecycle():
    async with httpx.AsyncClient(base_url=BACKEND_URL, timeout=30.0) as client:
        # Register + login a researcher
        email = "integration-test@equidx.ai"
        await client.post(
            "/api/v1/auth/register",
            json={"email": email, "password": "supersecret1", "full_name": "Integration Test"},
        )
        login_resp = await client.post(
            "/api/v1/auth/login", data={"username": email, "password": "supersecret1"}
        )
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Register a synthetic patient
        patient_resp = await client.post(
            "/api/v1/patients",
            json={"first_name": "Test", "last_name": "Patient", "date_of_birth": "1990-01-01", "sex": "other"},
            headers=headers,
        )
        assert patient_resp.status_code == 201
        patient_id = patient_resp.json()["id"]

        # Register a sample
        sample_resp = await client.post(
            "/api/v1/samples",
            json={"patient_id": patient_id, "sample_type": "urinalysis"},
            headers=headers,
        )
        assert sample_resp.status_code == 201
        sample_id = sample_resp.json()["id"]

        # Generate a report
        report_resp = await client.post(f"/api/v1/reports/generate/{sample_id}", headers=headers)
        assert report_resp.status_code == 201
        report = report_resp.json()
        assert report["confidence_scores"]
        assert "not" in report["disclaimer"].lower()
