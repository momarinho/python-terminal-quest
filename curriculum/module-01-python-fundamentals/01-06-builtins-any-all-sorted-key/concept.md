## Concept: Declarative Built-ins (`any`, `all`, `sorted`, `min`/`max` with `key`)

Python's built-in functions replace verbose imperative loops with readable, short-circuiting expressions.

### Short-Circuit Predicates
* `all(pred(x) for x in items)` stops at the first `False` (note: `all([])` is `True`, so guard empty collections explicitly when required!).
* `any(pred(x) for x in items)` stops at the first `True`.

### Key-Based Ranking (`sorted`, `min`, `max`)
* `sorted(items, key=..., reverse=...)` returns a **new** list (never mutates `items` in place like `.sort()`).
* Returning a tuple from `key` breaks ties deterministically—and you can negate numbers (`-score`) to mix descending primary with ascending tie-breaking!

```python
def top_audition(candidates: list[dict[str, object]]) -> str:
    winner = max(
        candidates,
        key=lambda c: (int(c["score"]), -int(c["mistakes"])),
    )
    return str(winner["name"])
```

### Challenge
Implement `is_release_ready`, `has_blocking_alert`, `rank_endpoints`, and `fastest_healthy_region` in `deploy_gates.py`.
