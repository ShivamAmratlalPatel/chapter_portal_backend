"""Database fixtures for testing."""
import os
import sys

import pytest
from sqlalchemy import MetaData, text

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from backend.database import session_local_factory


@pytest.fixture(scope="session")
def session_factory() -> session_local_factory:
    """Create a session factory for a local database."""
    # Migrate the database if it's not up to date.
    database_url = os.environ["DATABASE_URL"]
    if database_url != "postgresql://chapter@chapter-db/chapter_backend":  # pragma: no cover
        sys.exit(1)
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    alembic_upgrade(alembic_config, "head")

    return session_local_factory(database_url)


@pytest.fixture()
def session(session_factory: session_local_factory) -> session_local_factory:
    """Create a session for a local database."""
    sess = session_factory()
    engine = session_factory.kw["bind"]
    meta = MetaData()
    meta.reflect(bind=engine)
    conn = engine.connect()
    transaction = conn.begin()
    for table in meta.sorted_tables:
        if table.name in [
            "alembic_version",
            "stages",
        ]:
            continue
        conn.execute(text(f"TRUNCATE {table.name} CASCADE"))
    transaction.commit()

    try:
        yield sess
    finally:
        sess.close()
