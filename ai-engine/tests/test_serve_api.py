"""API-level tests for the ai-engine FastAPI service."""
from fastapi.testclient import TestClient

from ai_engine.serve import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_infer_urinalysis():
    resp = client.post("/api/v1/infer", json={"sample_type": "urinalysis", "sample_id": "sample-1"})
    assert resp.status_code == 200
    body = resp.json()
    assert "disclaimer" in body
    assert body["confidence_scores"]


def test_infer_unknown_domain_returns_400():
    resp = client.post("/api/v1/infer", json={"sample_type": "not_real", "sample_id": "x"})
    assert resp.status_code == 400
