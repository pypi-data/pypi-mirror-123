"""Tests for trading.backtester.strategy."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from collections import namedtuple

import pytest

from trading.backtester.backtester import Backtester
from trading.backtester.config import BacktesterConfig
from trading.backtester.strategy import BacktesterStrategy


INPUT_BACKTESTER_CONFIG = {
    "strategy_parameters": {
        "time_period": 34,
        "multiplier": 1.5
    },
    "initial_balance": 53.0091,
    "initial_balance_currency": "BTC",
    "trading_exchange": "bitmex",
    "starting_timestamp": "2020-01-01 00:00:00",
    "ending_timestamp": "2021-01-01 00:00:00",
    "assets": [
        {
            "trading_symbol": "ADAZ21",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ADABTC",
            "signal_timeframe": "4h",
            "percent_allocation": 100,
        }
    ]
}


@pytest.fixture(name="backtester", scope="class")
def fixture_backtester():
    class Exchange:
        def order(
            self, order_id, position, limit, stop,
            amount, amount_percent, **kwargs
        ):
            return (
                f"{order_id}-{position}-{limit}-{stop}-"
                f"{amount}-{amount_percent}")

        def cancel_all(self):
            return f"cancel-all"

        def cancel(self, order_or_id, **kwargs):
            return f"{order_or_id}"

        def exit_all(self):
            return f"close-all"

        def exit(self, order_or_id, amount, amount_percent, **kwargs):
            return f"{order_or_id}-{amount}-{amount_percent}"

    config = BacktesterConfig.from_dict(INPUT_BACKTESTER_CONFIG)
    Backtester = namedtuple("Backtester", ("config", "data", "exchange"))

    return Backtester(config=config, data="TEST_DATA", exchange=Exchange())


class TestBacktesterStrategy:

    def test_required_backtester_properties(self, backtester):
        """Required for class tests that need the Backtester class."""
        for mock_property in backtester._fields:
            assert mock_property in dir(Backtester)

    def test_successful_initialization(self, backtester):
        strategy = BacktesterStrategy(backtester)
        assert isinstance(strategy, BacktesterStrategy)

        # Create with parameter ovveride
        strategy = BacktesterStrategy(backtester, parameters={"test": 123})
        assert isinstance(strategy, BacktesterStrategy)
        assert strategy.p.test == 123

        with pytest.raises(NotImplementedError):
            strategy.next()

    def test_unsuccessful_initialization(self, backtester):
        # Create with an invalid parameter override
        with pytest.raises(TypeError):
            BacktesterStrategy(backtester, parameters=123)

    def test_strategy_order_functions(self, backtester):
        strategy = BacktesterStrategy(backtester)
        strategy.trading_symbol = backtester.config.assets[0].trading_symbol
        strategy.signal_source_symbol = (
            backtester.config.assets[0].signal_source_symbol)
        strategy.datetime = ["2021-10-18", "2021-10-17"]

        assert strategy.buy() == "order-id-long-None-None-None-None"
        assert strategy.sell() == "order-id-short-None-None-None-None"

        # These functions doesn't return any value
        # we just want to test it if its called properly for coverage
        assert strategy.cancel_all() is None
        assert strategy.cancel("order_object") is None
        assert strategy.exit_all() is None
        assert strategy.exit("ordertype", "amount", "price") is None

    def test_strategy_properties(self, backtester):
        strategy = BacktesterStrategy(backtester)
        assert strategy.data == "TEST_DATA"
        assert strategy.p.time_period == 34
        assert strategy.p.multiplier == 1.5
        assert strategy.parameters.time_period == 34
        assert strategy.parameters.multiplier == 1.5

        assert isinstance(strategy.backtester, tuple)
