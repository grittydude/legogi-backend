"""Fixtures shared by every test.

pytest finds this file by name and makes each `@pytest.fixture` here
available to any test under `app/tests/` that asks for it by parameter name.
No import needed.
"""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """An HTTP client that calls the app in-process, with no server or port.

    The `with` block also runs the app's startup and shutdown events, which
    later PRs rely on.
    """
    with TestClient(app) as c:
        yield c
