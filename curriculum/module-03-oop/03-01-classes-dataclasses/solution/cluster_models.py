from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServiceEndpoint:
    name: str
    port: int
    healthy: bool = True
    latency_ms: int = 0

    def __post_init__(self) -> None:
        cleaned = self.name.strip()
        if not cleaned:
            raise ValueError("Endpoint name must not be blank")
        object.__setattr__(self, "name", cleaned)
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")
        if self.latency_ms < 0:
            raise ValueError(f"latency_ms must be non-negative: {self.latency_ms}")


@dataclass
class ClusterSnapshot:
    region: str
    endpoints: list[ServiceEndpoint] = field(default_factory=list)

    def register(self, endpoint: ServiceEndpoint) -> None:
        self.endpoints.append(endpoint)

    def healthy_ratio(self) -> float:
        if not self.endpoints:
            return 0.0
        healthy_count = sum(1 for ep in self.endpoints if ep.healthy)
        return healthy_count / len(self.endpoints)
