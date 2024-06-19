from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from joltik.config import Config
from joltik.models.tables_faker_data import (
    generate_contact,
    generate_customer,
    generate_deal,
    import_services,
)

config = Config()

engine = create_engine(str(config.postgres_url), echo=True)

with Session(engine) as session:
    services = import_services()
    customer = generate_customer()
    contact = generate_contact(customer)
    deal = generate_deal(customer=customer, contact=contact)

    session.add_all(services)
    # session.add(customer)
    # session.add(contact)
    session.commit()

    # session.add(deal)
    # session.commit()

    # session.add(created_customer)
    # session.add_all(created_contacts)
    # session.commit()

    # session.add_all(interactions)
    # session.add_all(interactions_contacts_list)
    # session.commit()
