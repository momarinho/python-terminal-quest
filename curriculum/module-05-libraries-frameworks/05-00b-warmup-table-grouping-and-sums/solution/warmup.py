from collections import defaultdict


def sum_by_category(rows: list[dict[str, object]]) -> dict[str, int]:
    """Sum `amount` per `category` across row dictionaries."""
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        totals[str(row["category"])] += int(row["amount"])  # type: ignore[arg-type]
    return dict(totals)


def filter_min_amount(rows: list[dict[str, int | str]], min_amount: int) -> list[dict[str, int | str]]:
    """Return rows whose `amount` is >= min_amount."""
    return [row for row in rows if int(row["amount"]) >= min_amount]
