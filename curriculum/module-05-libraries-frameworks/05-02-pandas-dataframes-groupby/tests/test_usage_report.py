import pandas as pd
from usage_report import clean_and_summarize_usage


def test_clean_and_summarize_usage_drops_dirty_rows_and_aggregates() -> None:
    raw = pd.DataFrame([
        {"tenant": "  acme ", "tokens": "1200", "cost_usd": "0.12"},
        {"tenant": "acme", "tokens": 800, "cost_usd": 0.08},
        {"tenant": "beta", "tokens": "bad", "cost_usd": "0.50"},
        {"tenant": "   ", "tokens": 500, "cost_usd": 0.05},
        {"tenant": "gamma", "tokens": -10, "cost_usd": 0.01},
        {"tenant": "gamma", "tokens": 300, "cost_usd": 0.25},
    ])
    snapshot = raw.copy()
    out = clean_and_summarize_usage(raw)
    assert raw.equals(snapshot)

    assert list(out["tenant"]) == ["gamma", "acme"]
    assert list(out["total_tokens"]) == [300, 2000]
    assert list(out["total_cost_usd"]) == [0.25, 0.20]
    assert list(out["request_count"]) == [1, 2]


def test_clean_and_summarize_usage_handles_empty_or_all_invalid() -> None:
    empty = pd.DataFrame(columns=["tenant", "tokens", "cost_usd"])
    out_empty = clean_and_summarize_usage(empty)
    assert out_empty.empty
    assert list(out_empty.columns) == ["tenant", "total_tokens", "total_cost_usd", "request_count"]

    all_bad = pd.DataFrame([{"tenant": "", "tokens": "bad", "cost_usd": -1}])
    assert clean_and_summarize_usage(all_bad).empty
