import asyncio

from client import ProbeClient


class HealthAggregator:
    def __init__(self, probe_client: ProbeClient) -> None:
        self.probe_client = probe_client

    async def check_cluster(self, targets: dict[str, str]) -> dict[str, object]:
        """Fan out probes via asyncio.TaskGroup and summarize cluster health."""
        if not targets:
            return {"overall": "UP", "up_count": 0, "down_count": 0, "services": []}

        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(self.probe_client.probe(service, url))
                for service, url in targets.items()
            ]

        services = sorted((task.result() for task in tasks), key=lambda item: str(item["service"]))
        up_count = sum(1 for item in services if item["status"] == "UP")
        degraded_count = sum(1 for item in services if item["status"] == "DEGRADED")
        down_count = sum(1 for item in services if item["status"] == "DOWN")

        if up_count == len(services):
            overall = "UP"
        elif up_count + degraded_count > 0:
            overall = "DEGRADED"
        else:
            overall = "DOWN"

        return {
            "overall": overall,
            "up_count": up_count,
            "down_count": down_count,
            "services": services,
        }
