"""Module containing the backtester strategy class."""

from __future__ import annotations

from trading.backtester.config import AttrDict
from trading.backtester.position import LONG
from trading.backtester.position import SHORT


__all__ = [
    # Class exports
    "BacktesterStrategy",
]


class BacktesterStrategy:
    """Base strategy class.

    Arguments:
        backtester: The instance of the this strategy's backtester.
        parameters: Strategy parameters that are used as overrides
            over the strategy parameters set in the parent backtester's
            internal configuration.
    """

    def __init__(
        self,
        backtester: Backtester,
        parameters: dict | AttrDict | None = None,
    ):

        """Creates an instance of a new Backtester strategy."""

        # Check if strategy parameters configuration is dictionary
        if parameters and not isinstance(parameters, dict):
            raise TypeError(
                "strategy parameters configuration must be a dictionary, "
                f"got {type(parameters)}")

        self._backtester = backtester
        self._parameters = (
            AttrDict(parameters) if parameters
            else self.config.strategy_parameters)

    def initialize(self):
        """Data initialization for the strategy.

        This function is where all the indicator data are calculated.
        Only runs once and it runs when the strategy class is
        initialized. Similar to how the `__init__` function works.

        The correct way of adding a new indicator is by modifying the
        `self.data` variable of the strategy. This variable is a
        `DataFrame` and new column can be added by its usual syntax:

        ```python
        from trading.backtester import ta

        self._data[symbol]["ema50"] = ta.ema(
            self.data[symbol].close,
            timeperiod=50)

        # Use `indicator_period` parameter from configuration
        self._data[symbol]["another_indicator"] = ta.ema(
            self.data[symbol].close,
            timeperiod=self.p.indicator_period)
        ```

        This function can also be used to initialize new variables that
        can help the overall strategy.
        """

    def start(self):
        """Runs at the first period of each asset of a backtest run."""

    def prenext(self):
        """Runs before the minimum indicator period is reached.

        There are different indicators used in a strategy and some of
        these indicators have different required number of periods
        before they can be used. The largest required indicator period
        is called the "minimum indicator period".

        For Example, our strategy uses this list of indicators:
        - EMA 200 (required number of periods is 200)
        - SMA 50 (required number of periods is 50)
        - RSI 14 (required number of periods is 14)

        So for this strategy, the minimum indicator period is 200 since
        that's the largest required indicator period. Given this,
        `prenext()` is called while period is less than 200.
        """

    def nextstart(self):
        """Runs when the minimum indicator period is reached.

        See the documentation for `BacktesterStrategy.prenext()` for an
        explanation of what the minimum indicator period is.
        """

        # Called once for 1st full calculation - defaults to regular next
        self.next()  # pragma: no cover

    def next(self):
        """Runs after the minimum indicator period is reached.

        This is the main function of the strategy. The different order
        functions are used here to generate long or short signals.

        See the documentation for `BacktesterStrategy.prenext()` for an
        explanation of what the minimum indicator period is.
        """
        raise NotImplementedError

    def stop(self):
        """Runs at the end of the backtest run."""

    def buy(
        self,
        order_id: str = "order-id",
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
    ) -> Order:

        """Go long or reduce/close a short position."""
        return self.order(
            order_id, LONG, limit=limit, stop=stop,
            amount=amount, amount_percent=amount_percent)

    def sell(
        self,
        order_id: str = "order-id",
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
    ) -> Order:

        """Go short or reduce/close a long position."""
        return self.order(
            order_id, SHORT, limit=limit, stop=stop,
            amount=amount, amount_percent=amount_percent)

    def order(
        self,
        order_id: str,
        position: str,
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
    ) -> Order:

        """Lower-level order creation function.

        See the documentation for `BacktesterExchange.order()`
        for an explanation of what the different function arguments are.
        """
        return self.bt.exchange.order(
            order_id=order_id,
            position=position,
            limit=limit,
            stop=stop,
            amount=amount,
            amount_percent=amount_percent)

    def cancel_all(self):
        """Cancels all pending orders."""
        self.bt.exchange.cancel_all()

    def cancel(self, order_or_id : Order | str):
        """Cancels a pending order by referencing the order or its ID.

        See the documentation for `BacktesterExchange.cancel()`
        for an explanation of what the different function arguments are.
        """
        self.bt.exchange.cancel(order_or_id)

    def exit_all(self):
        """Exits all trades."""
        self.bt.exchange.exit_all()

    def exit(
        self,
        order_or_id : Order | str,
        amount: float | None = None,
        amount_percent: float | None = None,
    ):

        """Exit a trade by referencing the order or its ID.

        See the documentation for `BacktesterExchange.exit()`
        for an explanation of what the different function arguments are.
        """
        self.bt.exchange.exit(
            order_or_id=order_or_id,
            amount=amount,
            amount_percent=amount_percent)

    @property
    def bt(self) -> Backtester:
        """Shorthand for easier access of the backtester instance."""
        return self._backtester

    @property
    def backtester(self) -> Backtester:
        return self._backtester

    @property
    def config(self) -> BacktesterConfig:
        return self.bt.config

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self.bt.data

    @property
    def p(self) -> AttrDict:
        """Shorthand for easier access of parameters."""
        return self.parameters

    @property
    def parameters(self) -> AttrDict:
        return self._parameters
