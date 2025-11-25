import os
from collections.abc import Generator
from unittest.mock import Mock, patch

import pytest
from pytest import FixtureRequest
from sqlalchemy.engine import Connection, Engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

import databases
from databases import SessionFactory
from jabberwocky.shared.infrastructure.fake_flag_client import FakeFlagClient
from jabberwocky.shared.infrastructure.unleash_flag_client import UnleashFlagClient


@pytest.fixture(autouse=True)
def flag_client() -> Generator[FakeFlagClient]:
    client = FakeFlagClient()
    with patch.object(UnleashFlagClient, "__new__") as mock:
        mock.return_value = client
        yield client


@pytest.fixture(scope="session")
def connection() -> Generator[Connection]:
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql+psycopg://{os.environ['PG_USER']}:"
        f"{os.environ['PG_PASSWORD']}@"
        f"{os.environ['PG_HOST']}/"
        f"{os.environ['PG_DB']}_test"
    )

    engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="REPEATABLE READ")
    if not database_exists(engine.url):
        create_database(engine.url)

    with patch.object(SessionFactory, "create") as mock:
        mock.side_effect = lambda: sessionmaker(autocommit=False, autoflush=True, bind=engine)()
        yield engine.connect()


@pytest.fixture
def _setup_test_database(connection: Connection) -> Generator[None]:
    databases.Base.metadata.bind = connection
    databases.Base.metadata.create_all(connection.engine)

    yield

    databases.Base.metadata.drop_all(connection.engine)


class NotMarkedAsIntegrationTest(Exception):
    pass


@pytest.fixture(autouse=True)
def _integration_test_db_helper(request: FixtureRequest) -> Generator[Mock | None]:
    for marker in request.node.iter_markers():
        if marker.name == "integration":
            request.getfixturevalue("_setup_test_database")
            yield None
            return

    with patch.object(Engine, "connect") as mock_connect:
        mock_connect.side_effect = NotMarkedAsIntegrationTest
        yield mock_connect
