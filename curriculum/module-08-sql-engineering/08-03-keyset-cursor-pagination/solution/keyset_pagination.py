import base64
import sqlite3


def encode_cursor(created_at: str, item_id: int) -> str:
    """Encode (created_at, item_id) into an opaque URL-safe cursor string."""
    raw = f"{created_at}|{item_id}".encode()
    return base64.urlsafe_b64encode(raw).decode("ascii")


def decode_cursor(cursor: str) -> tuple[str, int]:
    """Decode cursor string back into (created_at, item_id); raise ValueError if malformed."""
    try:
        decoded = base64.urlsafe_b64decode(cursor.encode("ascii")).decode("utf-8")
        ts_part, id_part = decoded.rsplit("|", 1)
        if not ts_part:
            raise ValueError("Empty timestamp in cursor")
        return ts_part, int(id_part)
    except Exception as exc:
        raise ValueError(f"Invalid cursor: {cursor!r}") from exc


def fetch_feed_page(
    conn: sqlite3.Connection,
    limit: int = 3,
    cursor: str | None = None,
) -> dict[str, object]:
    """Fetch a deterministic keyset page ordered by (created_at DESC, id DESC) using limit+1 lookahead."""
    if limit < 1:
        raise ValueError("limit must be >= 1")

    if cursor is None:
        rows = conn.execute(
            """
            SELECT id, title, created_at
            FROM feed_events
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit + 1,),
        ).fetchall()
    else:
        cursor_ts, cursor_id = decode_cursor(cursor)
        rows = conn.execute(
            """
            SELECT id, title, created_at
            FROM feed_events
            WHERE (created_at < ?) OR (created_at = ? AND id < ?)
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (cursor_ts, cursor_ts, cursor_id, limit + 1),
        ).fetchall()

    has_more = len(rows) > limit
    page_rows = rows[:limit]
    items = [
        {"id": int(r[0]), "title": str(r[1]), "created_at": str(r[2])}
        for r in page_rows
    ]
    next_cursor = (
        encode_cursor(str(items[-1]["created_at"]), int(items[-1]["id"]))
        if has_more and items
        else None
    )
    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more,
    }
