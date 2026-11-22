## Concept: `pytest` Engineering & Pure-Python Test Doubles

While Python's stdlib ships `unittest` (xUnit class boilerplate) and `doctest` (inline docstring examples), **`pytest`** is the industry standard thanks to plain `assert` introspection, composable `@pytest.fixture`s, `@pytest.mark.parametrize`, and `monkeypatch`.

### Pure-Python Test Doubles (`Fake`, `Stub`, `Spy`) Over Fragile Mocks
Overusing `unittest.mock.patch` couples tests to internal import paths. Inject `Protocol` ports and test with crisp in-memory doubles:
* **Fake:** Working lightweight implementation (e.g., `dict`-backed `InMemoryBookRepo`).
* **Stub:** Returns canned answers (`FixedTokenGen`).
* **Spy:** Records outbound calls so tests assert side effects (`SpyEmailSender.sent`).

### Writing Contract Verification Assertions
A good test suite proves **both** that valid implementations pass and that subtle regressions (e.g. emailing unknown users, skipping case normalization, or silently dropping outbound mail) fail with `AssertionError`.

```python
class SpyNotifier:
    def __init__(self) -> None:
        self.messages: list[tuple[str, str]] = []

    def send(self, recipient: str, body: str) -> None:
        self.messages.append((recipient, body))
```

### Challenge
Implement `PasswordResetService` in `notifier_service.py` and the in-memory `FakeUserRepo`, `StubTokenGenerator`, `SpyEmailSender`, and `verify_reset_service_contract` in `doubles.py`.
