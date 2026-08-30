"""Test FastAPI Endpoints via AsyncClient."""
import pytest


@pytest.mark.asyncio
async def test_root_endpoint(async_api_client):
    response = await async_api_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "CreatorRadar"


@pytest.mark.asyncio
async def test_health_endpoint(async_api_client):
    response = await async_api_client.get("/api/v1/health")
    assert response.status_code == 200
    res = response.json()
    assert "data" in res
    assert "services" in res["data"]
    assert res["data"]["services"]["api"] == "healthy"


@pytest.mark.asyncio
async def test_config_endpoint(async_api_client):
    response = await async_api_client.get("/api/v1/config")
    assert response.status_code == 200
    res = response.json()
    assert res["success"] is True
    assert "ai_provider" in res["data"]
    assert "supported_source_adapters" in res["data"]
