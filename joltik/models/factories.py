import uuid
from random import randint

import factory
from factory import fuzzy
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from joltik.config import Config
from joltik.helpers import SERVICE
from joltik.models.contacts import Contacts
from joltik.models.customers import Customers
from joltik.models.deals import Deals
from joltik.models.interactions import InteractionContacts, Interactions
from joltik.models.services import Services

config = Config()

fake = Faker()
# Faker.seed(1234)


def import_services() -> list[Services]:
    return [Services(**service_dict) for service_dict in SERVICE]


services = import_services()


class CustomersFactory(factory.Factory):
    class Meta:
        model = Customers

    id = factory.LazyFunction(uuid.uuid4)
    company_name = factory.Faker("company")
    industry = factory.Faker("bs")
    address = factory.Faker("address")
    email = factory.LazyAttribute(
        lambda o: f"{o.company_name.replace(' ', '').lower()}@{o.company_name.replace(' ', '').lower()}.com",  # noqa: E501
    )
    phone_number = factory.Faker("phone_number")
    lead_status = fuzzy.FuzzyChoice(["New", "Connected", "Proposal", "Client", "Lost"])


class ContactsFactory(factory.Factory):
    class Meta:
        model = Contacts

    id = factory.LazyFunction(uuid.uuid4)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    job_title = factory.Faker("job")
    email = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com",
    )
    phone_number = factory.Faker("phone_number")
    comment = factory.Faker("sentence")
    customer = factory.SubFactory(CustomersFactory)
    customer_fk = factory.SelfAttribute("customer.id")


class InteractionContactsFactory(factory.Factory):
    class Meta:
        model = InteractionContacts

    interactions_fk = factory.LazyAttribute(lambda o: o.interaction.id)
    contacts_fk = factory.LazyAttribute(lambda o: o.contact.id)
    # interaction = factory.SubFactory("joltik.models.factories.InteractionsFactory", contacts=None)
    # contact = factory.SubFactory(ContactsFactory)


class InteractionsFactory(factory.Factory):
    class Meta:
        model = Interactions

    id = factory.LazyFunction(uuid.uuid4)
    date = factory.LazyFunction(
        lambda: int(
            fake.date_between(start_date="-1y", end_date="today").strftime("%Y%m%d"),
        ),
    )
    type = factory.Faker("random_element", elements=("Call", "Email", "Meeting"))
    description = factory.Faker("sentence")

    customer = factory.SubFactory(CustomersFactory)
    customer_fk = factory.SelfAttribute("customer.id")
    contacts = factory.SubFactory(CustomersFactory)

    # @factory.post_generation
    # def contacts(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #     if extracted:
    #         for contact in extracted:
    #             InteractionContactsFactory(interactions_fk=self.id, contacts_fk=contact.id)
    #             self.contacts.append(contact)

    #     else:
    #         # No contacts were passed in, create one
    #         contact = ContactsFactory(customer=self.customer)
    #         InteractionContactsFactory(interactions_fk=self.id, contacts_fk=contact.id)


class DealsFactory(factory.Factory):
    class Meta:
        model = Deals

    id = factory.LazyFunction(uuid.uuid4)
    deal_name = factory.Faker("catch_phrase")
    deal_type = factory.LazyFunction(
        lambda: fake.random_element(elements=("New business", "Existing Business")),
    )
    stage = factory.LazyFunction(
        lambda: fake.random_element(
            elements=("Prospecting", "Qualified", "Negotiation", "Won", "Lost"),
        ),
    )
    ammount = factory.LazyFunction(lambda: fake.random_int(min=10000, max=1000000))
    comments = factory.LazyFunction(lambda: fake.text())
    service = factory.LazyFunction(lambda: fake.random_element(services))
    service_fk = factory.SelfAttribute("service.id")
    customer = factory.SubFactory(CustomersFactory)
    customer_fk = factory.SelfAttribute("customer.id")
    contact = factory.SubFactory(ContactsFactory)
    contact_fk = factory.SelfAttribute("contact.id")


async def fill_database(session: AsyncSession) -> None:
    # Create all services
    for service in services:
        session.add(service)
    await session.commit()

    # Create 30 customers
    for _ in range(30):
        customer = CustomersFactory()
        session.add(customer)
        await session.commit()

        # Create 1 to 3 contacts for each customer
        num_contacts = randint(1, 3)
        contacts = ContactsFactory.create_batch(num_contacts, customer=customer)
        for contact in contacts:
            session.add(contact)
        await session.commit()

        # Create 1 to 5 meetings for each customer
        num_meetings = randint(1, 5)
        for _ in range(num_meetings):
            attending_contacts = fake.random_elements(
                elements=contacts,
                length=randint(1, num_contacts),
                unique=True,
            )
            interaction = InteractionsFactory(customer=customer, contacts=attending_contacts)
            session.add(interaction)
            await session.commit()  # Commit to generate the interaction ID

            # for contact in attending_contacts:
            #     interaction_contact = InteractionContactsFactory(
            #         interaction=interaction, contact=contact
            #     )
            #     session.add(interaction_contact)
            # await session.commit()  # Commit all InteractionContacts for this meeting

        num_deals = randint(1, 3)
        for _ in range(num_deals):
            deal = DealsFactory(
                customer=customer,
                contact=fake.random_element(contacts),
                service=fake.random_element(services),
            )
            session.add(deal)
        await session.commit()


async_engine = create_async_engine(config.postgres_url, echo=True)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)


async def main() -> None:
    async with AsyncSessionLocal() as session:
        await fill_database(session)


# FILL IN DB WITH RANDOM ELEMENTS
# asyncio.run(main())


# def generate_deal(
#     service: Union[Services, None] = None,
#     customer: Union[Customers, None] = None,
#     contact: Union[Contacts, None] = None,
# ) -> Deals:
#     if service is None:
#         services = import_services()
#         service = fake.random_element(services)

#     if customer is None:
#         if contact is None:
#             customer = generate_customer()
#             contact = generate_contact(customer)
#         else:
#             customer = contact.customer
#     elif contact is None:
#         contact = customer.contacts
#         if not contact:
#             contact = generate_contact(customer)

#     return Deals(
#         id=uuid.uuid4(),
#         deal_name=fake.catch_phrase(),
#         deal_type=fake.random_element(elements=("New business", "Existing Business")),
#         stage=fake.random_element(
#             elements=("Prospecting", "Qualified", "Negotiation", "Won", "Lost"),
#         ),
#         ammount=fake.random_int(min=10000, max=1000000),
#         comments=fake.text(),
#         service=service,
#         customer=customer,
#         contact=contact,
#     )


# def generate_customer() -> Customers:
#     company_name = fake.company()
#     email_username = re.sub(r"\W+", "", company_name).lower()
#     email = f"{email_username}@{email_username}.com"

#     return Customers(
#         id=uuid.uuid4(),
#         company_name=company_name,
#         industry=fake.bs(),
#         address=fake.address(),
#         email=email,
#         phone_number=fake.phone_number(),
#         lead_status=fake.random_element(
#             elements=("New", "Connected", "Proposal", "Client", "Lost"),
#         ),
#     )


# def generate_contact(customer: Union[Customers, None] = None) -> Contacts:
#     if customer is None:
#         customer = generate_customer()

#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     company_name = customer.company_name
#     email_domain = re.sub(r"\W+", "", company_name).lower()
#     email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}.com"

#     return Contacts(
#         id=uuid.uuid4(),
#         first_name=first_name,
#         last_name=last_name,
#         job_title=fake.job(),
#         email=email,
#         phone_number=fake.phone_number(),
#         comment=fake.sentence(),
#         customer=customer,
#     )


# def generate_interaction(
#     customer: Union[Customers, None] = None,
#     contacts: Union[Contacts, list[Contacts], None] = None,
#     num_interactions: int = 1,
# ) -> tuple[Union[list[Interactions], list[InteractionContacts]]]:
#     if isinstance(contacts, Contacts):
#         contacts = [contacts]

#     # if customer is none, but contacts provided, then customer is taken from contacts
#     if customer is None:
#         if contacts is None:
#             customer = generate_customer()
#             contact = generate_contact(customer)
#             contacts = [contact]
#         else:
#             customer = contacts[0].customer
#     elif contacts is None:
#         contacts = customer.contacts
#         if not contacts:
#             contact = generate_contact(customer)
#             contacts = [contact]

#     interactions = []
#     interactions_contacts_list = []

#     for _ in range(num_interactions):
#         interaction = Interactions(
#             id=uuid.uuid4(),
#             date=fake.date_between(start_date="-1y", end_date="today").strftime("%Y%m%d"),
#             type=fake.random_element(elements=("Call", "Email", "Meeting")),
#             description=fake.sentence(),
#             customer=customer,
#         )
#         # Select contacts from the customers contact list to associate with the interaction
#         interaction_contacts = [
#             InteractionContacts(interactions_fk=interaction.id, contacts_fk=contact.id)
#             for contact in contacts
#         ]

#         interactions_contacts_list.extend(interaction_contacts)
#         interactions.append(interaction)

#     return interactions, interactions_contacts_list
