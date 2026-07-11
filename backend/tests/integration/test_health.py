"""Integration test hitting the FastAPI app through httpx's ASGI transport."""
import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "research prototype" in body["disclaimer"].lower()


@pytest.mark.asyncio
async def test_register_and_login_flow(client):
    resp = await client.post(
        "/api/v1/auth/register",
        json={"email": "flow@equidx.ai", "password": "supersecret1", "full_name": "Flow Test"},
    )
    assert resp.status_code == 201

    resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "flow@equidx.ai", "password": "supersecret1"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()
