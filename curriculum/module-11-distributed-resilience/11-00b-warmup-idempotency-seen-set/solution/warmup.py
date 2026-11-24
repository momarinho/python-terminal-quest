class SimpleDeduplicator:
    def __init__(self) -> None:
        self._results: dict[str, str] = {}

    def process_once(self, event_id: str, value: str) -> tuple[str, bool]:
        """Process event_id once returning ('ok:<value>', False); replay stored result with True."""
        if event_id in self._results:
            return (self._results[event_id], True)
        result = f"ok:{value}"
        self._results[event_id] = result
        return (result, False)
