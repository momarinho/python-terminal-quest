## Concept: Modular `src/` Layout, `pyproject.toml` & Circular Imports

Production Python packages use a **`src/` layout** (`src/mypkg/`) configured by a single PEP 621 `pyproject.toml` so tests always import the installed package rather than accidental local directory shadows.

### `uv` + `pyproject.toml` vs. Legacy Python Tooling
| Tooling | Role | Modern Replacement |
| :--- | :--- | :--- |
| `pip` + `requirements.txt` | Unpinned manual dependency lists | `uv add` + deterministic `uv.lock` |
| `venv` + `pyenv` | Separate Python version & venv managers | `uv` manages Python 3.13 + `.venv` in one binary |
| `Pipenv` / `Poetry` | Legacy lockfile/build managers | `uv` + `pyproject.toml` (10–100x faster resolution) |

### Breaking Circular Imports (`domain` ← `ports` ← `service`)
Circular imports happen when `domain.py` imports `service.py` while `service.py` imports `domain.py`. Fix them with **Dependency Inversion**:
1. `domain.py` defines pure models/entities with **zero** imports from `ports.py` or `service.py`.
2. `ports.py` defines `Protocol` contracts referencing `domain` types (or `if TYPE_CHECKING:` for type-only references).
3. `service.py` imports both `domain` and `ports`—never the reverse!

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ports import CatalogPort  # Only evaluated by static type checkers!

def format_catalog_entry(isbn: str, title: str) -> str:
    return f"{isbn}: {title}"
```

### Challenge
Break the circular import across `domain.py`, `ports.py`, and `service.py` so `ShipmentOrder`, `CarrierPort`, and `DispatchService` import cleanly in any order.
