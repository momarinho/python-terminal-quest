## Beginner Warm-Up 2: Row Grouping Before Pandas

Pandas DataFrames automate grouping rows by category. Here is the plain-Python mental model using `defaultdict(int)`:

```python
from collections import defaultdict

def sum_by_category(rows: list[dict[str, object]]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        totals[str(row["category"])] += int(row["amount"])
    return dict(totals)
```

### Challenge
Implement `sum_by_category` and `filter_min_amount` in `warmup.py`.
