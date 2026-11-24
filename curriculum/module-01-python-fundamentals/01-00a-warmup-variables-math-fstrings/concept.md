## Beginner Warm-Up 1: Variables, Math & `f-strings`

Welcome to Day 1! Every exercise starts with an exact syntax pattern shown right here in **Concept** so you can learn by typing real Python without guesswork.

### 1. Basic Addition (`+`)
```python
def add_numbers(a: int, b: int) -> int:
    return a + b
```

### 2. Floor Division (`//`) & Remainder (`%`)
Use `//` to get whole groups and `%` to get the leftover items:
```python
def split_bill_cents(total_cents: int, people: int) -> tuple[int, int]:
    return (total_cents // people, total_cents % people)
```

### 3. Formatting Strings with `f"..."`
```python
def greet_player(name: str, level: int) -> str:
    return f"Welcome, {name}! Level {level}"
```

### Challenge
Open `warmup.py` and replace the 3 placeholder return statements using the patterns above.
