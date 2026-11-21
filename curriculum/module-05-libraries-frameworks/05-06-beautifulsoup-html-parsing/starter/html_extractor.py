from bs4 import BeautifulSoup


def extract_service_table(html: str) -> list[dict[str, int | str]]:
    """Extract [{'service': str, 'status': str, 'latency_ms': int}] from table#status-table tbody tr."""
    # TODO: parse HTML with BeautifulSoup, select rows, clean whitespace & 'ms' suffix
    _ = BeautifulSoup
    return []


def extract_nav_links(html: str) -> list[dict[str, str]]:
    """Extract [{'label': str, 'href': str}] from all <nav> anchor tags with non-empty href."""
    # TODO: select 'nav a[href]' and normalize text + href
    return []
