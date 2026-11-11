"""Tests for how `Settings` reads its values.

Each test builds its own `Settings(...)` instead of using the shared
`settings` object, so it controls exactly which environment variables and
`.env` file are in play. `monkeypatch` undoes every change after the test.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError
from sqlalchemy import URL

from app.core.config import Settings


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove any setting already in the shell, so tests start from defaults."""
    for name in Settings.model_fields:
        monkeypatch.delenv(name, raising=False)


def test_defaults_when_nothing_is_set() -> None:
    s = Settings(_env_file=None)

    assert s.PROJECT_NAME == "L'egogi API"
    assert s.ENVIRONMENT == "local"
    assert s.API_V1_STR == "/api/v1"


def test_environment_variable_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "staging")

    assert Settings(_env_file=None).ENVIRONMENT == "staging"


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "prod")

    with pytest.raises(ValidationError, match="ENVIRONMENT"):
        Settings(_env_file=None)


def test_env_file_is_read(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text('PROJECT_NAME="From dotenv"\n')

    assert Settings(_env_file=env_file).PROJECT_NAME == "From dotenv"


def test_environment_variable_beats_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("ENVIRONMENT=staging\n")
    monkeypatch.setenv("ENVIRONMENT", "production")

    assert Settings(_env_file=env_file).ENVIRONMENT == "production"


def test_empty_value_falls_back_to_default(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("VERSION=\n")

    assert Settings(_env_file=env_file).VERSION == "0.1.0"


def test_unknown_keys_in_env_file_are_ignored(tmp_path: Path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("POSTGRES_PASSWORD=only-for-docker\n")

    Settings(_env_file=env_file)  # must not raise


def test_database_defaults_to_a_local_sqlite_file() -> None:
    s = Settings(_env_file=None)

    assert s.USE_SQLITE is True
    assert s.database_url == "sqlite:///./legogi.db"


def test_database_url_for_postgres(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("USE_SQLITE", "false")
    monkeypatch.setenv("POSTGRES_SERVER", "db")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p@ss/word")

    url = Settings(_env_file=None).database_url

    assert isinstance(url, URL)
    assert url.drivername == "postgresql+psycopg"
    assert url.host == "db"
    assert url.port == 5432
    # Special characters are escaped, so they can't break the URL...
    assert url.render_as_string(hide_password=False).endswith(":p%40ss%2Fword@db:5432/legogi")
    # ...and printing the URL never shows the password.
    assert "p@ss" not in str(url)
    assert "***" in str(url)


def test_postgres_port_must_be_a_number(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("POSTGRES_PORT", "five-four-three-two")

    with pytest.raises(ValidationError, match="POSTGRES_PORT"):
        Settings(_env_file=None)
