"""Alembic configuration file."""
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from backend.actions.actions_models import Action  # noqa: F401
from backend.allocations.allocation_models import Allocation  # noqa: F401
from backend.chapters.chapters_models import Chapter  # noqa: F401
from backend.committees.committee_models import CommitteeMember  # noqa: F401
from backend.database import Base
from backend.events.event_models import (  # noqa: F401
    ChapterEventAssociation,
    Event,
    EventType,
)
from backend.health.health_models import (  # noqa: F401
    ChapterHealth,
    HealthQuestion,
    Section,
)
from backend.inventory.inventory_models import (  # noqa: F401
    Category,
    InventoryItem,
    Location,
)
from backend.meetings.meetings_models import (  # noqa: F401
    MatrixMeeting,
    SectionMeeting,
    ZonalTeamMeeting,
)
from backend.membership.membership_models import MembershipLog  # noqa: F401
from backend.updates.updates_models import ChapterUpdate, SectionUpdate  # noqa: F401
from backend.users.users_models import User, UserType  # noqa: F401
from backend.visits.visits_models import (  # noqa: F401
    ChapterVisitAssociation,
    Visit,
    VisitCategory,
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

if "DATABASE_URL" in os.environ:
    config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import my_model
# target_metadata = my_model.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:  # pragma: no cover
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():  # pragma: no cover
    run_migrations_offline()
else:
    run_migrations_online()
