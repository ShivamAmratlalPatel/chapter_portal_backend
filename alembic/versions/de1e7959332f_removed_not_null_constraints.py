"""
removed not null constraints

Revision ID: de1e7959332f
Revises: d559e431dbe6
Created Date: 2024-04-07 16:52:14.989719+01:00

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "de1e7959332f"
down_revision = "d559e431dbe6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("chapters", "zone", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("chapters", "email", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_constraint("chapters_email_key", "chapters", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("chapters_email_key", "chapters", ["email"])
    op.alter_column("chapters", "email", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column("chapters", "zone", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
