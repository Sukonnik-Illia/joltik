import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

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
