## Concept: Dictionaries, Safe Lookups & Dict Comprehensions

Dictionaries map hashable keys to values in amortized `O(1)` time. Modern Python makes merging, filtering, and diffing snapshots concise and non-destructive.

### Safe Lookup & Non-Mutating Merge (`|`)
* `mapping.get(key, default)` avoids `KeyError` without mutating `mapping`.
* `base | override` (Python 3.9+) returns a **new** merged dict where `override` keys win—leaving both inputs untouched.
* Dict comprehensions `{k: v for k, v in items.items() if ...}` transform and filter cleanly in one pass.

```python
def active_pantry_items(stock: dict[str, int], min_qty: int) -> dict[str, int]:
    return {item: qty for item, qty in stock.items() if qty >= min_qty}
```

### Inverting Maps & Diffing Snapshots
* When inverting `key -> value` into `value -> key`, duplicate values silently overwrite earlier keys unless you detect collisions explicitly.
* When auditing configuration drift between two dicts (`before` vs `after`), take the union of keys (`before.keys() | after.keys()`) and compare `before.get(k)` against `after.get(k)`.

### Challenge
Implement `merge_tenant_flags`, `enabled_flags_for_env`, `invert_unique_aliases`, and `diff_flag_snapshots` in `feature_flags.py`.
