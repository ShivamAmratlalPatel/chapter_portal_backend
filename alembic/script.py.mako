"""
${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Created Date: ${create_date}

"""
import sqlalchemy as sa

from alembic import op
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    ${downgrades if downgrades else "pass"}

def merge_upgrade_ops() -> None:
    """Merge upgrade operations from multiple branches."""
    ${merge_upgrade_ops if merge_upgrade_ops else "pass"}


def merge_downgrade_ops() -> None:
    """Merge downgrade operations from multiple branches."""
    ${merge_downgrade_ops if merge_downgrade_ops else "pass"}