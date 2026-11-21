import sqlite3

from index_tuning import (
    create_audit_index,
    explain_alerts_plan,
    fetch_recent_alerts,
)


def _setup_events() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE audit_events (
            id INTEGER PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    rows = [
        (i, f"t-{i % 3}", "ERROR" if i % 2 == 0 else "INFO", f"msg-{i}", f"2026-01-{10 + (i % 15):02d}T10:00:00Z")
        for i in range(1, 40)
    ]
    conn.executemany("INSERT INTO audit_events VALUES (?, ?, ?, ?, ?)", rows)
    return conn


def test_composite_index_eliminates_scan_in_explain_plan() -> None:
    conn = _setup_events()
    create_audit_index(conn)
    plan = explain_alerts_plan(conn, "t-0", "ERROR", 5)
    joined = " | ".join(plan).upper()
    assert "SEARCH AUDIT_EVENTS USING INDEX" in joined
    assert "SCAN AUDIT_EVENTS" not in joined


def test_fetch_recent_alerts_returns_ordered_subset() -> None:
    conn = _setup_events()
    create_audit_index(conn)
    alerts = fetch_recent_alerts(conn, "t-0", "ERROR", 2)
    assert len(alerts) == 2
    assert alerts[0][2] >= alerts[1][2]
