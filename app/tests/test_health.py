from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_is_not_versioned(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 404
