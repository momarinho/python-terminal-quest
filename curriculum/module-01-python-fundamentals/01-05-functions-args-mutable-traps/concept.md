## Concept: Python Function Parameters & The Mutable Default Trap

In Python, default parameter values are evaluated **once at function definition time (`def`)**, not on every call!

### The Classic Bug
```python
# BUG: every call without `labels` shares and mutates the SAME list!
def tag_artifact(name: str, labels: list[str] = []) -> list[str]:
    labels.append(name)
    return labels
```

**Fix:** Default to `None` and create a fresh list inside the body:
```python
def tag_artifact(name: str, labels: list[str] | None = None) -> list[str]:
    result = list(labels) if labels is not None else []
    result.append(name)
    return result
```

### `*args`, Keyword-Only (`*`), and `**kwargs`
* `*args` collects extra positional arguments into a `tuple`.
* A bare `*` forces all parameters after it to be passed **by keyword only** (preventing accidental positional swaps).
* `**kwargs` collects extra keyword arguments into a `dict`.

### Challenge
Fix the mutable default bug in `append_audit_tag` and implement `build_metric_event` with `*labels`, keyword-only `severity: str = "info"`, and `**attrs: str` in `audit_tags.py`.
