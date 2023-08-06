"""Tests for trading.backtester.errors."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from trading.backtester.errors import BacktesterException
from trading.backtester.errors import InsufficientBalanceError


class TestBacktesterErrors:

    def test_backtesterexception(self):
        assert issubclass(BacktesterException, Exception)

    def test_insufficientbalanceerror(self):
        assert issubclass(InsufficientBalanceError, BacktesterException)
