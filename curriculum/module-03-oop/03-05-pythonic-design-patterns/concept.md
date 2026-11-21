## Concept: Pythonic Design Patterns (Strategy, Factory, Repository)

In Python, patterns stay lightweight: `Protocol` replaces heavy Java-style interface hierarchies, and mapping tables or factory functions replace giant `if/elif` chains.

### Strategy + Factory + Repository
* **Strategy (`Protocol` or callable):** Encapsulates an interchangeable algorithm (e.g., document export formatters).
* **Factory:** Constructs the concrete strategy from configuration (`"markdown"` -> `MarkdownFormatter(...)`), raising `ValueError` for unknown keys.
* **Repository (`Protocol`):** Abstracts persistence (`save`, `get`) so domain services test cleanly in memory without a database.

```python
from typing import Protocol

class ExportFormatter(Protocol):
    def render(self, title: str) -> str: ...

class BookArchive(Protocol):
    def save(self, doc_id: str, body: str) -> None: ...
    def get(self, doc_id: str) -> str | None: ...
```

### Challenge
Complete `patterns.py` (`PricingStrategy`, `FlatDiscount`, `PercentDiscount`, `create_pricing_strategy`, `InvoiceRepository`, `InMemoryInvoiceRepository`) and `service.py` (`BillingService`) so discounts and persistence remain cleanly decoupled.
