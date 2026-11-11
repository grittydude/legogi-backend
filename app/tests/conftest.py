"""Fixtures shared by every test.

pytest finds this file by name and makes each `@pytest.fixture` here
available to any test under `app/tests/` that asks for it by parameter name.
No import needed.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from app.api.deps import get_session
from app.main import app


@pytest.fixture
def engine() -> Iterator[Engine]:
    """A fresh in-memory SQLite database for each test.

    Nothing touches your local `legogi.db`, and no test sees another test's
    data. StaticPool keeps the single in-memory connection alive, because
    each new connection to `sqlite://` would be a new, empty database.
    """
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as s:
        yield s


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """An HTTP client that calls the app in-process, with no server or port.

    Every endpoint that asks for `get_session` gets the test session instead
    of one from the real engine. The `with` block also runs the app's startup
    and shutdown events.
    """

    def get_test_session() -> Session:
        return session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
