## Concept: Compiled Regexes & Named Capture Groups

Pre-compiling patterns once at module load with `re.compile(...)` avoids re-parsing the regex engine bytecode inside tight loops, and `(?P<name>...)` named groups turn positional `group(1)` guesses into self-documenting `.groupdict()` dicts.

### Compiled Patterns, `.fullmatch()` & `.finditer()`
```python
import re

CATALOG_RE = re.compile(
    r"^(?P<shelf>[A-Z]{2})-(?P<bin>\d{4}):\s*(?P<title>.+?)$"
)

match = CATALOG_RE.match("AB-0412: Field Guide")
if match:
    data = match.groupdict()  # {'shelf': 'AB', 'bin': '0412', 'title': 'Field Guide'}
```

### Guardrails
* Always use raw strings (`r"..."`) so backslashes (`\d`, `\s`, `\b`) aren't interpreted by Python string escaping.
* Anchor full-line parsers with `^...$` or `.fullmatch(...)` when validating entire tokens, and use `.finditer(...)` to extract all structured `key=value` tags across a line.

### Challenge
Implement `parse_access_entry`, `mask_bearer_tokens`, and `extract_trace_tags` in `regex_extractor.py`.
