from warmup import MemoryNotifier, welcome_user


def test_welcome_user_records_notification() -> None:
    fake = MemoryNotifier()
    result = welcome_user("ada@example.com", fake)
    assert result == "welcomed:ada@example.com"
    assert fake.sent == [("ada@example.com", "Welcome!")]


def test_memory_notifier_multiple_calls() -> None:
    fake = MemoryNotifier()
    welcome_user("a@example.com", fake)
    welcome_user("b@example.com", fake)
    assert len(fake.sent) == 2
