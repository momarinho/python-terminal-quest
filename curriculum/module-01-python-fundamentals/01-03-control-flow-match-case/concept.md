## Concept: Control Flow, Truthiness & Structural `match`/`case`

In Python, `None`, `0`, `0.0`, `""`, `[]`, and `{}` are all **falsy**—which means `if retries:` skips `retries = 0` just as if it were `None`! Whenever `0` is a valid numeric value, check `is None` / `is not None` explicitly.

### Structural Pattern Matching (`match`/`case`)
Python's `match`/`case` inspects dictionary shapes, types, and guard conditions (`if ...`) in order from top to bottom:

```python
def dispatch_train_signal(signal: dict[str, object]) -> str:
    match signal:
        case {"kind": "emergency", "line": str(line)}:
            return f"HALT:{line}"
        case {"kind": "delay", "minutes": int(mins)} if mins >= 15:
            return "REROUTE"
        case {"kind": "delay", "minutes": int()}:
            return "HOLD"
        case _:
            return "UNKNOWN"
```

* Dict patterns match **at least** the specified keys (extra keys in `signal` are allowed).
* Guard clauses (`if ...`) run only after the pattern structure matches.

### Challenge
Implement `route_event(event: dict[str, object]) -> str` in `webhook_router.py` using `match`/`case` and explicit `None` checks so webhook events route accurately without treating `retry_count = 0` as missing.
