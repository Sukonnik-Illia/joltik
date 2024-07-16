import asyncio
from contextlib import ExitStack
from typing import AsyncGenerator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from joltik.app import app as actual_app
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


@pytest.fixture(autouse=True)
def app():  # noqa: ANN201
    with ExitStack():
        yield actual_app


@pytest.fixture()
def client(app):  # noqa: ANN201, ANN001
    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="session")
# async def async_client() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=actual_app, base_url=config.postgres_url) as client:
#         yield client


# https://tonybaloney.github.io/posts/async-test-patterns-for-pytest-and-unittest.html


@pytest.fixture(scope="session")
def event_loop(request):  # noqa: ANN201, ANN001, ARG001
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# # with GPT help
# @pytest.fixture(scope="session")
# async def async_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             # Check database connection
#             await session.execute(text("SELECT 1"))
#         except SQLAlchemyError as e:
#             pytest.fail(f"Database connection failed: {e}")
#         yield session

# # Use a function to override the dependency
# def get_test_db():
#     async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
#         async with AsyncSessionLocal() as session:
#             yield session
#     return _get_test_db

# # Override the get_db_session dependency to use the test database session
# actual_app.dependency_overrides[async_db] = get_test_db()


# https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
# Each test function is a clean slate
@pytest.fixture(scope="function", autouse=True)  # noqa: PT003
async def transactional_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction


@pytest.fixture(scope="function")  # noqa: PT003
async def db_session(transactional_session):  # noqa: ANN201, ANN001
    yield transactional_session  # noqa: PT022


@pytest.fixture(scope="function", autouse=True)  # noqa: PT003
async def _session_override(app, db_session):  # noqa: ANN202, ANN001
    async def _get_db_session_override():  # noqa: ANN202
        yield db_session[0]

    app.dependency_overrides[get_async_session] = _get_db_session_override
