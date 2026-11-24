def add_numbers(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def split_bill_cents(total_cents: int, people: int) -> tuple[int, int]:
    """Return (each_share, leftover_cents) using // and %."""
    return (total_cents // people, total_cents % people)


def greet_player(name: str, level: int) -> str:
    """Return 'Welcome, <name>! Level <level>'."""
    return f"Welcome, {name}! Level {level}"
