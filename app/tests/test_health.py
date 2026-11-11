from pathlib import Path

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from app.api.deps import get_session
from app.main import app


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_is_not_versioned(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 404


def test_ready_when_database_answers(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_is_503_when_database_is_unreachable(client: TestClient, tmp_path: Path) -> None:
    # SQLite can't create a file inside a folder that doesn't exist, so every
    # query on this engine fails, like a stopped database server.
    broken_engine = create_engine(f"sqlite:///{tmp_path / 'missing' / 'app.db'}")

    def get_broken_session() -> Session:
        return Session(broken_engine)

    app.dependency_overrides[get_session] = get_broken_session

    response = client.get("/ready")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}


def test_health_does_not_need_the_database(client: TestClient, tmp_path: Path) -> None:
    broken_engine = create_engine(f"sqlite:///{tmp_path / 'missing' / 'app.db'}")
    app.dependency_overrides[get_session] = lambda: Session(broken_engine)

    assert client.get("/health").status_code == 200
