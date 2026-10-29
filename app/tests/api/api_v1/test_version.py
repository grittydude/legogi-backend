from fastapi.testclient import TestClient

from app.core.config import settings


def test_version_reports_current_settings(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/version")

    assert response.status_code == 200
    # Compare with `settings`, not literals: a developer's .env may change
    # these values, and the test should still pass.
    assert response.json() == {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


def test_openapi_is_served_under_api_v1(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    assert f"{settings.API_V1_STR}/version" in paths
    assert "/health" in paths


def test_openapi_is_not_served_at_root(client: TestClient) -> None:
    assert client.get("/openapi.json").status_code == 404
