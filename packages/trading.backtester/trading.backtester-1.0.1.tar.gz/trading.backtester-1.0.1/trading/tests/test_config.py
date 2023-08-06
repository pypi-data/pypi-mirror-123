"""Tests for trading.backtester.config."""
# pylint: disable=missing-class-docstring,missing-function-docstring

from dataclasses import is_dataclass
import json as jsonlib

import pytest

from trading.backtester.config import BacktesterConfig


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
            "percent_allocation": 9,
        },
        {
            "trading_symbol": "XBTUSD",
            "trading_timeframe": "4h",
            "signal_source_exchange": "binance",
            "signal_source_symbol": "BTCUSDT",
            "signal_timeframe": "4h",
            "percent_allocation": 91,
        }
    ]
}


@pytest.fixture(name="config", scope="class")
def fixture_config():
    return BacktesterConfig.from_dict(INPUT_BACKTESTER_CONFIG)


class TestBacktesterConfig:

    def test_successful_initialization(self, config):
        assert is_dataclass(config)
        assert isinstance(config, BacktesterConfig)

        # Test using load classmethod on a BacktesterConfig instance
        assert isinstance(BacktesterConfig.load(config), BacktesterConfig)

        # Test using load classmethod on a string
        config = BacktesterConfig.load(jsonlib.dumps(INPUT_BACKTESTER_CONFIG))
        assert config.assets[0].trading_symbol == "ADAZ21"
        assert config.starting_timestamp == "2020-01-01 00:00:00"
        assert config.strategy_parameters.time_period == 34

        # Test using load classmethod on an object
        config = BacktesterConfig.load(INPUT_BACKTESTER_CONFIG)
        assert config.assets[0].trading_symbol == "ADAZ21"
        assert config.starting_timestamp == "2020-01-01 00:00:00"
        assert config.initial_balance == 53.0091

        # Test using from_json classmethod on a string
        config = BacktesterConfig.from_json(
            jsonlib.dumps(INPUT_BACKTESTER_CONFIG))
        assert config.assets[0].signal_source_exchange == "binance"
        assert config.ending_timestamp == "2021-01-01 00:00:00"
        assert config.strategy_parameters.multiplier == 1.5

    def test_unsuccessful_initialization(self):
        with pytest.raises(TypeError):
            BacktesterConfig.load(["invalid config"])

        with pytest.raises(ValueError):
            BacktesterConfig.load("invalid JSON")

        with pytest.raises(ValueError):
            BacktesterConfig.load(None)

        # Test an invalid assets configuration type
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config.update({"assets": [1, 2, 3, 4]})
        with pytest.raises(TypeError):
            BacktesterConfig.load(modified_config)

        # Test an invalid assets configuration type
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config.update({"assets": 1234})
        with pytest.raises(TypeError):
            BacktesterConfig.load(modified_config)

        # Test an invalid strategy parameter configuration type
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config.update({"strategy_parameters": [1, 2, 3, 4]})
        with pytest.raises(TypeError):
            BacktesterConfig.load(modified_config)

        # Test config without assets key
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        del modified_config["assets"]
        with pytest.raises(ValueError):
            BacktesterConfig.load(modified_config)

        # Test config without strategy_parameters key
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        del modified_config["strategy_parameters"]
        with pytest.raises(ValueError):
            BacktesterConfig.load(modified_config)

        # Test adding an unknown configuration key
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config.update({"unknown_key": 123})
        with pytest.raises(TypeError):
            BacktesterConfig.load(modified_config)

    def test_root_level_config_values(self, config):
        assert config.initial_balance == 53.0091
        assert config.initial_balance_currency == "BTC"
        assert config.trading_exchange == "bitmex"
        assert config.starting_timestamp == "2020-01-01 00:00:00"
        assert config.ending_timestamp == "2021-01-01 00:00:00"

    def test_strategy_parameter_config_values(self, config):
        assert config.strategy_parameters.multiplier == 1.5
        assert config.strategy_parameters.time_period == 34

    def test_asset_0_config_values(self, config):
        assert config.assets[0].trading_symbol == "ADAZ21"
        assert config.assets[0].trading_timeframe == "4h"
        assert config.assets[0].signal_source_exchange == "binance"
        assert config.assets[0].signal_source_symbol == "ADABTC"
        assert config.assets[0].signal_timeframe == "4h"
        assert config.assets[0].percent_allocation == 9

    def test_asset_1_config_values(self, config):
        assert config.assets[1].trading_symbol == "XBTUSD"
        assert config.assets[1].trading_timeframe == "4h"
        assert config.assets[1].signal_source_exchange == "binance"
        assert config.assets[1].signal_source_symbol == "BTCUSDT"
        assert config.assets[1].signal_timeframe == "4h"
        assert config.assets[1].percent_allocation == 91

    def test_100_percent_total_allocation(self, config):
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config["assets"][0]["percent_allocation"] = 0
        with pytest.raises(ValueError):
            BacktesterConfig.load(modified_config)

    def test_start_older_or_equal_to_end(self, config):
        modified_config = INPUT_BACKTESTER_CONFIG.copy()
        modified_config["starting_timestamp"] = "2021-01-01 00:00:00"
        modified_config["ending_timestamp"] = "2020-01-01 00:00:00"
        with pytest.raises(ValueError):
            BacktesterConfig.load(modified_config)

    def test_raw_property(self, config):
        assert config.raw == INPUT_BACKTESTER_CONFIG
