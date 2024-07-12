import asyncio
from typing import AsyncGenerator

import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from joltik.app import app
from joltik.config import config
from joltik.db import get_async_session

# @pytest.fixture(scope="session")
# def conf():
#     config.postgres_db = "testdb"
#     return config

async_engine = create_async_engine(config.postgres_url, echo=True)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    expire_on_commit=False,
)


@pytest.fixture(scope="session", autouse=True)
def _db() -> None:
    if database_exists(config.postgres_url):
        drop_database(config.postgres_url)
    create_database(config.postgres_url)
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url=config.postgres_url) as client:
        yield client


# https://tonybaloney.github.io/posts/async-test-patterns-for-pytest-and-unittest.html

# @pytest.fixture(scope="session")
# def async_client() -> Generator[TestClient, None, None]:
#     with TestClient(app) as client:
#         yield client


@pytest.fixture(scope="session")
def event_loop(request):  # noqa: ANN201, ANN001, ARG001
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Use a function to override the dependency
def get_test_db():  # noqa: ANN201
    async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSessionLocal() as session:
            yield session

    return _get_test_db


# Override the get_db_session dependency to use the test database session
app.dependency_overrides[get_async_session] = get_test_db()


# @pytest.fixture(scope="session")
# async def transactional_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             await session.begin()
#             yield session
#         finally:
#             await session.rollback()  # Rolls back the outer transaction


# @pytest.fixture(scope="function")
# async def db_session(transactional_session):
#     yield transactional_session


# @pytest.fixture(scope="function", autouse=True)
# async def session_override(app, db_session):
#     async def get_db_session_override():
#         yield db_session[0]
