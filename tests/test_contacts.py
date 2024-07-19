from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from joltik.models import Contacts
from joltik.models.tables_faker_data import generate_contact, generate_customer
from joltik.routes.contacts import ContactCreate
from tests.test_customers import customer_to_pydantic


def contact_to_pydantic(contact: Contacts) -> ContactCreate:
    return ContactCreate.model_validate(contact)


def test_contacts_CRUD(client: TestClient) -> None:
    resp = client.get("/contact")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST contact
    customer1_sqla = generate_customer()
    customer1_dict = customer_to_pydantic(customer1_sqla).model_dump(mode="json")
    customer1_pyd = client.post("/customer", json=customer1_dict)
    customer1_sqla.id = customer1_pyd.json()["id"]

    contact_sqla = generate_contact(customer1_sqla)
    contact_dict = contact_to_pydantic(contact_sqla).model_dump(mode="json")

    resp = client.post("/contact", json=contact_dict)
    assert resp.status_code == status.HTTP_201_CREATED
    returned_contact = {"id": resp.json()["id"], **contact_dict}
    assert resp.json() == returned_contact
    resp = client.get("/contact")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == [returned_contact]

    # Test for UPDATE contact info
    # contact data update
    updated_contact = generate_contact(customer1_sqla)
    updated_contact = contact_to_pydantic(updated_contact).model_dump(mode="json")
    del updated_contact["customer"]

    contact_id = returned_contact.get("id")
    resp = client.put(f"/contact/{contact_id}", json=updated_contact)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    # updated_contact = client.get(f"/contact/{contact_id}").json()
    updated_contact = {
        "id": contact_id,
        **updated_contact,
        "customer": returned_contact.get("customer"),
    }
    assert resp.json() == updated_contact

    resp = client.get(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_contact

    # contact's customer relationship updating
    customer2_sqla = generate_customer()
    customer2_dict = customer_to_pydantic(customer2_sqla).model_dump(mode="json")
    customer2_pyd = client.post("/customer", json=customer2_dict)
    customer2_sqla.id = customer2_pyd.json()["id"]

    update_customer_data = {"customer": {"id": customer2_sqla.id}}
    resp = client.put(f"/contact/{contact_id}", json=update_customer_data)
    assert resp.status_code == status.HTTP_202_ACCEPTED

    updated_contact = {**updated_contact, "customer": {"id": customer2_sqla.id}}
    assert resp.json() == updated_contact

    resp = client.get(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_contact

    nonexistent_id = uuid4()
    resp = client.put(f"/contact/{nonexistent_id}", json=updated_contact)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for DELETE contact by id
    contact_id = returned_contact.get("id")
    resp = client.delete(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/contact/{contact_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/contact/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # delete customer at the end of the test
    resp = client.delete(f"/customer/{customer1_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/customer/{customer2_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
