"""Tests for how `Settings` reads its values.

Each test builds its own `Settings(...)` instead of using the shared
`settings` object, so it controls exactly which environment variables and
`.env` file are in play. `monkeypatch` undoes every change after the test.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

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
