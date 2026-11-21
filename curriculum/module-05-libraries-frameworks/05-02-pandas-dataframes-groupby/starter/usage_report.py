import pandas as pd


def clean_and_summarize_usage(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Clean dirty LLM usage rows and aggregate per tenant ordered by total_cost_usd desc, tenant asc."""
    # TODO: copy df, strip tenant, coerce tokens/cost_usd, drop NA/negatives, groupby tenant
    _ = pd
    return pd.DataFrame(columns=["tenant", "total_tokens", "total_cost_usd", "request_count"])
