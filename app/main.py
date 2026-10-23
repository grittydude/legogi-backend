"""Entry point of the L'egogi API.

uvicorn imports the `app` object from this module and serves it:

    poetry run uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.core.config import settings

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
