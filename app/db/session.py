"""The database engine: created once per process and shared by every request.

The engine owns a pool of open connections. Each request borrows one through
a `Session` (see `app/api/deps.py`) and gives it back when the request ends.
"""

from sqlmodel import create_engine

from app.core.config import settings


def _connect_args() -> dict[str, object]:
    if settings.USE_SQLITE:
        # SQLite refuses by default to share a connection across threads,
        # and FastAPI runs plain `def` endpoints in a thread pool.
        return {"check_same_thread": False}
    # Without a timeout, connecting to a server that never answers can hang
    # for minutes instead of failing so the caller can retry or report it.
    return {"connect_timeout": 5}


engine = create_engine(
    settings.database_url,
    # Test each pooled connection before use, so one dropped by the server
    # (restart, idle timeout) is replaced instead of failing a request.
    pool_pre_ping=True,
    echo=settings.DB_ECHO,
    connect_args=_connect_args(),
)
