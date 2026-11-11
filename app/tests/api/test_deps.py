from sqlmodel import Session

from app.api.deps import get_session
from app.db.session import engine


def test_get_session_yields_one_session_on_the_app_engine() -> None:
    # list() runs the generator to the end, like FastAPI does after the
    # response, so the `with` block closes the session.
    sessions = list(get_session())

    assert len(sessions) == 1
    assert isinstance(sessions[0], Session)
    assert sessions[0].get_bind() is engine
