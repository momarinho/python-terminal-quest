import pandas as pd


def clean_and_summarize_usage(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean dirty LLM usage rows and aggregate per tenant ordered by total_cost_usd desc, tenant asc."""
    if raw_df.empty:
        return pd.DataFrame(columns=["tenant", "total_tokens", "total_cost_usd", "request_count"])

    df = raw_df.copy()
    df["tenant"] = df["tenant"].fillna("").astype(str).str.strip()
    df = df[df["tenant"] != ""]
    df["tokens"] = pd.to_numeric(df["tokens"], errors="coerce")
    df["cost_usd"] = pd.to_numeric(df["cost_usd"], errors="coerce")
    df = df.dropna(subset=["tokens", "cost_usd"])
    df = df[(df["tokens"] >= 0) & (df["cost_usd"] >= 0)]

    if df.empty:
        return pd.DataFrame(columns=["tenant", "total_tokens", "total_cost_usd", "request_count"])

    summary = (
        df.groupby("tenant", as_index=False)
        .agg(
            total_tokens=("tokens", "sum"),
            total_cost_usd=("cost_usd", "sum"),
            request_count=("tokens", "count"),
        )
        .sort_values(by=["total_cost_usd", "tenant"], ascending=[False, True])
        .reset_index(drop=True)
    )
    summary["total_tokens"] = summary["total_tokens"].astype(int)
    summary["total_cost_usd"] = summary["total_cost_usd"].round(4)
    summary["request_count"] = summary["request_count"].astype(int)
    return summary
