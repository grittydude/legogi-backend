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
from sqlalchemy import URL


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

    # --- Database -------------------------------------------------------------
    # Local development uses a SQLite file, so no database server is needed.
    # Docker Compose, CI and production set USE_SQLITE=false to use Postgres.
    USE_SQLITE: bool = True
    SQLITE_DATABASE_URI: str = "sqlite:///./legogi.db"

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "legogi"
    POSTGRES_PASSWORD: str = "legogi"
    POSTGRES_DB: str = "legogi"

    # Logs every SQL statement. Handy while debugging, noisy otherwise.
    DB_ECHO: bool = False

    @property
    def database_url(self) -> str | URL:
        """Where SQLAlchemy connects, built from the fields above.

        For Postgres this is a `URL` object rather than a string: it escapes
        special characters in the password, and printing it shows `***`
        instead of the password.
        """
        if self.USE_SQLITE:
            return self.SQLITE_DATABASE_URI
        return URL.create(
            "postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings()
