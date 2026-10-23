"""Application settings, read once at startup from environment variables.

Every value has a safe local default, so the app runs with no `.env` at all.
To change one, set an environment variable with the same name, or put it in
a `.env` file in the project root (see `.env-example`):

    PROJECT_NAME="L'egogi API (local)"

Values are validated when the module is imported, so a bad value stops the
app at startup instead of failing on the first request that uses it.
"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        # `FOO=` in .env means "use the default", not "use an empty string".
        env_ignore_empty=True,
        # Unknown variables in .env are ignored, so one .env can also hold
        # values for Docker Compose and other tools.
        extra="ignore",
    )

    PROJECT_NAME: str = "L'egogi API"
    # The deploy workflow will set this to the release tag or commit SHA.
    VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    # Every versioned endpoint lives under this prefix. A breaking change to
    # the API gets a new prefix (/api/v2) so older app versions keep working.
    API_V1_STR: str = "/api/v1"


settings = Settings()
