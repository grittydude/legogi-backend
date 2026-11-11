import pytest

from app.core.config import settings
from app.db import session as db_session


def test_sqlite_connections_can_be_shared_across_threads(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "USE_SQLITE", True)

    assert db_session._connect_args() == {"check_same_thread": False}


def test_postgres_connections_time_out(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "USE_SQLITE", False)

    assert db_session._connect_args() == {"connect_timeout": 5}
