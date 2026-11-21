from __future__ import annotations

from collections.abc import Callable

from pydantic import BaseModel, Field


class ToolDeniedError(PermissionError):
    """Raised when an unknown or non-read-only tool invocation is attempted."""


class OrderLookupArgs(BaseModel):
    order_id: str = Field(min_length=2)


class MetricQueryArgs(BaseModel):
    service: str = Field(min_length=2)
    window_minutes: int = Field(ge=1, le=1440)


ToolHandler = Callable[[BaseModel], dict[str, object]]


class ReadOnlyToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[type[BaseModel], ToolHandler]] = {}

    def register(
        self,
        name: str,
        args_schema: type[BaseModel],
        handler: ToolHandler,
    ) -> None:
        self._tools[name] = (args_schema, handler)

    def execute(self, name: str, raw_args: dict[str, object]) -> dict[str, object]:
        entry = self._tools.get(name)
        if entry is None:
            raise ToolDeniedError(f"Tool '{name}' is not in the read-only allowlist")
        schema_cls, handler = entry
        validated = schema_cls.model_validate(raw_args)
        return handler(validated)
