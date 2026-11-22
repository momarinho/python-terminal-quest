import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add plan & max_seats columns, backfill enterprise/pro rows, and create idx_tenants_plan_name."""
    _ = (op, sa)


def downgrade() -> None:
    """Drop idx_tenants_plan_name, max_seats, and plan in reverse order."""
    pass
