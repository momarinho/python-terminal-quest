import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # TODO: add 'plan' column (String(32), nullable=False, server_default='free'),
    # backfill 'enterprise' where name LIKE 'ent-%', and create index 'idx_tenants_plan_name' on ['plan', 'name'].
    _ = (op, sa)


def downgrade() -> None:
    # TODO: drop index 'idx_tenants_plan_name' and drop column 'plan' from 'tenants'
    pass
