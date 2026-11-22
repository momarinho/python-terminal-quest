from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class EvalCaseResult:
    case_id: str
    passed: bool
    latency_ms: float
    input_tokens: int
    output_tokens: int


@dataclass(frozen=True)
class EvalSummary:
    total_cases: int
    passed_cases: int
    pass_rate: float
    p50_latency_ms: float
    p95_latency_ms: float
    total_cost_usd: float


def _percentile(sorted_vals: list[float], pct: float) -> float:
    idx = max(0, math.ceil((pct / 100.0) * len(sorted_vals)) - 1)
    return float(sorted_vals[idx])


def summarize_eval_run(
    results: list[EvalCaseResult],
    price_per_1k_input: float = 0.0005,
    price_per_1k_output: float = 0.0015,
) -> EvalSummary:
    """Aggregate pass rate, p50/p95 latencies (nearest-rank), and estimated USD token cost."""
    if not results:
        raise ValueError("results must not be empty")
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    latencies = sorted(r.latency_ms for r in results)
    cost = sum(
        (r.input_tokens / 1000.0) * price_per_1k_input
        + (r.output_tokens / 1000.0) * price_per_1k_output
        for r in results
    )
    return EvalSummary(
        total_cases=total,
        passed_cases=passed,
        pass_rate=round(passed / total, 4),
        p50_latency_ms=_percentile(latencies, 50.0),
        p95_latency_ms=_percentile(latencies, 95.0),
        total_cost_usd=round(cost, 6),
    )


def compute_retrieval_metrics(
    rankings: list[tuple[str, list[str]]],
    k: int = 3,
) -> dict[str, float]:
    """Compute {'recall_at_k': float, 'mrr_at_k': float} over (expected_doc_id, retrieved_doc_ids) pairs."""
    if not rankings:
        raise ValueError("rankings must not be empty")
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")

    hits = 0
    rr_total = 0.0
    for expected_id, retrieved in rankings:
        top_k = retrieved[:k]
        if expected_id in top_k:
            hits += 1
            rr_total += 1.0 / (top_k.index(expected_id) + 1)

    total = len(rankings)
    return {
        "recall_at_k": round(hits / total, 4),
        "mrr_at_k": round(rr_total / total, 4),
    }
