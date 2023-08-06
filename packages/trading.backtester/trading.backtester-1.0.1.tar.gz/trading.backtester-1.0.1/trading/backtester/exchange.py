"""Module containing the backtester exchange class."""

from __future__ import annotations

import warnings

import pandas as pd

import trading.datasets_core as tdc

from trading.backtester.order import LIMIT
from trading.backtester.order import MARKET
from trading.backtester.order import STOP_LIMIT
from trading.backtester.order import STOP_MARKET

from trading.backtester.position import LONG
from trading.backtester.position import SHORT
from trading.backtester.position import VALID_POSITION_TYPES

from trading.backtester.errors import InsufficientBalanceError
from trading.backtester.errors import InsufficientPositionAmountError
from trading.backtester.order import Order
from trading.backtester.warnings import OrderNotFoundWarning


__all__ = [
    # Class exports
    "BacktesterExchange",
]


class BacktesterExchange:

    """Exchange/Broker abstraction for the backtester.

    This represents a hyper exchange that can download any data from any
    real exchange and it also contains all the balance, orders, trades,
    and positions information.

    Arguments:
        backtester: The instance of the this exchange's backtester.
        initial_balance: Initial balance of the exchange when an
            instance is created
        currency: Determines the quote currency of the balance
            and the PnL and value of positions in the exchange.

    """

    def __init__(
        self,
        backtester: Backtester,
        initial_balance: float = 10000,
        currency: str = "USD",
    ):

        """Creates an instance of a new Backtester exchange.

        Each accounting variable has their own structure:
            asset_balances: A one-level dictionary with the asset
                trading symbols as its keys.
            equity: A dictionary of dictionaries with the asset trading
                symbols as its first-level keys and then the timestamp
                per record as its second-level keys.
            pending_orders: A list of orders
            open_trades: A list of executed orders that are still open
            closed_trades: A list of closed trades
            order_history: A dictionary of dictionaries with the asset
                trading symbols as its first-level keys and then the
                timestamp per record as its second-level keys.
            positions: A one-level dictionary with the asset trading
                symbols as its keys.
        """
        self._backtester = backtester
        self._initial_balance = float(initial_balance)
        self._currency = str(currency)

        # Accounting variables
        self._asset_balances = {}
        self._equity = {}
        self._pending_orders = []
        self._open_trades = []
        self._cancelled_orders = []
        self._closed_trades = []

        for asset in self.bt.config.assets:

            # Divide the balance per symbol
            self._asset_balances[asset.trading_symbol] = (
                self._initial_balance * (asset.percent_allocation / 100.0))

            # Initialize other account variables
            self._equity[asset.trading_symbol] = {}

        # Load OHLCV datasets
        self._data = self._fetch_ohlcv()

    def reset(self):
        self.__init__(self.backtester, self._initial_balance, self.currency)

    def start(self):
        """Runs at the very first period of a backtest run."""

    def nextstart(self):
        """Runs at the start of each period."""

    def nextstop(self):
        """Runs after the end of every period in the data."""

        # Update orders
        for pending_order in self.pending_orders[:]:
            execute_order = False

            if pending_order.type == MARKET:
                execute_order = True
                pending_order.limit = self.close[0]

            elif pending_order.type == LIMIT:
                if ((pending_order.position == LONG and
                     pending_order.limit <= self.high[0]) or
                    (pending_order.position == SHORT and
                     pending_order.limit >= self.low[0])
                ):
                    execute_order = True

            elif pending_order.type == STOP_MARKET:
                if self.low[0] <= pending_order.stop <= self.high[0]:
                    execute_order = True
                    pending_order.limit = self.close[0]

            if execute_order:
                pending_order.execution_timestamp = self.datetime[0]
                self._pending_orders.remove(pending_order)
                self._open_trades.append(pending_order)

        self._update_equity()

    def stop(self):
        """Runs at the end of the backtest run."""

    def order(
        self,
        order_id: str,
        position: str,
        limit: float | None = None,
        stop: float | None = None,
        amount: float | None = None,
        amount_percent: float | None = None,
    ) -> Order:

        """Create an order.

        Arguments:
            order_id: Used to identify the orders in the exchange.
            position: The position of the order. Value can either be
                "long" or "short".
            limit: Optional order limit price in the exchange currency.
                If both `limit` and `stop` prices are `None`, the order
                type is market order.
            stop: Optional order stop price in the exchange currency.
                If both `limit` and `stop` prices are `None`, the order
                type is market order.
            amount: Optional order amount in the exchange currency.
            amount_percent: Optional order amount (in percentage) in the
                exchange currency. This argument takes precedence over
                the `amount` parameter. If both are not provided, the
                order will use the available wallet balance as basis.

        Raises:
            ValueError: Raised when the input position type is not
                found in the list of valid values. Check out
                `trading.backtester.position.VALID_POSITION_TYPES` for
                the list of valid values.
            InsufficientBalanceError: Raised when the remaining wallet
                balance in the exchange is no longer enough to create
                an order.
            ValueError: Raised when number arguments are negative
                numbers or zero.

        Return:
            The created order instance. This is only for the user's
            copy. The order returned is automatically added to the
            exchange's record of pending orders.
        """

        # Make sure position and order types are valid values
        if position not in VALID_POSITION_TYPES:
            raise ValueError(f"invalid position type: {position!r}")

        # Automatically determine the order type
        if limit is not None and stop is not None:
            ordertype = STOP_LIMIT
        elif limit is None and stop is not None:
            ordertype = STOP_MARKET
        elif limit is not None and stop is None:
            ordertype = LIMIT
        else:
            ordertype = MARKET

        # Make sure amount percent is between 1 and 100 (inclusive)
        if isinstance(amount_percent, (float, int)):
            if not(1 <= amount_percent <= 100):
                raise ValueError(f"amount_percent must be between 1 and 100")
        elif amount_percent is not None:
            raise ValueError(f"invalid amount_percent value: {amount_percent}")

        # Make sure amount is a positive number if given
        if amount_percent is None and isinstance(amount, (float, int)):
            if amount <= 0:
                raise ValueError(f"amount must be a positive number: {amount}")
        elif amount_percent is None and amount is not None:
            raise ValueError(f"invalid amount value: {amount}")

        # Automatically determine the actual order amount
        wallet_balance = self._asset_balances[self.trading_symbol]
        if amount_percent:
            amount = wallet_balance * (float(amount_percent) / 100.0)
        elif amount:
            amount = float(amount)
        else:
            amount = wallet_balance

        # Make sure we still have enough balance in the exchange for the
        # specified order amount
        if wallet_balance <= 0.0 or amount > wallet_balance:
            raise InsufficientBalanceError(
                f"tried to create an order {amount} {self.currency} with "
                f"{wallet_balance} {self.currency} balance")

        if isinstance(limit, (float, int)):
            if limit <= 0:
                raise ValueError(f"limit price must be positive: {limit}")
        elif limit is not None:
            raise ValueError(f"invalid limit price: {limit}")

        if isinstance(stop, (float, int)):
            if stop <= 0:
                raise ValueError(f"stop price must be positive: {stop}")
        elif stop is not None:
            raise ValueError(f"invalid stop price: {stop}")

        order = Order(
            order_id=order_id,
            ordertype=ordertype,
            position=position,
            trading_symbol=self.trading_symbol,
            signal_source_symbol=self.signal_source_symbol,
            creation_timestamp=self.datetime[0],
            limit=limit,
            stop=stop,
            amount=amount,
        )

        self._pending_orders.append(order)
        self._asset_balances[self.trading_symbol] -= order.amount

        return order

    def cancel_all(self):
        """Cancels all pending orders."""
        for pending_order in self.pending_orders[:]:
            self.cancel(pending_order)

    def cancel(self, order_or_id: Order | str):

        """Cancels a pending order by referencing the order or its ID.

        Arguments:
            order_or_id: Used to identify the orders in the exchange. If
                this is a string, it is considered as a order ID. If its
                an `Order` object then the order itself is deleted from
                the list of pending orders.

        Raises:
            OrderNotFoundError: Raised when the exchange can't find any
                pending orders relating to the `order_or_id` input.
        """
        target_order = None

        # Let's first check if the input is an object instance
        if isinstance(order_or_id, Order):
            pending_orders = [order_or_id]
            order_id = str(order_or_id.id)
        else:
            pending_orders = self.pending_orders[:]
            order_id = str(order_or_id)

        # Try converting it into a string and consider as order ID
        # then loop through each pending order to try and find a match
        for pending_order in pending_orders:
            if pending_order.id != order_id:
                continue

            target_order = pending_order

            # We found it so we need to remove it from the pending order
            # list and add the order amount back to the asset balances
            self._pending_orders.remove(target_order)
            self._asset_balances[target_order.trading_symbol] += (
                target_order.amount)

            # Add cancellation timestamp
            target_order.cancellation_timestamp = self.datetime[0]
            self._cancelled_orders.append(target_order)

        # We failed to search for the target order
        if target_order is None:
            warnings.warn(
                f"order not found: {order_or_id!r}", OrderNotFoundWarning)
            return

    def exit_all(self):
        """Exits all trades."""
        for open_trade in self.open_trades[:]:
            self._open_trades.remove(open_trade)
            self._closed_trades.append(open_trade)
            self._asset_balances[open_trade.trading_symbol] += (
                open_trade.value(self.close[0]))

    def exit(
        self,
        order_id: Order | str,
        amount: float | None = None,
        amount_percent: float | None = None,
    ):  # pragma: no cover

        """Exit a trade with the specified ID.

        If there were multiple entry orders with the same ID, all of
        them are exited at once. If there are no open entries with the
        specified ID by the moment the function is called, the function
        will not have any effect.

        The command uses market order. Every entry is closed by a
        separate market order.

        Arguments:
            order_id: Used to identify the orders in the exchange.
            signal_source_symbol: Signal-source symbol of the asset
                where the order is being made on.
            amount: Optional order amount in the exchange currency.
            amount_percent: Optional order amount (in percentage) in the
                exchange currency. This argument takes precedence over
                the `amount` parameter. If both are not provided, the
                order will use the available wallet balance as basis.
        """

        # Make sure there's a position to close to begin with
        position_amount = self.positions[self.trading_symbol]["total_amount"]
        abs_position_amount = abs(position_amount)
        if position_amount == 0:
            return

        # Make sure amount percent is between 1 and 100 (inclusive)
        if isinstance(amount_percent, (float, int)):
            if not(1 <= amount_percent <= 100):
                raise ValueError(f"amount_percent must be between 1 and 100")
        elif amount_percent is not None:
            raise ValueError(f"invalid amount_percent value: {amount_percent}")

        # Make sure amount is a positive number if given
        if amount_percent is None and isinstance(amount, (float, int)):
            if amount <= 0:
                raise ValueError(f"amount must be a positive number: {amount}")
        elif amount_percent is None and amount is not None:
            raise ValueError(f"invalid amount value: {amount}")

        # Automatically determine the actual order amount
        if amount_percent:
            amount = abs_position_amount * (float(amount_percent) / 100.0)
        elif amount:
            amount = float(amount)
        else:
            amount = abs_position_amount

        # Make sure we still have enough balance in the exchange for the
        # specified order amount
        if abs(amount) > abs_position_amount:
            raise InsufficientPositionAmountError(
                f"tried to close {amount} {self.currency} with "
                f"{position_amount} {self.currency} position")

        for open_trade in self.open_trades[:]:
            if open_trade.id == order_id:
                self._open_trades.remove(open_trade)
                self._closed_trades.append(open_trade)
                self._asset_balances[open_trade.trading_symbol] += (
                    open_trade.value(self.close[0]))

    def _fetch_ohlcv(self) -> dict[str, pd.DataFrame]:
        """Needs improvement: Currently just using Datasets Core."""

        ohlcvs = {}

        for asset in self.bt.config.assets:
            # Create a dynamic starting datetime based on the assumption
            # the max strategy parameter is the minimum indicator period
            diff = tdc.Timeframe(asset.signal_timeframe).to_timedelta()
            diff *= self.bt.minimum_indicator_period
            start = self.bt.config.starting_timestamp
            start = tdc.utils.datetime_utils.to_datetime(start) - diff

            exchange = tdc.exchange.get(asset.signal_source_exchange)
            ohlcv = pd.DataFrame(exchange.fetch_ohlcv(
                symbol=asset.signal_source_symbol,
                timeframe=asset.signal_timeframe,
                end=self.bt.config.ending_timestamp,
                start=start,
            ))

            # Preprocess the columns and index of the dataframe return
            ohlcv.columns = [
                "datetime", "open", "high", "low", "close", "volume"
            ]

            ohlcv["datetime"] = pd.to_datetime(
                ohlcv["datetime"], unit="ms", utc=True)

            ohlcv.set_index("datetime", inplace=True)
            ohlcv.sort_index(inplace=True)

            ohlcvs[asset.signal_source_symbol] = ohlcv

        return ohlcvs

    def _update_equity(self):
        """Updates the equity variable of the exchange."""

        # Add the current timestamp to equity and set it to
        # The current wallet balance for that asset
        timestamp = self.datetime[0]
        self._equity[self.trading_symbol][timestamp] = (
            self.asset_balances[self.trading_symbol])

        # Add pending order values into the equity
        for pending_order in self.pending_orders:
            if pending_order.trading_symbol != self.trading_symbol:
                continue  # pragma: no cover

            self._equity[pending_order.trading_symbol][timestamp] += (
                pending_order.value(self.close[0]))

        # Add existing positions to equity
        position_average_price = self.positions[self.trading_symbol]["price"]
        position_average_price = position_average_price or self.close[0]
        total_amount = self.positions[self.trading_symbol]["total_amount"]

        if self.positions[self.trading_symbol]["position_amount"] < 0:
            amount_multiplier = position_average_price / self.close[0]
        else:
            amount_multiplier = self.close[0] / position_average_price

        self._equity[self.trading_symbol][timestamp] += (
            amount_multiplier * total_amount)

    @staticmethod
    def _get_average_price(
        old_price: float,
        old_amount: float,
        new_price: float,
        new_amount: float,
    ):
        """Returns the average price given the prices and amounts."""
        total_amount = old_amount + new_amount
        return float(
            (old_amount * old_price) + (new_amount * new_price)) / total_amount

    @property
    def asset_balances(self) -> dict:
        return self._asset_balances

    @property
    def backtester(self) -> Backtester:
        return self._backtester

    @property
    def bt(self) -> Backtester:
        return self._backtester

    @property
    def cancelled_orders(self) -> list[Order]:
        return self._cancelled_orders

    @property
    def closed_trades(self) -> dict[str, Order]:
        return self._closed_trades

    @property
    def data(self) -> dict[str, pd.DataFrame]:
        return self._data

    @property
    def currency(self) -> str:
        return self._currency

    @property
    def equity(self) -> dict[str, dict[str, float]]:
        return self._equity

    @property
    def initial_balance(self) -> float:
        return self._initial_balance

    @property
    def open_trades(self) -> dict[str, Order]:
        return self._open_trades

    @property
    def pending_orders(self) -> dict[str, Order]:
        return self._pending_orders

    @property
    def positions(self) -> dict[str, dict[str, float]]:
        result = {
            asset.trading_symbol: {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            }
            for asset in self.bt.config.assets
        }

        for open_trade in self.open_trades:
            if result[open_trade.trading_symbol]["price"] is None:
                result[open_trade.trading_symbol]["price"] = float(
                    open_trade.limit)
                result[open_trade.trading_symbol]["total_amount"] = (
                    open_trade.amount)
                result[open_trade.trading_symbol]["position_amount"] = (
                    open_trade.position_amount)

            else:
                result[open_trade.trading_symbol]["price"] = (
                    self._get_average_price(
                        result[open_trade.trading_symbol]["price"],
                        result[open_trade.trading_symbol]["position_amount"],
                        open_trade.limit,
                        open_trade.position_amount))

                result[open_trade.trading_symbol]["total_amount"] += (
                    open_trade.amount)

                result[open_trade.trading_symbol]["position_amount"] += (
                    open_trade.position_amount)

        return result

    @property
    def wallet_balance(self) -> float:
        return sum([
            self.asset_balances[asset.trading_symbol]
            for asset in self.bt.config.assets
        ])
