from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

service_example = {
    "service_type": "SEO",
    "description": "Optimize your website to rank higher in search engine results.",
}


def test_services_CRUD(client: TestClient) -> None:
    resp = client.get("/service")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST service
    resp = client.post(
        "/service",
        json={
            "service_type": "SEO",
            "description": "Optimize your website to rank higher in search engine results.",
        },
    )
    assert resp.status_code == status.HTTP_201_CREATED
    returned_service = {"id": resp.json()["id"], **service_example}
    assert resp.json() == returned_service
    resp = client.get("/service")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == [returned_service]

    # Test for GET ONE service by id
    service_id = returned_service.get("id")
    resp = client.get(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == returned_service
    nonexistent_id = uuid4()
    resp = client.get(f"/service/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for UPDATE service info
    service_id = returned_service.get("id")
    update_service = {"service_type": "PPC", "description": "Updated PPC service description"}
    resp = client.put(f"/service/{service_id}", json=update_service)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    updated_service = client.get(f"/service/{service_id}").json()
    update_service = {"id": service_id, **update_service}
    assert updated_service == update_service
    resp = client.put(f"/service/{nonexistent_id}", json=update_service)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for DELETE service by id
    service_id = returned_service.get("id")
    resp = client.delete(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/service/{service_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/service/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
