## Concept: Structured Exceptions (`try`/`except`/`else`/`finally` & `raise ... from`)

Swallowing exceptions with bare `except Exception: return None` hides root causes in production. Instead, wrap low-level errors in meaningful domain exceptions while preserving the causal chain.

### Exception Chaining & `else` / `finally`
* `try:` — keep the `try` block small so you only catch errors from the intended operation.
* `except LowLevelError as exc: raise DomainError(...) from exc` — preserves `__cause__` for debugging and logging.
* `else:` — runs **only** if `try` succeeded without raising (keeps post-parse logic out of `try`).
* `finally:` — **always** runs (success or failure) to release locks, close handles, or emit audit events.

```python
class PacketDecodeError(Exception):
    pass

def parse_telemetry_packet(raw: str, audit_log: list[str]) -> dict[str, object]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PacketDecodeError("Malformed telemetry JSON") from exc
    else:
        audit_log.append("DECODED")
        return data
    finally:
        audit_log.append("CLOSED")
```

### Challenge
Define `PayloadDecodeError` and `InvalidAmountError` (both inheriting from `SettlementError`) and implement `decode_settlement(raw_json: str, audit_log: list[str]) -> dict[str, object]` in `settlement_decoder.py`.
