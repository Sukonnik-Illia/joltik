import re
import uuid
from typing import Union

from faker import Faker

from joltik.helpers import SERVICE
from joltik.models.contacts import ContactsModel
from joltik.models.customers import CustomerModel
from joltik.models.deals import DealsModel
from joltik.models.interactions import InteractionContacts, InteractionsModel
from joltik.models.services import ServicesModel

fake = Faker()
# Faker.seed(1234)


def generate_customer() -> CustomerModel:
    company_name = fake.company()
    email_username = re.sub(r"\W+", "", company_name).lower()
    email = f"{email_username}@{email_username}.com"

    return CustomerModel(
        id=uuid.uuid4(),
        company_name=company_name,
        industry=fake.bs(),
        address=fake.address(),
        email=email,
        phone_number=fake.phone_number(),
        lead_status=fake.random_element(
            elements=("New", "Connected", "Proposal", "Client", "Lost"),
        ),
    )


def generate_contact(customer: Union[CustomerModel, None] = None) -> ContactsModel:
    if customer is None:
        customer = generate_customer()

    first_name = fake.first_name()
    last_name = fake.last_name()
    company_name = customer.company_name
    email_domain = re.sub(r"\W+", "", company_name).lower()
    email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}.com"

    return ContactsModel(
        id=uuid.uuid4(),
        first_name=first_name,
        last_name=last_name,
        job_title=fake.job(),
        email=email,
        phone_number=fake.phone_number(),
        comment=fake.sentence(),
        customer=customer,
    )


def generate_interaction(
    customer: Union[CustomerModel, None] = None,
    contacts: Union[ContactsModel, list[ContactsModel], None] = None,
    num_interactions: int = 1,
) -> tuple[Union[list[InteractionsModel], list[InteractionContacts]]]:
    if isinstance(contacts, ContactsModel):
        contacts = [contacts]

    # if customer is none, but contacts provided, then customer is taken from contacts
    if customer is None:
        if contacts is None:
            customer = generate_customer()
            contact = generate_contact(customer)
            contacts = [contact]
        else:
            customer = contacts[0].customer
    elif contacts is None:
        contacts = customer.contacts
        if not contacts:
            contact = generate_contact(customer)
            contacts = [contact]

    interactions = []
    interactions_contacts_list = []

    for _ in range(num_interactions):
        interaction = InteractionsModel(
            id=uuid.uuid4(),
            date=fake.date_between(start_date="-1y", end_date="today").strftime("%Y%m%d"),
            type=fake.random_element(elements=("Call", "Email", "Meeting")),
            description=fake.sentence(),
            customer=customer,
        )
        # Select contacts from the customers contact list to associate with the interaction
        interaction_contacts = [
            InteractionContacts(interactions_fk=interaction.id, contacts_fk=contact.id)
            for contact in contacts
        ]

        interactions_contacts_list.extend(interaction_contacts)
        interactions.append(interaction)

    return interactions, interactions_contacts_list


def import_services() -> list[ServicesModel]:
    return [ServicesModel(**service_dict) for service_dict in SERVICE]


def generate_deal(
    service: Union[ServicesModel, None] = None,
    customer: Union[CustomerModel, None] = None,
    contact: Union[ContactsModel, None] = None,
) -> DealsModel:
    if service is None:
        services = import_services()
        service = fake.random_element(services)

    if customer is None:
        if contact is None:
            customer = generate_customer()
            contact = generate_contact(customer)
        else:
            customer = contact.customer
    elif contact is None:
        contact = customer.contacts
        if not contact:
            contact = generate_contact(customer)

    return DealsModel(
        id=uuid.uuid4(),
        deal_name=fake.catch_phrase(),
        deal_type=fake.random_element(elements=("New business", "Existing Business")),
        stage=fake.random_element(
            elements=("Prospecting", "Qualified", "Negotiation", "Won", "Lost"),
        ),
        ammount=fake.random_int(min=10000, max=1000000),
        comments=fake.text(),
        service=service,
        customer=customer,
        contact=contact,
    )


# fake_customer = generate_customer()
# fake_contact = generate_contact(fake_customer)
# fake_deal = generate_deal(customer=fake_customer, contact=fake_contact)
# print(fake_deal)
