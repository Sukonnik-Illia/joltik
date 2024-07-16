from uuid import uuid4

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from joltik.models import Customers
from joltik.models.tables_faker_data import generate_customer
from joltik.routes.customers import CustomerResponse


def customer_to_pydantic(customer: Customers) -> CustomerResponse:
    return CustomerResponse.model_validate(customer)


customer_example = generate_customer()
customer_example = customer_to_pydantic(customer_example).model_dump(mode="json")
del customer_example["id"]


def test_customers_CRUD(client, db_session: AsyncSession) -> None:  # noqa: N802, ANN001, ARG001
    resp = client.get("/customer")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

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
    update_customer = generate_customer()
    update_customer = customer_to_pydantic(update_customer).model_dump(mode="json")
    del update_customer["id"]

    customer_id = returned_customer.get("id")
    resp = client.put(f"/customer/{customer_id}", json=update_customer)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    updated_customer = client.get(f"/customer/{customer_id}").json()
    update_customer = {"id": customer_id, **update_customer}
    assert updated_customer == update_customer
    resp = client.put(f"/customer/{nonexistent_id}", json=update_customer)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for DELETE customer by id
    customer_id = returned_customer.get("id")
    resp = client.delete(f"/customer/{customer_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/customer/{customer_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/customer/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
