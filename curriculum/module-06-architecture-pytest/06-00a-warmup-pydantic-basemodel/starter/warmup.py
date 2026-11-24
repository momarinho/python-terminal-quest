from pydantic import BaseModel, Field  # noqa: F401


class ServiceItem(BaseModel):
    name: str
    port: int = 8000


def validate_service(raw: dict[str, object]) -> ServiceItem:
    """Validate an untyped dict into ServiceItem."""
    return ServiceItem(name="todo")


def dump_service_dict(item: ServiceItem) -> dict[str, object]:
    """Serialize ServiceItem to a Python dict."""
    return {}
