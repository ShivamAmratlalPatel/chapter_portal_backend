"""
added icon to sections tables

Revision ID: 2e6e034a2f54
Revises: 2858c0da24a5
Created Date: 2024-06-04 23:02:07.091061+01:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "2e6e034a2f54"
down_revision = "2858c0da24a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("section", sa.Column("icon", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("section", "icon")
    # ### end Alembic commands ###


def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
