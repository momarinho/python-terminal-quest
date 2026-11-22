from __future__ import annotations

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


def summarize_eval_run(
    results: list[EvalCaseResult],
    price_per_1k_input: float = 0.0005,
    price_per_1k_output: float = 0.0015,
) -> EvalSummary:
    """Aggregate pass rate, p50/p95 latencies (nearest-rank), and estimated USD token cost."""
    raise NotImplementedError("TODO: summarize_eval_run")


def compute_retrieval_metrics(
    rankings: list[tuple[str, list[str]]],
    k: int = 3,
) -> dict[str, float]:
    """Compute {'recall_at_k': float, 'mrr_at_k': float} over (expected_doc_id, retrieved_doc_ids) pairs."""
    raise NotImplementedError("TODO: compute_retrieval_metrics")
