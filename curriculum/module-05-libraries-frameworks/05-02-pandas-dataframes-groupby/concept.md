## Concept: Tabular Cleaning & `groupby` Reporting with `pandas`

Real CSV exports arrive with whitespace, missing cells, and malformed numbers. Pandas handles vectorized cleaning and SQL-style `groupby` aggregations cleanly when you chain explicit transformations.

### Safe Coercion & `groupby(...).agg(...)`
```python
import pandas as pd

def summarize_crops(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df["region"] = df["region"].astype("string").str.strip()
    df["yield_kg"] = pd.to_numeric(df["yield_kg"], errors="coerce")
    clean = df.dropna(subset=["region", "yield_kg"])
    clean = clean[clean["yield_kg"] >= 0]
    return (
        clean.groupby("region", as_index=False)
        .agg(total_kg=("yield_kg", "sum"), samples=("yield_kg", "count"))
        .sort_values("total_kg", ascending=False)
        .reset_index(drop=True)
    )
```

* Always work on `raw_df.copy()` so caller DataFrames aren't mutated in place.
* `pd.to_numeric(..., errors="coerce")` turns bad strings (`"N/A"`) into `NaN` rather than crashing.

### Challenge
Implement `clean_and_summarize_usage(raw_df: pd.DataFrame) -> pd.DataFrame` in `usage_report.py` to normalize tenant names, drop invalid/negative rows, and aggregate `total_tokens`, `total_cost_usd`, and `request_count` per tenant.
