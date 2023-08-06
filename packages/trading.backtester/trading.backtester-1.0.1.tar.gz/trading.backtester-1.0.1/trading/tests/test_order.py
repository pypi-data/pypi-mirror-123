"""Tests for trading.backtester.position."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from trading.backtester.order import LIMIT
from trading.backtester.order import MARKET
from trading.backtester.order import STOP_LIMIT
from trading.backtester.order import STOP_MARKET
from trading.backtester.order import VALID_ORDER_TYPES
from trading.backtester.position import SHORT

from trading.backtester.order import Order


class TestBacktesterOrder:

    def test_constants(self):
        assert isinstance(LIMIT, str)
        assert isinstance(MARKET, str)
        assert isinstance(STOP_LIMIT, str)
        assert isinstance(STOP_MARKET, str)
        assert isinstance(VALID_ORDER_TYPES, tuple)

    def test_order_class_initailization(self):
        order = Order(
            order_id="TEST_ORDER_ID",
            position="TEST_POSITION_TYPE",
            ordertype="TEST_ORDER_TYPE",
            amount=1234,
            trading_symbol="TEST_TRADING_SYMBOL",
            signal_source_symbol="TEST_SIGNAL_SOURCE_SYMBOL",
            limit=1234,
            stop=1234,
            closing_timestamp="TEST_CLOSING_TIMESTAMP",
            creation_timestamp="TEST_CREATION_TIMESTAMP",
            execution_timestamp="TEST_EXECUTION_TIMESTAMP",
            cancellation_timestamp="TEST_CANCELLATION_TIMESTAMP")

        assert order.id == "TEST_ORDER_ID"
        assert order.type == "TEST_ORDER_TYPE"

        order_2 = Order(
            order_id="TEST_ORDER_ID_2",
            position=SHORT,
            ordertype="TEST_ORDER_TYPE_2",
            amount=1234,
            trading_symbol="TEST_TRADING_SYMBOL_2",
            signal_source_symbol="TEST_SIGNAL_SOURCE_SYMBOL_2",
            limit=1234,
            stop=1234,
            closing_timestamp="TEST_CLOSING_TIMESTAMP",
            creation_timestamp="TEST_CREATION_TIMESTAMP",
            execution_timestamp="TEST_EXECUTION_TIMESTAMP",
            cancellation_timestamp="TEST_CANCELLATION_TIMESTAMP")

        assert order_2.id == "TEST_ORDER_ID_2"
        assert order_2.type == "TEST_ORDER_TYPE_2"
        assert order_2.position_amount == -1234
        assert order_2.pnl(1235) == 100.08103727714747
