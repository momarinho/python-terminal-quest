## Concept: Reversible Schema Migrations with `alembic`

Production databases evolve without dropping tables. **Alembic** tracks revision history in `alembic_version` and applies deterministic `upgrade()` / `downgrade()` steps.

### Safe Expand-and-Backfill Pattern
1. Add the new nullable or defaulted columns (`op.add_column(...)`).
2. Run deterministic SQL backfills (`op.execute(...)`) for existing rows.
3. Add supporting indexes (`op.create_index(...)`).
4. Implement the exact reverse order in `downgrade()` (`drop_index` → `drop_column` in reverse order) so rollbacks stay clean!

```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.add_column("devices", sa.Column("channel", sa.String(32), nullable=False, server_default="stable"))
    op.execute("UPDATE devices SET channel = 'canary' WHERE serial LIKE 'dev-%'")
    op.create_index("idx_devices_channel_serial", "devices", ["channel", "serial"])

def downgrade() -> None:
    op.drop_index("idx_devices_channel_serial", table_name="devices")
    op.drop_column("devices", "channel")
```

*(In production PostgreSQL workflows, generate baseline drafts with `alembic revision --autogenerate -m "..."`, review every diff manually, and test both `upgrade` and `downgrade` in CI.)*

### Challenge
Complete `migrations/versions/0002_add_plan_and_index.py`: add `plan` (`String(32)`, `nullable=False`, `server_default="free"`) and `max_seats` (`Integer()`, `nullable=False`, `server_default="5"`) to `tenants`, backfill `'enterprise'`/`100` for `'ent-%'` and `'pro'`/`25` for `'pro-%'`, create `idx_tenants_plan_name` on `["plan", "name"]`, and reverse everything cleanly in `downgrade()`.
