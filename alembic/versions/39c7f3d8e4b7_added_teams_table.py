"""
Added teams table

Revision ID: 39c7f3d8e4b7
Revises: 211b8137920f
Created Date: 2023-08-27 19:41:04.642877+01:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "39c7f3d8e4b7"
down_revision = "211b8137920f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "teams",
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
        sa.Column("is_deleted", sa.Boolean(), nullable=False, default=False),
        sa.Column("last_modified_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("chapter_id", sa.UUID(), nullable=False),
        sa.Column("sport_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["chapter_id"], ["chapters.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["sport_id"], ["sports.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_teams_id"), "teams", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_teams_id"), table_name="teams")
    op.drop_table("teams")
    # ### end Alembic commands ###


def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
