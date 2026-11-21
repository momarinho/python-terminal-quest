from client import ProbeClient


class HealthAggregator:
    def __init__(self, probe_client: ProbeClient) -> None:
        self.probe_client = probe_client

    async def check_cluster(self, targets: dict[str, str]) -> dict[str, object]:
        """Fan out probes via asyncio.TaskGroup and summarize cluster health."""
        # TODO: run probes concurrently, sort services by name, compute overall/up_count/down_count
        return {"overall": "DOWN", "up_count": 0, "down_count": 0, "services": []}
