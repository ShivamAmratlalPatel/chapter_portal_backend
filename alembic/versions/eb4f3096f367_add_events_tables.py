"""
add events tables

Revision ID: eb4f3096f367
Revises: db47fbe8d33e
Created Date: 2024-04-04 09:54:52.290631+01:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "eb4f3096f367"
down_revision = "db47fbe8d33e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "event_types",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(timezone=True),
            server_default=sa.text(
                "timezone('Europe/London', timezone('Europe/London', CURRENT_TIMESTAMP))",
            ),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_event_types_id"), "event_types", ["id"], unique=False)
    op.create_table(
        "events",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("event_type_id", sa.UUID(), nullable=False),
        sa.Column(
            "created_date",
            sa.DateTime(timezone=True),
            server_default=sa.text(
                "timezone('Europe/London', timezone('Europe/London', CURRENT_TIMESTAMP))",
            ),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("last_modified_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["event_type_id"],
            ["event_types.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_events_id"), "events", ["id"], unique=False)
    op.create_table(
        "chapter_event_association",
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("event_id", sa.UUID(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chapter_id"],
            ["chapters.id"],
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_chapter_event_association_id"),
        "chapter_event_association",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_chapter_event_association_id"),
        table_name="chapter_event_association",
    )
    op.drop_table("chapter_event_association")
    op.drop_index(op.f("ix_events_id"), table_name="events")
    op.drop_table("events")
    op.drop_index(op.f("ix_event_types_id"), table_name="event_types")
    op.drop_table("event_types")
    # ### end Alembic commands ###


def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
