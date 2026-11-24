from pydantic import BaseModel, Field  # noqa: F401


class ServiceItem(BaseModel):
    name: str
    # Reveal: constrain port with Field(ge=1, le=65535)
    port: int = 8000


def validate_service(raw: dict[str, object]) -> ServiceItem:
    """Validate an untyped dict into a ServiceItem model."""
    # Reveal: return ServiceItem.model_validate(raw)
    return ServiceItem(name="todo")


def dump_service_dict(item: ServiceItem) -> dict[str, object]:
    """Serialize a ServiceItem into a plain Python dictionary."""
    # Reveal: return item.model_dump()
    return {}
