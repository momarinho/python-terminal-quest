from bs4 import BeautifulSoup


def extract_service_table(html: str) -> list[dict[str, int | str]]:
    """Extract [{'service': str, 'status': str, 'latency_ms': int}] from table#status-table tbody tr."""
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, int | str]] = []
    for tr in soup.select("table#status-table tbody tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td")]
        if len(cells) < 3:
            continue
        service, status, raw_latency = cells[0], cells[1], cells[2]
        latency_ms = int(raw_latency.removesuffix("ms").strip())
        rows.append(
            {
                "service": service,
                "status": status.upper(),
                "latency_ms": latency_ms,
            }
        )
    return rows


def extract_nav_links(html: str) -> list[dict[str, str]]:
    """Extract [{'label': str, 'href': str}] from all <nav> anchor tags with non-empty href."""
    soup = BeautifulSoup(html, "html.parser")
    links: list[dict[str, str]] = []
    for anchor in soup.select("nav a[href]"):
        href = str(anchor.get("href", "")).strip()
        if not href:
            continue
        links.append(
            {
                "label": anchor.get_text(" ", strip=True),
                "href": href,
            }
        )
    return links
