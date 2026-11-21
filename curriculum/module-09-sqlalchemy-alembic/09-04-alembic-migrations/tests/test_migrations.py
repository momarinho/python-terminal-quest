from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text


def _alembic_cfg(db_path: Path) -> Config:
    migrations_dir = Path(__file__).resolve().parents[1] / "migrations"
    cfg = Config()
    cfg.set_main_option("script_location", str(migrations_dir))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    return cfg


def test_alembic_upgrade_backfills_and_creates_index(tmp_path: Path) -> None:
    db_path = tmp_path / "app.db"
    cfg = _alembic_cfg(db_path)

    command.upgrade(cfg, "0001")
    engine = create_engine(f"sqlite:///{db_path}")
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO tenants (id, name) VALUES (1, 'ent-acme'), (2, 'indie-dev')"))

    command.upgrade(cfg, "head")
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, plan FROM tenants ORDER BY id")).fetchall()
        assert rows == [(1, "enterprise"), (2, "free")]
        indexes = {idx["name"] for idx in inspect(conn).get_indexes("tenants")}
        assert "idx_tenants_plan_name" in indexes


def test_alembic_downgrade_reverses_column_and_index(tmp_path: Path) -> None:
    db_path = tmp_path / "down.db"
    cfg = _alembic_cfg(db_path)

    command.upgrade(cfg, "head")
    command.downgrade(cfg, "0001")

    engine = create_engine(f"sqlite:///{db_path}")
    with engine.connect() as conn:
        cols = {col["name"] for col in inspect(conn).get_columns("tenants")}
        indexes = {idx["name"] for idx in inspect(conn).get_indexes("tenants")}
        assert cols == {"id", "name"}
        assert "idx_tenants_plan_name" not in indexes
