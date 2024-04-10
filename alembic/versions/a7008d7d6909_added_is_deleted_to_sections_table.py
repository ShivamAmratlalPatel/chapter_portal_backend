"""
added is deleted to sections table

Revision ID: a7008d7d6909
Revises: 3a74aaac1648
Created Date: 2024-04-08 20:49:30.279234+01:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a7008d7d6909"
down_revision = "3a74aaac1648"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "section",
        sa.Column("is_deleted", sa.Boolean(), server_default="false", nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("section", "is_deleted")
    # ### end Alembic commands ###


def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
