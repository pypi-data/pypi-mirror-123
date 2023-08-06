"""Tests for trading.backtester.warnings."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from trading.backtester.warnings import BacktesterWarning
from trading.backtester.warnings import OrderNotFoundWarning


class TestBacktesterWarnings:

    def test_backtesterwarning(self):
        assert issubclass(BacktesterWarning, UserWarning)

    def test_ordernotfoundwarning(self):
        assert issubclass(OrderNotFoundWarning, BacktesterWarning)
