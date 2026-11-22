import sqlite3


def create_audit_index(conn: sqlite3.Connection) -> None:
    """Create the optimal composite index on `audit_events` for tenant/severity/created_at queries."""
    _ = conn


def fetch_recent_alerts(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[tuple[int, str, str]]:
    """Return [(id, message, created_at)] filtered by tenant_id + severity, newest created_at first."""
    _ = (tenant_id, severity, limit)
    return []


def explain_alerts_plan(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[str]:
    """Return EXPLAIN QUERY PLAN detail lines (column index 3) for the recent-alerts query."""
    return []


def audit_index_health(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> dict[str, object]:
    """Return {'uses_index': bool, 'has_full_scan': bool, 'plan': list[str]} from EXPLAIN QUERY PLAN."""
    return {}
