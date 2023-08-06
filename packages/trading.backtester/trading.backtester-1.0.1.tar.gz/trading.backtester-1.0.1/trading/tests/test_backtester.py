"""Tests for trading.backtester.backtester."""
# pylint: disable=missing-class-docstring,missing-function-docstring,line-too-long

import pytest

from trading.backtester import ta
from trading.backtester.config import BacktesterConfig
from trading.backtester.strategy import BacktesterStrategy
import trading.backtester as bt


INPUT_BACKTESTER_CONFIG = {
    "strategy_parameters": {
        "ema50_period": 50,
        "ema200_period": 200
    },
    "initial_balance": 2000,
    "initial_balance_currency": "USD",
    "trading_exchange": "bitmex",
    "starting_timestamp": "2020-01-01 00:00:00",
    "ending_timestamp": "2021-10-17 00:00:00",
    "assets": [
        {
            "trading_symbol": "XBTUSD",
            "trading_timeframe": "1d",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "BTC/USDT",
            "signal_timeframe": "1d",
            "percent_allocation": 91,
        },
        {
            "trading_symbol": "ADAUSD",
            "trading_timeframe": "1d",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ADA/USDT",
            "signal_timeframe": "1d",
            "percent_allocation": 9,
        }
    ]
}


@pytest.fixture(name="backtester", scope="class")
def fixture_backtester():
    return bt.Backtester(INPUT_BACKTESTER_CONFIG)


class TestBacktester:

    def test_successful_initialization(self, backtester):
        assert isinstance(backtester, bt.Backtester)
        assert backtester.config == BacktesterConfig.from_dict(
            INPUT_BACKTESTER_CONFIG)
        assert backtester.data is not None

    def test_unsuccessful_initialization(self, backtester):
        # No strategies yet
        backtester._strat = None
        with pytest.raises(ValueError):
            backtester.run()

    def test_unsuccessful_setting_of_strategy(self, backtester):
        with pytest.raises(ValueError):
            backtester.set_strategy(None)

        with pytest.raises(ValueError):
            class InvalidClass: pass
            backtester.set_strategy(InvalidClass)

        with pytest.raises(ValueError):
            backtester.set_strategy(BacktesterStrategy)

    def test_successful_setting_of_strategy(self, backtester):
        class StrategySubclass(bt.BacktesterStrategy): pass
        backtester.set_strategy(StrategySubclass, name="TEST1")
        assert backtester._strat_class == StrategySubclass
        assert isinstance(backtester.strategy, bt.BacktesterStrategy)
        assert backtester.strategy.parameters.ema50_period == 50
        assert backtester.strategy.parameters.ema200_period == 200

        backtester.set_strategy(StrategySubclass, parameters={"period": 1000}, name="TEST2")
        assert backtester._strat_class == StrategySubclass
        assert isinstance(backtester.strategy, bt.BacktesterStrategy)
        assert backtester.strategy.parameters.period == 1000

    def test_buy_at_start_strategy(self, backtester):
        class BuyAtStartStrategy(bt.BacktesterStrategy):
            def start(self):
                self.bought = False

            def next(self):
                if not self.bought:
                    self.buy()
                    self.bought = True

        backtester.exchange.reset()
        backtester.set_strategy(BuyAtStartStrategy)
        backtester.run()

        assert list(backtester.exchange.equity["XBTUSD"].values())[-1] == 16076.115801547869
        assert list(backtester.exchange.equity["ADAUSD"].values())[-1] == 11882.532884674214

    def test_golden_cross_strategy(self, backtester):
        class GoldenCrossStrategy(bt.BacktesterStrategy):
            def initialize(self):
                for asset in self.config.assets:
                    symbol = asset.signal_source_symbol

                    self.data[symbol]["ema50"] = ta.ema(
                        self.data[symbol].close,
                        timeperiod=self.p.ema50_period)

                    self.data[symbol]["ema200"] = ta.ema(
                        self.data[symbol].close,
                        timeperiod=self.p.ema200_period)

            def next(self):
                if ta.crossover(self.ema50, self.ema200):
                    self.exit_all()
                    self.buy()

                if ta.crossunder(self.ema50, self.ema200):
                    self.exit_all()
                    self.sell()

        backtester.exchange.reset()
        backtester.set_strategy(GoldenCrossStrategy)
        backtester.run()

        assert list(backtester.exchange.equity["XBTUSD"].values())[-1] == 11269.832192745862
        assert list(backtester.exchange.equity["ADAUSD"].values())[-1] == 5656.618610747052
