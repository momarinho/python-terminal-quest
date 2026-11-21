import sqlite3


def encode_cursor(created_at: str, item_id: int) -> str:
    """Encode (created_at, item_id) into an opaque URL-safe cursor string."""
    # TODO: encode cursor
    _ = (created_at, item_id)
    return ""


def decode_cursor(cursor: str) -> tuple[str, int]:
    """Decode cursor string back into (created_at, item_id); raise ValueError if malformed."""
    # TODO: decode and validate
    raise ValueError(f"Invalid cursor: {cursor}")


def fetch_feed_page(
    conn: sqlite3.Connection,
    limit: int = 3,
    cursor: str | None = None,
) -> dict[str, object]:
    """Fetch a deterministic keyset page ordered by (created_at DESC, id DESC) using limit+1 lookahead."""
    # TODO: validate limit >= 1, decode optional cursor, query limit+1 rows, compute has_more & next_cursor
    _ = (conn, limit, cursor)
    return {"items": [], "next_cursor": None, "has_more": False}
