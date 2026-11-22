import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add plan & max_seats columns, backfill enterprise/pro rows, and create idx_tenants_plan_name."""
    op.add_column(
        "tenants",
        sa.Column("plan", sa.String(length=32), nullable=False, server_default="free"),
    )
    op.add_column(
        "tenants",
        sa.Column("max_seats", sa.Integer(), nullable=False, server_default="5"),
    )
    op.execute("UPDATE tenants SET plan = 'enterprise', max_seats = 100 WHERE name LIKE 'ent-%'")
    op.execute("UPDATE tenants SET plan = 'pro', max_seats = 25 WHERE name LIKE 'pro-%'")
    op.create_index("idx_tenants_plan_name", "tenants", ["plan", "name"])


def downgrade() -> None:
    """Drop idx_tenants_plan_name, max_seats, and plan in reverse order."""
    op.drop_index("idx_tenants_plan_name", table_name="tenants")
    op.drop_column("tenants", "max_seats")
    op.drop_column("tenants", "plan")
