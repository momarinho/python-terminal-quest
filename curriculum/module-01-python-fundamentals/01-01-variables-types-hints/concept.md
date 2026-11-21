## Concept: Dynamic Variables, Explicit Casting & Type Hints

Python variables bind names to strongly typed objects at runtime—you never get silent string-to-number coercion like `"5" + 2` (which raises `TypeError`). Modern Python 3.12+ pairs runtime type safety with readable static type hints (`int`, `float`, `bool`, `str`, and `X | None` union syntax).

### Explicit Type Conversion
When reading configuration from environment variables or CLI flags, every raw input begins as a `str`. Convert explicitly and validate bounds:

```python
def parse_greenhouse_sensor(
    raw_zone: str,
    raw_target_temp: str,
    raw_misting: str,
) -> dict[str, int | float | bool | str]:
    zone = int(raw_zone.strip())
    target_temp = float(raw_target_temp.strip())
    misting = raw_misting.strip().lower() in {"1", "true", "yes", "on"}
    return {
        "zone": zone,
        "target_temp": target_temp,
        "misting": misting,
    }
```

### Why `bool("false")` Is a Classic Trap
In Python, `bool(value)` tests **truthiness**, not string spelling:
* `bool("false")` evaluates to `True` because `"false"` is a non-empty string!
* Always normalize booleans explicitly (`raw.strip().lower() in {"1", "true", "yes", "on"}`) and reject unknown strings if strict parsing is required.

### Challenge
Implement `parse_service_config` in `config_parser.py` to convert raw service environment strings into typed values (`service_name: str`, `port: int`, `timeout_sec: float`, `tls_enabled: bool`, and optional `region: str | None`).
