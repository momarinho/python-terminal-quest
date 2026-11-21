import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "tenants",
        sa.Column("plan", sa.String(length=32), nullable=False, server_default="free"),
    )
    op.execute("UPDATE tenants SET plan = 'enterprise' WHERE name LIKE 'ent-%'")
    op.create_index("idx_tenants_plan_name", "tenants", ["plan", "name"])


def downgrade() -> None:
    op.drop_index("idx_tenants_plan_name", table_name="tenants")
    op.drop_column("tenants", "plan")
