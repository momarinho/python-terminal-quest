## Concept: Tuples, Starred Unpacking & `set` Algebra

Tuples represent fixed-structure immutable records, while sets provide hash-backed `O(1)` membership checks and set operations (`|`, `&`, `-`, `^`).

### Starred Tuple Unpacking
```python
plant_id, genus, *tags = ("BOT-19", "Quercus", "oak", "deciduous", "native")
```
If you receive a variable-length tuple, starred unpacking (`first, *middle, last`) extracts head/tail fields cleanly.

### Order-Preserving Deduplication in `O(N)`
Converting a list to `set(items)` destroys insertion order, while `if x not in result_list` is `O(N²)`! Combine a `seen: set[str]` lookup with a `result: list[str]` output for `O(N)` order-preserving deduplication:
```python
def unique_species(records: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for item in records:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique
```

### Challenge
Implement `split_route_record`, `audit_permission_drift`, and `dedupe_preserve_order` in `rbac_audit.py`.
