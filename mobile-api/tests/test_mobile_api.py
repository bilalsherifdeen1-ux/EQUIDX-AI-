"""Smoke test for the mobile BFF's health endpoint."""
from fastapi.testclient import TestClient

from mobile_api.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
