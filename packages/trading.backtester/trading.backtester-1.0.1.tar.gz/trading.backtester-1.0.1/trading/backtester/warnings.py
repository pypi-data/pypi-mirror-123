"""Module containing custom warning categories for the backtester."""


__all__ = [
    # Class exports
    "BacktesterWarning",
    "OrderNotFoundWarning",
]


class BacktesterWarning(UserWarning):
    """Base category for any backtester-related warnings."""


class OrderNotFoundWarning(BacktesterWarning):
    """Used when an order can't be identified while cancelling."""
