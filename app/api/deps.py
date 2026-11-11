"""Dependencies shared by endpoints: what a path operation can ask for by type.

Layer order: router -> deps -> services -> actions -> database.
"""

from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.db.session import engine


def get_session() -> Iterator[Session]:
    """Give each request its own database session, closed when it ends.

    It never commits: committing is the job of the service that does the
    work, so a request that fails halfway leaves nothing half-saved.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
