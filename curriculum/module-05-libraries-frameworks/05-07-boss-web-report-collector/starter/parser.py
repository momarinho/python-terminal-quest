from bs4 import BeautifulSoup


def parse_metrics_table(html: str) -> list[dict[str, object]]:
    """Parse table#metrics tbody tr rows into [{'region': str, 'service': str, 'latency_ms': int}]."""
    # TODO: parse with BeautifulSoup, skip incomplete/invalid rows
    _ = BeautifulSoup
    return []
