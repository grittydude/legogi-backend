import logging
from collections.abc import Callable

import pytest
from sqlalchemy import Connection, Engine
from sqlalchemy.exc import OperationalError

from app import backend_pre_start
from app.backend_pre_start import wait_for_database
from app.db.session import engine as app_engine


def fail_first(engine: Engine, failures: int) -> Callable[[], Connection]:
    """Make `engine.connect()` fail `failures` times, then work normally."""
    real_connect = engine.connect
    calls = {"count": 0}

    def connect() -> Connection:
        calls["count"] += 1
        if calls["count"] <= failures:
            raise OperationalError("SELECT 1", {}, Exception("server not ready"))
        return real_connect()

    return connect


def test_returns_at_once_when_database_is_up(engine: Engine) -> None:
    wait_for_database(engine, attempts=3, delay_seconds=0)  # must not raise


def test_retries_until_database_is_up(
    engine: Engine, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.INFO)
    monkeypatch.setattr(engine, "connect", fail_first(engine, failures=2))

    wait_for_database(engine, attempts=5, delay_seconds=0)

    assert "attempt 1/5" in caplog.text
    assert "attempt 2/5" in caplog.text
    assert "Database is ready (attempt 3)" in caplog.text


def test_gives_up_after_the_last_attempt(engine: Engine, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(engine, "connect", fail_first(engine, failures=10))

    with pytest.raises(OperationalError):
        wait_for_database(engine, attempts=3, delay_seconds=0)


def test_main_waits_for_the_app_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    called_with: list[Engine] = []
    monkeypatch.setattr(backend_pre_start, "wait_for_database", called_with.append)

    backend_pre_start.main()

    assert called_with == [app_engine]
