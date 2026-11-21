from fastapi import FastAPI, HTTPException
from observability import REQUEST_ID_CTX, MetricsRegistry, install_observability


def create_app(
    log_sink: list[dict[str, object]] | None = None,
    metrics: MetricsRegistry | None = None,
) -> FastAPI:
    app = FastAPI(title="Observable Service")
    logs = log_sink if log_sink is not None else []
    registry = metrics if metrics is not None else MetricsRegistry()
    install_observability(app, logs, registry)

    @app.get("/work")
    def do_work() -> dict[str, str | None]:
        return {"request_id": REQUEST_ID_CTX.get()}

    @app.get("/boom")
    def do_boom() -> None:
        raise HTTPException(status_code=500, detail="boom")

    @app.get("/metrics")
    def read_metrics() -> dict[str, object]:
        return registry.snapshot()

    return app
