from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from joltik.config import Config

config = Config()

sync_engine = create_engine(config.postgres_url, echo=True)
async_engine = create_async_engine(config.postgres_url, echo=True)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
    expire_on_commit=False,
)


# Dependency
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


DBAsyncSession = Annotated[AsyncSession, Depends(get_async_session)]

# user_roles = [{"user_role": "Mortal"}, {"user_role": "Admin"}]


# def import_roles(user_roles: list[dict]) -> None:
#     return [Role(**role_dict) for role_dict in user_roles]


# roles = import_roles(user_roles)

# with Session(engine) as session:
#     session.add_all(roles)
#     session.commit()

# with Session(sync_engine) as session:
#     role = session.query(Role).all()
#     print(role)
#     print(session.query(Role).delete())
#     session.commit()

# services = import_services()
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
