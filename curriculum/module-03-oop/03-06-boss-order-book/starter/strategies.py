from typing import Protocol

from models import Order, TradeFill


class MatchingStrategy(Protocol):
    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]: ...


class PriceTimeStrategy:
    """Matches crossing opposite-side orders by best price then earliest seq; rests remainder."""

    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]:
        # TODO: implement price-time matching and return (fills, updated_resting, remainder_or_none)
        _ = TradeFill
        return [], list(resting), incoming


class ImmediateOrCancelStrategy:
    """Matches crossing opposite-side orders immediately; cancels any unfilled remainder."""

    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]:
        # TODO: reuse matching logic but return None for unfilled remainder
        return [], list(resting), None
