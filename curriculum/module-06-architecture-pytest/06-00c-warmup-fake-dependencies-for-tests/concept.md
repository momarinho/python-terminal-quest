## Beginner Warm-Up 3: Dependency Injection for Clean Tests

Instead of hardcoding an external email server inside business logic, pass a `Protocol` dependency:

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, recipient: str, msg: str) -> None: ...

def welcome_user(email: str, notifier: Notifier) -> str:
    notifier.send(email, "Welcome!")
    return f"welcomed:{email}"
```

### Challenge
Implement `welcome_user` and `MemoryNotifier.send` in `warmup.py`.
