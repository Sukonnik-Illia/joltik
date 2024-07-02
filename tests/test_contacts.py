from uuid import uuid4

from fastapi import status

from joltik.models import Contacts
from joltik.models.tables_faker_data import generate_contact, generate_customer
from joltik.routes.contacts import ContactResponse
from tests.test_customers import customer_to_pydantic


def contact_to_pydantic(contact: Contacts) -> ContactResponse:
    return ContactResponse.model_validate(contact)


nonexistent_id = uuid4()


def test_contacts_CRUD(client) -> None:  # noqa: N802, ANN001
    resp = client.get("/contact")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST customer
    customer_example = generate_customer()
    customer = customer_to_pydantic(customer_example).model_dump(mode="json")
    del customer["id"]
    resp = client.post("/customer", json=customer)
    customer_id = resp.json()["id"]

    contact_example = generate_contact(customer_example)
    contact_example.customer_fk = customer_id
    contact_example = contact_to_pydantic(contact_example).model_dump(mode="json")
    del contact_example["id"]

    resp = client.post("/contact", json=contact_example)
    assert resp.status_code == status.HTTP_201_CREATED
    returned_contact = {"id": resp.json()["id"], **contact_example}
    assert resp.json() == returned_contact
    resp = client.get("/contact")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == [returned_contact]

    # Test for UPDATE contact info

    # Test for DELETE contact by id
    contact_id = returned_contact.get("id")
    resp = client.delete(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_200_OK
    resp = client.get(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/contact/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # delete customer at the end of the test
    resp = client.delete(f"/customer/{customer_id}")
