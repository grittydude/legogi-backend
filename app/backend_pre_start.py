"""Wait until the database accepts connections.

prestart.sh runs this before the server starts. In Docker Compose and on the
server, the API container can start before Postgres is ready; without this
wait, the first requests (or PR 8's migrations) would fail.

    python -m app.backend_pre_start
"""

import logging
import time

from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import engine

logger = logging.getLogger(__name__)


def wait_for_database(engine: Engine, attempts: int = 60, delay_seconds: float = 1.0) -> None:
    """Try `SELECT 1` until it works, up to `attempts` times.

    Raises the last error if the database never answers, so the container
    exits with an error instead of starting a server that can't work.
    """
    for attempt in range(1, attempts + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except SQLAlchemyError as error:
            if attempt == attempts:
                logger.error("Database still unavailable after %d attempts", attempts)
                raise
            logger.warning("Database not ready (attempt %d/%d): %s", attempt, attempts, error)
            time.sleep(delay_seconds)
        else:
            logger.info("Database is ready (attempt %d)", attempt)
            return


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    wait_for_database(engine)


if __name__ == "__main__":
    main()
