import sqlite3


def create_audit_index(conn: sqlite3.Connection) -> None:
    """Create the optimal composite index on `audit_events` for tenant/severity/created_at queries."""
    # TODO: CREATE INDEX IF NOT EXISTS ... ON audit_events (...)
    _ = conn


def fetch_recent_alerts(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[tuple[int, str, str]]:
    """Return [(id, message, created_at)] filtered by tenant_id + severity, newest created_at first."""
    # TODO: parameterized SELECT ... WHERE tenant_id = ? AND severity = ? ORDER BY created_at DESC LIMIT ?
    _ = (tenant_id, severity, limit)
    return []


def explain_alerts_plan(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[str]:
    """Return EXPLAIN QUERY PLAN detail lines for the recent-alerts query."""
    # TODO: run EXPLAIN QUERY PLAN on the exact SELECT and return detail column strings (index 3)
    return []
