## Concept: Structured Formatting (`f-strings`) & Stream I/O

Python f-strings (`f"{expr:spec}"`) combine readability with full mini-language formatting for alignment, padding, thousands separators, and percentages.

### Format Specifier Mini-Language
* `{label:<14}` — left-align inside a 14-character column
* `{count:>6,}` — right-align with comma thousands separators
* `{ratio:6.2%}` — multiply by 100 and format with 2 decimals + `%`
* `{temp:+06.1f}` — signed float padded with leading zeros

```python
def format_weather_row(station: str, readings: int, humidity_ratio: float) -> str:
    return f"{station:<12} | {readings:>6,} | {humidity_ratio:6.1%}"
```

### Testable `sys.stdin` / `sys.stdout` Functions
Hardcoding `input()` or `print()` makes CLI processors awkward to test. Accept optional `stream: TextIO | None = None` / `out: TextIO | None = None` defaulting to `sys.stdin` / `sys.stdout`!

### Challenge
Implement `format_slo_row` and `emit_slo_report` in `slo_report.py` to parse `service,requests,errors` CSV lines from an input stream and write formatted report lines to an output stream.
