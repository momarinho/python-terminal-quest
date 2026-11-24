from pydantic import BaseModel, Field


class ServiceItem(BaseModel):
    name: str
    port: int = Field(ge=1, le=65535)


def validate_service(raw: dict[str, object]) -> ServiceItem:
    """Validate an untyped dict into a ServiceItem model."""
    return ServiceItem.model_validate(raw)


def dump_service_dict(item: ServiceItem) -> dict[str, object]:
    """Serialize a ServiceItem into a plain Python dictionary."""
    return item.model_dump()
