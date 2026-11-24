class SimpleDeduplicator:
    def __init__(self) -> None:
        self._results: dict[str, str] = {}

    def process_once(self, event_id: str, value: str) -> tuple[str, bool]:
        """Process event_id once returning ('ok:<value>', False); replay stored result with True."""
        return ("", False)
