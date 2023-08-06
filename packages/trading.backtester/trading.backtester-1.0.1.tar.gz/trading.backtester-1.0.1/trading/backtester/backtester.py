"""Module containing the Backtester class."""

from __future__ import annotations

import inspect
import math

import numpy as np

from trading.backtester.config import AttrDict
from trading.backtester.config import BacktesterConfig
from trading.backtester.exchange import BacktesterExchange
from trading.backtester.strategy import BacktesterStrategy


__all__ = [
    # Class exports
    "Backtester",
]


class Backtester:
    """Base strategy class."""

    def __init__(self, config: dict | str):
        """Creates an instance of a new strategy."""
        self._config = BacktesterConfig.load(config)

        self._exchange = BacktesterExchange(
            backtester=self,
            initial_balance=self.config.initial_balance,
            currency=self.config.initial_balance_currency)

        self._strat_class = None
        self._strat = None

    def run(self):
        """The core method to perform backtesting."""
        if self.strategy is None:
            raise ValueError("strategy is not set")

        if self.data is None:
            raise ValueError("data is not set")  # pragma: no cover

        for asset in self.config.assets:
            data = self.data[asset.signal_source_symbol]

            # Add current asset to the strategy
            setattr(self._strat, "trading_symbol", asset.trading_symbol)
            setattr(self._strat, "signal_source_symbol",
                asset.signal_source_symbol)

            # Add current asset to the exchange
            setattr(self._exchange, "trading_symbol", asset.trading_symbol)
            setattr(self._exchange, "signal_source_symbol",
                asset.signal_source_symbol)

            for i, _ in enumerate(data.index):
                # Add the same Trading View-like data but for the index
                setattr(
                    self._exchange,
                    data.index.name,
                    data.index[:(i + 1)][::-1])

                # Create a Trading View-like data object and assign
                # it to the strategy object for Trader's use
                for column in data.columns:
                    padded_data = data[column][:(i + 1)][::-1]
                    padded_data = np.pad(
                        padded_data,
                        (0, self.minimum_indicator_period),
                        mode="constant",
                        constant_values=(np.nan,))

                    setattr(self._strat, column, padded_data)
                    setattr(self._exchange, column, padded_data)

                # Very first period
                if i == 0:
                    self.exchange.start()
                    self.strategy.start()

                # Run next for the rest of the whole backtest
                if i > self.minimum_indicator_period:
                    self.exchange.nextstart()
                    self.strategy.next()
                    self.exchange.nextstop()

                # Run prenext if we're still warming up
                elif i < self.minimum_indicator_period:
                    self.strategy.prenext()

                # Run nextstart if we just finished warming up
                else:
                    self.strategy.nextstart()

            # Ending function calls
            self.strategy.stop()
            self.exchange.stop()

    def set_strategy(
        self,
        strategy: BacktesterStrategy,
        parameters: dict | None = None,
        name=None,
    ):

        """Sets the strategy to be used by the Backtester.

        Arguments:
            strategy: A subclass of the `bt.BacktesterStrategy` class.
            parameters: A dictionary containing a set of strategy
                parameters. If the configuration given to the Backtester
                already has a set of parameters and the user still
                entered another set of parameters in this function,
                the latter is the one we would use.

        Raises:
            ValueError: If the strategy is not a subclass of
                `bt.BacktesterStrategy` or if the input strategy is not
                a class at all. This includes instances.

        """
        if not inspect.isclass(strategy):
            raise ValueError(f"input strategy is not a class: {strategy}")

        if not issubclass(strategy, BacktesterStrategy):
            raise ValueError(f"not a strategy subclass: {type(strategy)}")

        if strategy == BacktesterStrategy:
            raise ValueError(f"invalid strategy type: {type(strategy)}")

        # Try to get the parameters from the configuration if not given
        if not parameters:
            parameters = self._config.strategy_parameters
        else:
            parameters = AttrDict(parameters)

        self._strat_class = strategy
        self._strat = strategy(self, parameters=parameters)
        self._strat.initialize()

    @property
    def config(self) -> BacktesterConfig:
        return self._config

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self._exchange.data

    @property
    def exchange(self):
        return self._exchange

    @property
    def minimum_indicator_period(self) -> int:
        return math.ceil(max(self._config.strategy_parameters.values()))

    @property
    def strategy(self) -> BacktesterStrategy:
        return self._strat
