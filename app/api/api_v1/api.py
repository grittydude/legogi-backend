"""The v1 API: every endpoint module's router, collected under one router.

`app/main.py` mounts this at `settings.API_V1_STR`, so a route declared as
`/version` here is served at `/api/v1/version`. Each new feature adds its
endpoint module here with one `include_router` line.
"""

from fastapi import APIRouter

from app.api.api_v1.endpoints import version

api_router = APIRouter()

api_router.include_router(version.router, tags=["meta"])
