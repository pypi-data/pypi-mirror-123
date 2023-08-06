"""Module containing order constants and classes for the backtester."""

from __future__ import annotations

from dataclasses import dataclass

from trading.backtester.position import SHORT


__all__ = [
    # Constants export
    "LIMIT",
    "MARKET",
    "STOP_LIMIT",
    "STOP_MARKET",
    "VALID_ORDER_TYPES",
]


LIMIT = "limit"
MARKET = "market"
STOP_LIMIT = "stop_limit"
STOP_MARKET = "stop_market"

# Consolidate into a list of string values that can be used
# for validation of newly created orders
VALID_ORDER_TYPES = (MARKET, LIMIT, STOP_LIMIT, STOP_MARKET)


@dataclass
class Order:
    order_id: str
    position: str
    ordertype: str
    amount: float
    trading_symbol: str
    signal_source_symbol: str
    limit: float | None = None
    stop: float | None = None
    closing_timestamp: str | None = None
    creation_timestamp: str | None = None
    execution_timestamp: str | None = None
    cancellation_timestamp: str | None = None

    def value(self, price: float):
        if self.limit is None or self.execution_timestamp is None:
            return self.amount
        return abs((price / self.limit) * self.amount)

    def pnl(self, price: float):
        return self.value(price) / self.amount * 100

    @property
    def id(self) -> str:
        return self.order_id

    @property
    def type(self) -> str:
        return self.ordertype

    @property
    def position_amount(self) -> str:
        return -self.amount if self.position == SHORT else self.amount
