from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

service_example = {
    "service_type": "SEO",
    "description": "Optimize your website to rank higher in search engine results.",
}


# https://fastapi.tiangolo.com/advanced/async-tests/
# @pytest.mark.anyio
@pytest.mark.asyncio()
async def test_services_CRUD(async_client: AsyncClient) -> None:  # noqa: N802
    resp = await async_client.get("/service")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST service
    resp = await async_client.post(
        "/service",
        json={
            "service_type": "SEO",
            "description": "Optimize your website to rank higher in search engine results.",
        },
    )
    assert resp.status_code == status.HTTP_201_CREATED
    returned_service = {"id": resp.json()["id"], **service_example}
    assert resp.json() == returned_service
    resp = await async_client.get("/service")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == [returned_service]

    # Test for GET ONE service by id
    service_id = returned_service.get("id")
    resp = await async_client.get(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == returned_service
    nonexistent_id = uuid4()
    resp = await async_client.get(f"/service/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for UPDATE service info
    service_id = returned_service.get("id")
    update_service = {"service_type": "PPC", "description": "Updated PPC service description"}
    resp = await async_client.put(f"/service/{service_id}", json=update_service)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    updated_service = await async_client.get(f"/service/{service_id}").json()
    update_service = {"id": service_id, **update_service}
    assert updated_service == update_service
    resp = await async_client.put(f"/service/{nonexistent_id}", json=update_service)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for DELETE service by id
    service_id = returned_service.get("id")
    resp = await async_client.delete(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = await async_client.get(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = await async_client.delete(f"/service/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
