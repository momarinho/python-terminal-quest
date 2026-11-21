## Boss Fight: Streaming PII Log Redactor

Centralized log collectors cannot load multi-gigabyte log files into memory before redacting secrets and personal data (LGPD / GDPR). You must stream lines lazily with `yield`, scrub PII deterministically via compiled regex rules, and emit an atomic audit summary.

### Multi-File Architecture (`patterns.py` + `pipeline.py`)
1. **`patterns.py` -> `redact_line(line: str) -> tuple[str, dict[str, int]]`**
   * Scrub three PII categories using compiled regexes and return `(sanitized_line, counts_dict)` where `counts_dict` has keys `"emails"`, `"cpfs"`, `"bearers"`:
     * **Emails:** replace `local@domain.tld` with `<first_char>***@<domain.tld>` (e.g., `ana.silva@acme.com` -> `a***@acme.com`).
     * **Brazilian CPFs:** replace formatted `123.456.789-01` with `***.456.789-**` (preserve middle 6 digits for audit correlation).
     * **Bearer JWT/API Tokens:** replace `Bearer <token>` (case-insensitive `Bearer`) with `Bearer [REDACTED]`.
2. **`pipeline.py` -> `iter_redacted_lines(lines: Iterable[str]) -> Iterator[tuple[str, dict[str, int]]]`**
   * Lazy generator yielding `(sanitized_line, counts)` per line without materializing a list.
3. **`pipeline.py` -> `redact_log_file(src: Path, dest: Path, stats_dest: Path) -> dict[str, int]`**
   * Stream `src` line-by-line into `dest` (using `with` context managers), accumulate total `{"lines": N, "emails": ..., "cpfs": ..., "bearers": ...}`, atomically write the JSON stats to `stats_dest`, and return the stats dict.
