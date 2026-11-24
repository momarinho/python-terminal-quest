class SimpleBreaker:
    def __init__(self, threshold: int = 3) -> None:
        self.threshold = threshold
        self.failures = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        """Increment failures and switch state to 'OPEN' at threshold."""
        self.failures += 1
        if self.failures >= self.threshold:
            self.state = "OPEN"

    def record_success(self) -> None:
        """Reset failures to 0 and state to 'CLOSED'."""
        self.failures = 0
        self.state = "CLOSED"
