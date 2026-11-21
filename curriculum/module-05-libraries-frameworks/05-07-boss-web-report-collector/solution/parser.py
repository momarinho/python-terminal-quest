from bs4 import BeautifulSoup


def parse_metrics_table(html: str) -> list[dict[str, object]]:
    """Parse table#metrics tbody tr rows into [{'region': str, 'service': str, 'latency_ms': int}]."""
    soup = BeautifulSoup(html, "html.parser")
    records: list[dict[str, object]] = []
    for tr in soup.select("table#metrics tbody tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td")]
        if len(cells) < 3:
            continue
        region, service, raw_ms = cells[0], cells[1], cells[2]
        if not region or not service:
            continue
        try:
            latency_ms = int(raw_ms.removesuffix("ms").strip())
        except ValueError:
            continue
        records.append({"region": region, "service": service, "latency_ms": latency_ms})
    return records
