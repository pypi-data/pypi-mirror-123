"""Tests for trading.backtester.exchange."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from collections import namedtuple

import pandas as pd
import pytest

from trading.backtester.order import LIMIT
from trading.backtester.order import MARKET
from trading.backtester.order import STOP_LIMIT
from trading.backtester.order import STOP_MARKET

from trading.backtester.position import LONG
from trading.backtester.position import SHORT

from trading.backtester.backtester import Backtester
from trading.backtester.config import BacktesterConfig
from trading.backtester.errors import InsufficientBalanceError
from trading.backtester.exchange import BacktesterExchange


INPUT_BACKTESTER_CONFIG = {
    "strategy_parameters": {
        "time_period": 34,
        "multiplier": 1.5
    },
    "initial_balance": 53.0091,
    "initial_balance_currency": "USD",
    "trading_exchange": "bitmex",
    "starting_timestamp": "2020-01-01 00:00:00",
    "ending_timestamp": "2021-01-01 00:00:00",
    "assets": [
        {
            "trading_symbol": "ADAUSD",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ADA/USDT",
            "signal_timeframe": "4h",
            "percent_allocation": 45,
        },
        {
            "trading_symbol": "ETHUSD",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "ETH/USDT",
            "signal_timeframe": "4h",
            "percent_allocation": 55,
        }
    ]
}


@pytest.fixture(name="backtester", scope="class")
def fixture_backtester():
    config = BacktesterConfig.from_dict(INPUT_BACKTESTER_CONFIG)

    Backtester = namedtuple(
        "Backtester", ("config", "minimum_indicator_period"))

    return Backtester(config=config, minimum_indicator_period=200)


class TestBacktesterExchange:

    def test_required_backtester_properties(self, backtester):
        """Required for class tests that need the Backtester class."""
        for mock_property in backtester._fields:
            assert mock_property in dir(Backtester)

    def test_initialization(self, backtester):
        exchange = BacktesterExchange(backtester)
        assert isinstance(exchange, BacktesterExchange)

    def test_successful_order_creation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        # Make sure the wallet balance is 10000 before any orders
        assert len(exchange.pending_orders) == 0
        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=1000)
        assert order_1.type == MARKET
        assert len(exchange.pending_orders) == 1
        assert exchange.wallet_balance == 9000
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG, limit=1234)
        assert order_2.type == LIMIT
        assert len(exchange.pending_orders) == 2
        assert exchange.wallet_balance == 4500
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        order_3 = exchange.order("test-order_ada", LONG, amount=1000, stop=12)
        assert order_3.type == STOP_MARKET
        assert len(exchange.pending_orders) == 3
        assert exchange.wallet_balance == 3500
        assert exchange.pending_orders[2] == order_3
        assert exchange.pending_orders[2].id == order_3.id

        order_4 = exchange.order("test-order_ada_3", LONG, amount_percent=50)
        assert order_4.type == MARKET
        assert len(exchange.pending_orders) == 4
        assert exchange.wallet_balance == 1750
        assert exchange.pending_orders[3] == order_4
        assert exchange.pending_orders[3].id == order_4.id

        order_5 = exchange.order("test-order_ada", LONG, stop=124, limit=123)
        assert order_5.type == STOP_LIMIT
        assert len(exchange.pending_orders) == 5
        assert exchange.wallet_balance == 0
        assert exchange.pending_orders[4] == order_5
        assert exchange.pending_orders[4].id == order_5.id

    def test_unsuccessful_order_creation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester, initial_balance=9)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        # Unknown position value
        with pytest.raises(ValueError):
            exchange.order("id", "unknown_position")

        with pytest.raises(InsufficientBalanceError):
            exchange.order("id", "long", amount=100)

        # Amount percent is not between 100
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount_percent=-1)

        # Amount percent is not between 100
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount_percent=101)

        # Amount percent is invalid
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount_percent=[1])

        # Amount is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount=-10)

        # Amount is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount=0)

        # Amount is invalid
        with pytest.raises(ValueError):
            exchange.order("id", "long", amount=[1])

        # Price is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", limit=-10)

        # Price is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", limit=0)

        # Invalid price type
        with pytest.raises(ValueError):
            exchange.order("id", "long", limit=[1])

        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        # stop is negative, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", stop=-10)

        # stop is zero, should be positive
        with pytest.raises(ValueError):
            exchange.order("id", "long", stop=0)

        # Invalid stop type
        with pytest.raises(ValueError):
            exchange.order("id", "long", stop=[1])

    def test_successful_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.cancel(order_1)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 1
        assert exchange.pending_orders[0] == order_2
        assert exchange.pending_orders[0].id == order_2.id

        exchange.cancel("test-order-2")
        assert len(exchange.pending_orders) == 0
        assert len(exchange.cancelled_orders) == 2

    def test_unsuccessful_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        with pytest.warns(None) as record:
            exchange.cancel("some-unknown-order-id")

        assert len(record) == 1

        with pytest.warns(None) as record:
            exchange.cancel([1, 2, 3])

        assert len(record) == 1

        order = exchange.order("test-order-2", LONG)
        with pytest.warns(None) as record:
            exchange.cancel("different-id")

        assert len(record) == 1

    def test_all_order_cancellation(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        exchange.cancel_all()
        assert len(exchange.pending_orders) == 0
        assert len(exchange.cancelled_orders) == 2

    def test_successful_order_exit(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        assert exchange.wallet_balance == 10000

        exchange.exit("test-order")

        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        # Force buy to avoid dependency on nextstop or next start
        order_1.execution_timestamp = "2021-10-19 00:00:00"
        order_2.execution_timestamp = "2021-10-19 00:00:00"
        order_1.limit = 1.23
        order_2.limit = 3020
        exchange._open_trades.append(order_1)
        exchange._open_trades.append(order_2)
        exchange._positions = {
            "ADAUSD": {
                "price": 1.23,
                "total_amount": 3000.0,
                "position_amount": 3000.0,
            },
            "ETHUSD": {
                "price": 3020,
                "total_amount": 5500.0,
                "position_amount": 5500.0,
            }
        }

        assert len(exchange.open_trades) == 2
        assert len(exchange.closed_trades) == 0
        assert exchange.wallet_balance == 1500

        exchange.close = [1.35]
        exchange.exit("test-order")

        assert len(exchange.open_trades) == 1
        assert len(exchange.closed_trades) == 1

        exchange.exit("test-order-2")

        assert len(exchange.open_trades) == 0
        assert len(exchange.closed_trades) == 2

    def test_unsuccessful_order_exit(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

    def test_order_exit_all(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"
        exchange.datetime = ["2021-10-18 00:00:00"]

        assert exchange.wallet_balance == 10000

        exchange.exit("test-order")

        assert exchange.wallet_balance == 10000

        order_1 = exchange.order("test-order", LONG, amount=3000)
        assert len(exchange.pending_orders) == 1
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[0] == order_1
        assert exchange.pending_orders[0].id == order_1.id

        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order_2 = exchange.order("test-order-2", LONG)
        assert len(exchange.pending_orders) == 2
        assert len(exchange.cancelled_orders) == 0
        assert exchange.pending_orders[1] == order_2
        assert exchange.pending_orders[1].id == order_2.id

        # Force buy to avoid dependency on nextstop or next start
        order_1.execution_timestamp = "2021-10-19 00:00:00"
        order_2.execution_timestamp = "2021-10-19 00:00:00"
        order_1.limit = 1.23
        order_2.limit = 3020
        exchange._open_trades.append(order_1)
        exchange._open_trades.append(order_2)
        exchange._positions = {
            "ADAUSD": {
                "price": 1.23,
                "total_amount": 3000.0,
                "position_amount": 3000.0,
            },
            "ETHUSD": {
                "price": 3020,
                "total_amount": 5500.0,
                "position_amount": 5500.0,
            }
        }

        assert len(exchange.open_trades) == 2
        assert len(exchange.closed_trades) == 0
        assert exchange.wallet_balance == 1500

        exchange.close = [1.35]
        exchange.exit_all()

        assert len(exchange.open_trades) == 0
        assert len(exchange.closed_trades) == 2

    def test_exchange_nextstop_function(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [3412.00, 3403.69]
        exchange.high = [3613.00, 3546.76]
        exchange.close = [3607.27, 3491.63]
        exchange.datetime = ["2021-10-13 00:00:00", "2021-10-12 00:00:00"]
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order = exchange.order("test-order", LONG, amount=3000, limit=3700)
        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 4500.0, "ETHUSD": 2500.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            }
        }

        assert exchange.equity == {
            "ADAUSD": {},
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
            },
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [3587.79, 3412.00]
        exchange.high = [3824.74, 3613.00]
        exchange.close = [3791.42, 3607.27]
        exchange.datetime = ["2021-10-14 00:00:00", "2021-10-13 00:00:00"]
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        assert len(exchange.pending_orders) == 1
        assert len(exchange.open_trades) == 0

        order = exchange.order("test-order", LONG, amount=500)

        assert len(exchange.pending_orders) == 2
        assert len(exchange.open_trades) == 0

        exchange.nextstop()

        assert len(exchange.pending_orders) == 0
        assert len(exchange.open_trades) == 2

        assert exchange.asset_balances == {"ADAUSD": 4500.0, "ETHUSD": 2000.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": 3713.06,
                "total_amount": 3500.0,
                "position_amount": 3500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {},
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [3735.24, 3587.79]
        exchange.high = [3904.00, 3824.74]
        exchange.close = [3868.28, 3791.42]
        exchange.datetime = ["2021-10-15 00:00:00", "2021-10-14 00:00:00"]
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 4500.0, "ETHUSD": 2000.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": 3713.06,
                "total_amount": 3500.0,
                "position_amount": 3500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {},
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [3804.67, 3735.24]
        exchange.high = [3969.70, 3904.00]
        exchange.close = [3830.61, 3868.28]
        exchange.datetime = ["2021-10-16 00:00:00", "2021-10-15 00:00:00"]
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order = exchange.order("test-order", SHORT, amount=500)
        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 4500.0, "ETHUSD": 1500.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": 3693.4683333333332,
                "total_amount": 4000.0,
                "position_amount": 3000.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {},
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
                "2021-10-16 00:00:00": 5648.523451985735,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [3759.11, 3804.67]
        exchange.high = [3900.91, 3969.70]
        exchange.close = [3770.16, 3830.61]
        exchange.datetime = ["2021-10-17 00:00:00", "2021-10-16 00:00:00"]
        exchange.trading_symbol = "ETHUSD"
        exchange.signal_source_symbol = "ETH/USDT"

        order = exchange.order("test-order", SHORT, amount_percent=100)
        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 4500.0, "ETHUSD": 0.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": 3616.7766666666666,
                "total_amount": 5500.0,
                "position_amount": 1500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {},
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
                "2021-10-16 00:00:00": 5648.523451985735,
                "2021-10-17 00:00:00": 5733.248666169599,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [2.071, 2.107]
        exchange.high = [2.173, 2.250]
        exchange.close = [2.118, 2.171]
        exchange.datetime = ["2021-10-12 00:00:00", "2021-10-11 00:00:00"]
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        order = exchange.order("test-order", SHORT, stop=2.2, amount_percent=60)
        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 1800.0, "ETHUSD": 0.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": 3616.7766666666666,
                "total_amount": 5500.0,
                "position_amount": 1500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {
                "2021-10-12 00:00:00": 4500.0,
            },
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
                "2021-10-16 00:00:00": 5648.523451985735,
                "2021-10-17 00:00:00": 5733.248666169599,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [2.078, 2.071]
        exchange.high = [2.200, 2.173]
        exchange.close = [2.190, 2.118]
        exchange.datetime = ["2021-10-13 00:00:00", "2021-10-12 00:00:00"]
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 1800.0, "ETHUSD": 0.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": 2.19,
                "total_amount": 2700.0,
                "position_amount": -2700.0,
            },
            "ETHUSD": {
                "price": 3616.7766666666666,
                "total_amount": 5500.0,
                "position_amount": 1500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {
                "2021-10-12 00:00:00": 4500.0,
                "2021-10-13 00:00:00": 4500.0,
            },
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
                "2021-10-16 00:00:00": 5648.523451985735,
                "2021-10-17 00:00:00": 5733.248666169599,
            }
        }

        # Simulate backtester data: add low, high, close, datetime
        # trading_symbol, and trading_signal_source property to exchange
        exchange.low = [2.155, 2.078]
        exchange.high = [2.225, 2.200]
        exchange.close = [2.172, 2.190]
        exchange.datetime = ["2021-10-14 00:00:00", "2021-10-13 00:00:00"]
        exchange.trading_symbol = "ADAUSD"
        exchange.signal_source_symbol = "ADA/USDT"

        exchange.nextstop()

        assert exchange.asset_balances == {"ADAUSD": 1800.0, "ETHUSD": 0.0}
        assert exchange.positions == {
            "ADAUSD": {
                "price": 2.19,
                "total_amount": 2700.0,
                "position_amount": -2700.0,
            },
            "ETHUSD": {
                "price": 3616.7766666666666,
                "total_amount": 5500.0,
                "position_amount": 1500.0,
            }
        }
        assert exchange.equity == {
            "ADAUSD": {
                "2021-10-12 00:00:00": 4500.0,
                "2021-10-13 00:00:00": 4500.0,
                "2021-10-14 00:00:00": 4522.375690607734,
            },
            "ETHUSD": {
                "2021-10-13 00:00:00": 5500.0,
                "2021-10-14 00:00:00": 5573.863605759131,
                "2021-10-15 00:00:00": 5646.313283383517,
                "2021-10-16 00:00:00": 5648.523451985735,
                "2021-10-17 00:00:00": 5733.248666169599,
            }
        }

    def test_exchange_properties(self, backtester):
        exchange = BacktesterExchange(backtester=backtester)
        assert isinstance(exchange.data["ADA/USDT"], pd.DataFrame)
        assert exchange.initial_balance == 10000
        assert exchange.wallet_balance == 10000
        assert exchange.asset_balances["ADAUSD"] == 4500
        assert exchange.asset_balances["ETHUSD"] == 5500
        assert exchange.currency == "USD"
        assert exchange.equity["ADAUSD"] == {}
        assert exchange.equity["ETHUSD"] == {}
        assert exchange.pending_orders == []
        assert exchange.positions == {
            "ADAUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            },
            "ETHUSD": {
                "price": None,
                "total_amount": 0,
                "position_amount": 0,
            }
        }
        assert exchange.open_trades == []
        assert exchange.cancelled_orders == []
        assert exchange.closed_trades == []
