"""Entry point of the L'egogi API.

uvicorn imports the `app` object from this module and serves it:

    poetry run uvicorn app.main:app --reload
"""

from fastapi import FastAPI

app = FastAPI(title="L'egogi API", version="0.1.0")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Report that the API process is up.

    Uptime monitors and the deploy script call this; it must stay cheap and
    never touch the database.
    """
    return {"status": "ok"}
