## Concept: Operators & Exact `Decimal` Precision

Python gives you both true division (`/`) and floor division (`//`), plus exact base-10 arithmetic via the standard library `decimal` module.

### Why Binary `float` Fails Monetary & Ratio Math
Standard `float` values use IEEE-754 binary representations, so `0.1 + 0.2 == 0.30000000000000004`. Worse, constructing `Decimal(0.1)` passes that binary approximation directly into `Decimal`! Always construct `Decimal` from a **`str`** (or `int`).

```python
from decimal import Decimal, ROUND_HALF_UP

def compute_reagent_dose(
    grams_per_liter: str,
    liters: int,
    purity_pct: str,
) -> Decimal:
    base = Decimal(grams_per_liter) * Decimal(liters)
    purity_factor = Decimal(purity_pct) / Decimal("100")
    raw_dose = base * purity_factor
    return raw_dose.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

### Key Guardrails
* Never mix `float` and `Decimal` in `+`, `-`, `*`, `/` (raises `TypeError`).
* `.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` rounds predictably to 2 decimal places instead of Python's default banker's rounding (`ROUND_HALF_EVEN`).

### Challenge
Implement `compute_invoice_total` and `split_installments` in `invoice_math.py` using `Decimal` constructed from strings/ints and `ROUND_HALF_UP` rounding.
