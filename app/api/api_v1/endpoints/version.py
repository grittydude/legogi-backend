from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/version")
def read_version() -> dict[str, str]:
    """Report which build of the API is running and where.

    The app can show this on its About screen, and it tells you which release
    a server is on after a deploy.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }
