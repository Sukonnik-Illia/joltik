from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from joltik.app import app
from joltik.config import config

# @pytest.fixture(scope="session")
# def conf():
#     config.postgres_db = "testdb"
#     return config


@pytest.fixture(scope="session", autouse=True)
def _db() -> None:
    if database_exists(config.postgres_url):
        drop_database(config.postgres_url)
    create_database(config.postgres_url)
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    # Union in typing used for compatibility with different IDEs
    with TestClient(app) as client:
        yield client
