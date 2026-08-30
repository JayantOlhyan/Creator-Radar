"""Test Creator Watchlist REST API Routers."""
import pytest


@pytest.mark.asyncio
async def test_creators_api_lifecycle(async_api_client):
    # 1. Create Creator
    create_res = await async_api_client.post("/api/v1/creators", json={
        "platform": "instagram",
        "username": "apiguy",
        "check_interval_minutes": 30
    })
    assert create_res.status_code == 201
    res_data = create_res.json()
    assert res_data["success"] is True
    creator_id = res_data["data"]["id"]
    assert res_data["data"]["username"] == "apiguy"
    assert res_data["data"]["status"] == "ACTIVE"

    # 2. Duplicate Creator 409
    dup_res = await async_api_client.post("/api/v1/creators", json={
        "platform": "instagram",
        "username": "apiguy"
    })
    assert dup_res.status_code == 409

    # 3. Invalid Handle 400
    inv_res = await async_api_client.post("/api/v1/creators", json={
        "platform": "instagram",
        "username": "invalid_handle"
    })
    assert inv_res.status_code == 400

    # 4. List Creators
    list_res = await async_api_client.get("/api/v1/creators")
    assert list_res.status_code == 200
    creators_list = list_res.json()["data"]
    assert len(creators_list) >= 1

    # 5. Patch Creator Status
    patch_res = await async_api_client.patch(f"/api/v1/creators/{creator_id}", json={
        "status": "INACTIVE"
    })
    assert patch_res.status_code == 200
    assert patch_res.json()["data"]["status"] == "INACTIVE"

    # 6. Delete Creator
    del_res = await async_api_client.delete(f"/api/v1/creators/{creator_id}")
    assert del_res.status_code == 200
    assert del_res.json()["data"]["deleted"] is True
