from contextlib import ExitStack
from typing import Generator

import pytest
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from joltik.app import app as actual_app
from joltik.config import config


@pytest.fixture(scope="session", autouse=True)
def _db() -> None:
    if database_exists(config.postgres_url):
        drop_database(config.postgres_url)
    create_database(config.postgres_url)
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(autouse=True)
def app() -> Generator[FastAPI, None, None]:
    with ExitStack():
        yield actual_app


@pytest.fixture()
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
