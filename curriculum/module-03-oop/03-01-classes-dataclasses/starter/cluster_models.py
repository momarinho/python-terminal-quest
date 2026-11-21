from dataclasses import dataclass, field


@dataclass(frozen=True)
class ServiceEndpoint:
    name: str
    port: int
    healthy: bool = True
    latency_ms: int = 0

    def __post_init__(self) -> None:
        # TODO: validate non-blank name, port in 1..65535, latency_ms >= 0
        pass


@dataclass
class ClusterSnapshot:
    region: str
    endpoints: list[ServiceEndpoint] = field(default_factory=list)

    def register(self, endpoint: ServiceEndpoint) -> None:
        # TODO: append endpoint to self.endpoints
        pass

    def healthy_ratio(self) -> float:
        # TODO: return fraction of healthy endpoints (0.0 if empty)
        return 0.0
