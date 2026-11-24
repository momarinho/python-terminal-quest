from statistics import mean


def scale_values(values: list[float], factor: float) -> list[float]:
    """Multiply every element in values by factor."""
    return [v * factor for v in values]


def average_or_zero(values: list[float]) -> float:
    """Return arithmetic mean of values, or 0.0 if empty."""
    return float(mean(values)) if values else 0.0
