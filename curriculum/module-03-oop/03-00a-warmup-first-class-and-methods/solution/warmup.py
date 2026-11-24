class SimpleWallet:
    def __init__(self, balance: int = 0) -> None:
        self.balance = balance

    def deposit(self, amount: int) -> None:
        """Add amount to self.balance."""
        self.balance += amount

    def withdraw(self, amount: int) -> bool:
        """Subtract amount if affordable and return True, else False."""
        if amount > self.balance:
            return False
        self.balance -= amount
        return True
