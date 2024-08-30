from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from joltik.models import Customers
from joltik.models.factories import CustomersFactory
from joltik.routes.customers import CustomerResponse


def customer_to_pydantic(customer: Customers) -> CustomerResponse:
    return CustomerResponse.model_validate(customer)


def test_customers_CRUD(client: TestClient) -> None:
    resp = client.get("/customer")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Generate a customer
    customer_instance = CustomersFactory()
    customer_example = customer_to_pydantic(customer_instance).model_dump(mode="json")
    del customer_example["id"]

    # Test for POST customer
    resp = client.post("/customer", json=customer_example)
    assert resp.status_code == status.HTTP_201_CREATED
    returned_customer = {"id": resp.json()["id"], **customer_example}
    assert resp.json() == returned_customer
    resp = client.get("/customer")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == [returned_customer]

    # Test for GET ONE customer by id
    customer_id = returned_customer.get("id")
    resp = client.get(f"/customer/{customer_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == returned_customer
    nonexistent_id = uuid4()
    resp = client.get(f"/customer/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for UPDATE customer info
    update_customer_instance = CustomersFactory()
    update_customer = customer_to_pydantic(update_customer_instance).model_dump(mode="json")
    del update_customer["id"]

    customer_id = returned_customer.get("id")
    resp = client.put(f"/customer/{customer_id}", json=update_customer)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    resp = client.put(f"/customer/{nonexistent_id}", json=update_customer)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    updated_customer = client.get(f"/customer/{customer_id}").json()
    update_customer = {"id": customer_id, **update_customer}
    assert updated_customer == update_customer

    # Test for DELETE customer by id
    customer_id = returned_customer.get("id")
    resp = client.delete(f"/customer/{customer_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/customer/{customer_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/customer/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
