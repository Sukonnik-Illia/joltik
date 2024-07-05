from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# from joltik.models.tables_faker_data import (
#     generate_contact,
#     generate_customer,
#     generate_deal,
#     generate_interaction,
#     import_services,
# )
from joltik.config import Config

config = Config()

engine = create_engine(config.postgres_url, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db() -> Generator[Session, Any, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    # with Session(engine) as session:
    #     services = import_services()
    #     customer = generate_customer()
    #     interactions, interactions_contacts_list = generate_interaction(
    #         customer=customer, contacts=contact, num_interactions=3
    #     )
    #     deal = generate_deal(customer=customer, contact=contact)

    # session.add_all(services)
    # session.add(customer)
    # session.add(contact)
    # session.commit()


# session.add(deal)
# session.commit()

# session.add_all(interactions)
# session.add_all(interactions_contacts_list)
# session.commit()

# session.add(created_customer)
# session.add_all(created_contacts)
# session.commit()
