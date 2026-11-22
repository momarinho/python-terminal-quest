import sqlite3

_QUERY = """
SELECT id, message, created_at
FROM audit_events
WHERE tenant_id = ? AND severity = ?
ORDER BY created_at DESC
LIMIT ?
"""


def create_audit_index(conn: sqlite3.Connection) -> None:
    """Create the optimal composite index on `audit_events` for tenant/severity/created_at queries."""
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_audit_tenant_sev_ts
        ON audit_events (tenant_id, severity, created_at DESC)
        """
    )


def fetch_recent_alerts(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[tuple[int, str, str]]:
    """Return [(id, message, created_at)] filtered by tenant_id + severity, newest created_at first."""
    rows = conn.execute(_QUERY, (tenant_id, severity, limit)).fetchall()
    return [(int(r[0]), str(r[1]), str(r[2])) for r in rows]


def explain_alerts_plan(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> list[str]:
    """Return EXPLAIN QUERY PLAN detail lines (column index 3) for the recent-alerts query."""
    rows = conn.execute(f"EXPLAIN QUERY PLAN {_QUERY}", (tenant_id, severity, limit)).fetchall()
    return [str(row[3]) for row in rows]


def audit_index_health(
    conn: sqlite3.Connection,
    tenant_id: str,
    severity: str,
    limit: int = 10,
) -> dict[str, object]:
    """Return {'uses_index': bool, 'has_full_scan': bool, 'plan': list[str]} from EXPLAIN QUERY PLAN."""
    plan = explain_alerts_plan(conn, tenant_id, severity, limit)
    joined = " | ".join(plan).upper()
    return {
        "uses_index": "USING INDEX" in joined,
        "has_full_scan": "SCAN " in joined,
        "plan": plan,
    }
