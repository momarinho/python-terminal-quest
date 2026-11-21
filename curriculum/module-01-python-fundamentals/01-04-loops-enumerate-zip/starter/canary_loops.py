def pair_node_latencies(nodes: list[str], latencies_ms: list[int]) -> list[str]:
    """Pair each node with its latency as 'node:latency_ms'; raise ValueError on length mismatch."""
    # TODO: use zip(..., strict=True)
    return []


def first_degraded_stage(error_rates: list[float], threshold: float) -> int | None:
    """Return the 1-based index of the first stage strictly above threshold, else None."""
    # TODO: use enumerate(error_rates, start=1)
    return None


def simulate_backoff_attempts(
    initial_delay_ms: int,
    max_attempts: int,
    budget_ms: int,
) -> list[int]:
    """Return exponential backoff delays (doubling each attempt) fitting within remaining budget_ms."""
    # TODO: bounded while loop respecting both max_attempts and budget_ms
    return []
