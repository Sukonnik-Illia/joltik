from fastapi import status

from joltik.models import Services
from joltik.models.tables_faker_data import generate_contact, generate_customer, generate_deal
from joltik.routes.deals import DealCreate, DealUpdate
from joltik.routes.services import ServiceCreate
from tests.test_contacts import contact_to_pydantic
from tests.test_customers import customer_to_pydantic


def test_deals_CRUD(client) -> None:  # noqa: N802, ANN001
    resp = client.get("/deal")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

    # Test for POST deal
    customer_sqla = generate_customer()
    customer_dict = customer_to_pydantic(customer_sqla).model_dump(mode="json")
    customer_pyd = client.post("/customer", json=customer_dict)
    customer_sqla.id = customer_pyd.json()["id"]

    contact_sqla = generate_contact(customer_sqla)
    contact_dict = contact_to_pydantic(contact_sqla).model_dump(mode="json")
    resp = client.post("/contact", json=contact_dict)
    contact_sqla.id = resp.json()["id"]

    service_sqla = Services(
        service_type="SEO",
        description="Improve site structure, load speed, and mobile-friendliness",
    )
    service_dict = ServiceCreate.model_validate(service_sqla).model_dump(mode="json")
    service_pyd = client.post("/service", json=service_dict)
    service_sqla.id = service_pyd.json()["id"]

    deal_sqla = generate_deal(customer=customer_sqla, contact=contact_sqla, service=service_sqla)
    deal_sqla.service_fk = service_sqla.id
    deal_sqla.customer_fk = customer_sqla.id
    deal_sqla.contact_fk = contact_sqla.id
    deal_dict = DealCreate.model_validate(deal_sqla).model_dump(mode="json")

    resp = client.post("/deal", json=deal_dict)
    assert resp.status_code == status.HTTP_201_CREATED
    returned_deal = {"id": resp.json()["id"], **deal_dict}
    assert resp.json() == returned_deal
    deal_id = returned_deal["id"]
    resp = client.get(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == returned_deal

    # Test for UPDATE deal
    new_service_sqla = Services(
        service_type="PPC",
        description="Develop ad strategies, conduct keyword research, and optimize ads.",
    )
    new_service_dict = ServiceCreate.model_validate(new_service_sqla).model_dump(mode="json")
    new_service_pyd = client.post("/service", json=new_service_dict)
    new_service_sqla.id = new_service_pyd.json()["id"]

    new_customer_sqla = generate_customer()
    new_customer_dict = customer_to_pydantic(new_customer_sqla).model_dump(mode="json")
    new_customer_pyd = client.post("/customer", json=new_customer_dict)
    new_customer_sqla.id = new_customer_pyd.json()["id"]

    new_contact1_sqla = generate_contact(new_customer_sqla)
    new_contact1_dict = contact_to_pydantic(new_contact1_sqla).model_dump(mode="json")
    new_contact1_pyd = client.post("/contact", json=new_contact1_dict)
    new_contact1_sqla.id = new_contact1_pyd.json()["id"]

    new_contact2_sqla = generate_contact(new_customer_sqla)
    new_contact2_dict = contact_to_pydantic(new_contact2_sqla).model_dump(mode="json")
    new_contact2_pyd = client.post("/contact", json=new_contact2_dict)
    new_contact2_sqla.id = new_contact2_pyd.json()["id"]

    # Update both customer and contact
    update_deal_both_dict = DealUpdate(
        customer_fk=new_customer_sqla.id,
        contact_fk=new_contact1_sqla.id,
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/deal/{deal_id}", json=update_deal_both_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_deal_both = {**returned_deal, **update_deal_both_dict}
    assert resp.json() == updated_deal_both
    resp = client.get(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_deal_both

    # Update contact only
    update_deal_contact_dict = DealUpdate(
        contact_fk=new_contact2_sqla.id,
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/deal/{deal_id}", json=update_deal_contact_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_deal_contact = {**updated_deal_both, **update_deal_contact_dict}
    assert resp.json() == updated_deal_contact
    resp = client.get(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_deal_contact

    # Update other fields
    update_deal_other_dict = DealUpdate(
        deal_name="Updated Deal",
        deal_type="Existing Business",
        stage="Won",
        ammount=50000,
        comments="Updated comments",
        service_fk=new_service_sqla.id,
    ).model_dump(mode="json", exclude_unset=True)

    resp = client.put(f"/deal/{deal_id}", json=update_deal_other_dict)
    assert resp.status_code == status.HTTP_200_OK
    updated_deal_other = {**updated_deal_contact, **update_deal_other_dict}
    assert resp.json() == updated_deal_other
    resp = client.get(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == updated_deal_other

    # Test for DELETE deal
    resp = client.delete(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.get(f"/deal/{deal_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    resp = client.delete(f"/contact/{contact_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/customer/{customer_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/service/{service_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/contact/{new_contact1_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/contact/{new_contact2_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/customer/{new_customer_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    resp = client.delete(f"/service/{new_service_sqla.id}")
    assert resp.status_code == status.HTTP_204_NO_CONTENT
