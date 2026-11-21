from typing import Protocol

from models import Order, TradeFill


class MatchingStrategy(Protocol):
    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]: ...


def _run_price_time(
    incoming: Order,
    resting: list[Order],
) -> tuple[list[TradeFill], list[Order], Order | None]:
    if incoming.side == "BUY":
        candidates = [o for o in resting if o.side == "SELL" and o.price <= incoming.price]
        candidates.sort(key=lambda o: (o.price, o.seq))
    else:
        candidates = [o for o in resting if o.side == "BUY" and o.price >= incoming.price]
        candidates.sort(key=lambda o: (-o.price, o.seq))

    remaining_qty = incoming.qty
    fills: list[TradeFill] = []
    updated_by_id: dict[str, Order | None] = {}

    for counter in candidates:
        if remaining_qty == 0:
            break
        traded = min(remaining_qty, counter.qty)
        remaining_qty -= traded
        buy_id = incoming.order_id if incoming.side == "BUY" else counter.order_id
        sell_id = counter.order_id if incoming.side == "BUY" else incoming.order_id
        fills.append(TradeFill(buy_id=buy_id, sell_id=sell_id, price=counter.price, qty=traded))

        leftover_counter = counter.qty - traded
        updated_by_id[counter.order_id] = (
            counter.with_qty(leftover_counter) if leftover_counter > 0 else None
        )

    next_resting: list[Order] = []
    for item in resting:
        if item.order_id in updated_by_id:
            replacement = updated_by_id[item.order_id]
            if replacement is not None:
                next_resting.append(replacement)
        else:
            next_resting.append(item)

    remainder = incoming.with_qty(remaining_qty) if remaining_qty > 0 else None
    return fills, next_resting, remainder


class PriceTimeStrategy:
    """Matches crossing opposite-side orders by best price then earliest seq; rests remainder."""

    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]:
        return _run_price_time(incoming, resting)


class ImmediateOrCancelStrategy:
    """Matches crossing opposite-side orders immediately; cancels any unfilled remainder."""

    def match(
        self,
        incoming: Order,
        resting: list[Order],
    ) -> tuple[list[TradeFill], list[Order], Order | None]:
        fills, next_resting, _remainder = _run_price_time(incoming, resting)
        return fills, next_resting, None
