## Beginner Warm-Up 1: Classes, `self` & Methods

A Python `class` bundles state (`self.balance`) and behavior (`deposit`, `withdraw`) together cleanly:

```python
class SimpleWallet:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def deposit(self, amount: int) -> None:
        self.balance += amount
```

### Challenge
Open `warmup.py` and complete `deposit()` (add `amount`) and `withdraw()` (subtract `amount` and return `True` when sufficient balance, or return `False` without changing `self.balance` when `amount > self.balance`).
