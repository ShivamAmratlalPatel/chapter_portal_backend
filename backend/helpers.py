"""Helper functions."""
from sqlalchemy.orm import Session

from backend import database


def get_db() -> Session:  # pragma: no cover
    """
    Get a database session.

    Returns
        Session: database session

    """
    db = None
    try:
        db = database.session_local_factory()()
        yield db
    finally:
        if db:
            db.close()
