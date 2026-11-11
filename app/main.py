"""Entry point of the L'egogi API.

uvicorn imports the `app` object from this module and serves it:

    poetry run uvicorn app.main:app --reload
"""

import logging

from fastapi import FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.api.api_v1.api import api_router
from app.api.deps import SessionDep
from app.core.config import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Report that the API process is up.

    Uptime monitors and the deploy script call this; it must stay cheap and
    never touch the database. It is deliberately outside /api/v1: it describes
    the server, not a version of the API.
    """
    return {"status": "ok"}


@app.get(
    "/ready",
    tags=["health"],
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Database unavailable"}},
)
def ready(session: SessionDep) -> dict[str, str]:
    """Report whether the API can serve real requests: is the database reachable?

    /health says the process is alive; /ready says it can do useful work. The
    deploy script waits for /ready before sending traffic to a new release.
    """
    try:
        # Raw SQL goes through the session's connection: SQLModel's
        # `session.exec` only takes `select(...)` statements built in Python.
        session.connection().execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Readiness check failed: database unavailable")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable"
        ) from None
    return {"status": "ok"}
