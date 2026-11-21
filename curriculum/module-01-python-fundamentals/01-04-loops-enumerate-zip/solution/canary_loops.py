def pair_node_latencies(nodes: list[str], latencies_ms: list[int]) -> list[str]:
    """Pair each node with its latency as 'node:latency_ms'; raise ValueError on length mismatch."""
    return [f"{node}:{ms}ms" for node, ms in zip(nodes, latencies_ms, strict=True)]


def first_degraded_stage(error_rates: list[float], threshold: float) -> int | None:
    """Return the 1-based index of the first stage strictly above threshold, else None."""
    for stage_idx, rate in enumerate(error_rates, start=1):
        if rate > threshold:
            return stage_idx
    return None


def simulate_backoff_attempts(
    initial_delay_ms: int,
    max_attempts: int,
    budget_ms: int,
) -> list[int]:
    """Return exponential backoff delays (doubling each attempt) fitting within remaining budget_ms."""
    if initial_delay_ms <= 0 or max_attempts <= 0 or budget_ms <= 0:
        return []

    delays: list[int] = []
    remaining = budget_ms
    delay = initial_delay_ms
    while len(delays) < max_attempts and delay <= remaining:
        delays.append(delay)
        remaining -= delay
        delay *= 2
    return delays
