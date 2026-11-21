import sqlite3

import pytest
from keyset_pagination import decode_cursor, fetch_feed_page


def _seed_feed() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE feed_events (id INTEGER PRIMARY KEY, title TEXT NOT NULL, created_at TEXT NOT NULL)"
    )
    conn.executemany(
        "INSERT INTO feed_events VALUES (?, ?, ?)",
        [
            (1, "ev-1", "2026-01-01T10:00:00Z"),
            (2, "ev-2", "2026-01-02T10:00:00Z"),
            (3, "ev-3", "2026-01-02T10:00:00Z"),  # tie on created_at!
            (4, "ev-4", "2026-01-03T10:00:00Z"),
        ],
    )
    return conn


def test_keyset_pagination_tie_breaks_and_avoids_live_insert_drift() -> None:
    conn = _seed_feed()
    p1 = fetch_feed_page(conn, limit=2)
    assert [it["id"] for it in p1["items"]] == [4, 3]  # type: ignore[index]
    assert p1["has_more"] is True
    assert p1["next_cursor"] is not None

    # Live insert at top of feed must NOT duplicate id=3 on page 2!
    conn.execute("INSERT INTO feed_events VALUES (5, 'ev-5', '2026-01-04T10:00:00Z')")
    p2 = fetch_feed_page(conn, limit=2, cursor=str(p1["next_cursor"]))
    assert [it["id"] for it in p2["items"]] == [2, 1]  # type: ignore[index]
    assert p2["has_more"] is False
    assert p2["next_cursor"] is None


def test_decode_cursor_rejects_corrupt_token() -> None:
    with pytest.raises(ValueError):
        decode_cursor("not-valid-base64!!!")
