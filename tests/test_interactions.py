from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

from joltik.models import Interactions
from joltik.models.factories import (
    ContactsFactory,
    CustomersFactory,
    InteractionsFactory,
)
from joltik.routes.interactions import InteractionCreate, InteractionUpdate
from tests.test_contacts import contact_to_pydantic
from tests.test_customers import customer_to_pydantic


def interaction_to_pydantic(interaction: Interactions) -> InteractionCreate:
    return InteractionCreate.model_validate(interaction)


def test_interactions_CRUD(client: TestClient) -> None:
    resp = client.get("/interaction")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST interaction
    customer_sqla = CustomersFactory()
    customer_dict = customer_to_pydantic(customer_sqla).model_dump(mode="json")
    customer_pyd = client.post("/customer", json=customer_dict)
    assert customer_pyd.status_code == status.HTTP_201_CREATED
    customer_sqla.id = customer_pyd.json()["id"]

    contacts_sqla = ContactsFactory.create_batch(2, customer=customer_sqla)
    for contact in contacts_sqla:
        contact_dict = contact_to_pydantic(contact).model_dump(mode="json")
        resp = client.post("/contact", json=contact_dict)
        assert resp.status_code == status.HTTP_201_CREATED
        contact.id = resp.json()["id"]

    interaction_sqla = InteractionsFactory(customer=customer_sqla, contacts=contacts_sqla)
    interaction_dict = interaction_to_pydantic(interaction_sqla).model_dump(mode="json")
    resp = client.post("/interaction", json=interaction_dict)
    assert resp.status_code == status.HTTP_201_CREATED
    interaction_id = resp.json()["id"]
    returned_interaction = {"id": interaction_id, **interaction_dict}
    assert resp.json() == returned_interaction

    # new_interaction_sqla_list, interaction_contacts_sqla_list = generate_interaction(
    #     customer=customer_sqla,
    #     contacts=contacts_sqla,
    #     num_interactions=1,
    # )
    # new_interaction_sqla = new_interaction_sqla_list[0]
    # new_interaction_sqla.customer_fk = customer_sqla.id
    # contacts = contacts_sqla
    # new_interaction_sqla.contacts = contacts

    # new_interaction_dict = interaction_to_pydantic(new_interaction_sqla).model_dump(mode="json")
    # resp = client.post("/interaction", json=new_interaction_dict)
    # assert resp.status_code == status.HTTP_201_CREATED
    # interaction_id = resp.json()["id"]
    # returned_interaction = {"id": interaction_id, **new_interaction_dict}
    # assert resp.json() == returned_interaction

    # Test for GET interaction by id
    resp = client.get(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == returned_interaction

    # Test for UPDATE interaction by id
    new_customer_sqla = CustomersFactory()
    new_customer_dict = customer_to_pydantic(new_customer_sqla).model_dump(mode="json")
    new_customer_pyd = client.post("/customer", json=new_customer_dict)
    new_customer_sqla.id = new_customer_pyd.json()["id"]

    new_contact1_sqla = ContactsFactory(customer=new_customer_sqla)
    new_contact1_dict = contact_to_pydantic(new_contact1_sqla).model_dump(mode="json")
    new_contact1_pyd = client.post("/contact", json=new_contact1_dict)
    new_contact1_sqla.id = new_contact1_pyd.json()["id"]

    updated_inter_both_dict = InteractionUpdate(
        customer_fk=new_customer_sqla.id,
        contacts=[{"id": new_contact1_sqla.id}],
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/interaction/{interaction_id}", json=updated_inter_both_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_inter_both_dict = {**returned_interaction, **updated_inter_both_dict}
    assert resp.json() == updated_inter_both_dict
    resp = client.get(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_inter_both_dict

    # Test for update - contacts only
    new_contact2_sqla = ContactsFactory(customer=new_customer_sqla)
    new_contact2_dict = contact_to_pydantic(new_contact2_sqla).model_dump(mode="json")
    new_contact2_pyd = client.post("/contact", json=new_contact2_dict)
    new_contact2_sqla.id = new_contact2_pyd.json()["id"]

    updated_inter_contact_dict = InteractionUpdate(
        contacts=[{"id": new_contact2_sqla.id}],
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/interaction/{interaction_id}", json=updated_inter_contact_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_inter_contact_dict = {**updated_inter_both_dict, **updated_inter_contact_dict}
    assert resp.json() == updated_inter_contact_dict
    resp = client.get(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_inter_contact_dict

    # Test for UPDATE interaction - Update other fields only
    updated_inter_other_dict = InteractionUpdate(
        type="Updated Type",
        description="Updated description",
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/interaction/{interaction_id}", json=updated_inter_other_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_inter_other_dict = {**updated_inter_contact_dict, **updated_inter_other_dict}
    assert resp.json() == updated_inter_other_dict
    resp = client.get(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_inter_other_dict

    nonexistent_id = uuid4()
    resp = client.put(f"interaction/{nonexistent_id}", json=updated_inter_other_dict)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Test for DELETE interaction by id
    resp = client.delete(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/interaction/{interaction_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.get(f"/interaction/{nonexistent_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

    # Delete all data from DB
    for contact in contacts_sqla:
        resp = client.delete(f"/contact/{contact.id}")
        assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/contact/{new_contact1_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/contact/{new_contact2_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/customer/{customer_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/customer/{new_customer_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
