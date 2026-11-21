## Concept: Structured HTML Extraction with Beautiful Soup (`bs4`)

HTML pages rarely match brittle string splits or regexes. `BeautifulSoup(html, "html.parser")` builds a navigable DOM tree supporting CSS selectors (`.select()`, `.select_one()`) and clean text extraction.

### CSS Selectors & Text Normalization
```python
from bs4 import BeautifulSoup

def extract_book_rows(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    rows: list[dict[str, str]] = []
    for tr in soup.select("table#catalog tbody tr"):
        cells = [td.get_text(" ", strip=True) for td in tr.select("td")]
        if len(cells) >= 2:
            rows.append({"isbn": cells[0], "title": cells[1]})
    return rows
```

* Use `tag.get_text(" ", strip=True)` to collapse nested `<span>` whitespace cleanly.
* Guard `soup.select_one(...)` for `None` before reading `.get("href")` or `.get_text()`.

### Challenge
Implement `extract_service_table(html)` and `extract_nav_links(html)` in `html_extractor.py`.
