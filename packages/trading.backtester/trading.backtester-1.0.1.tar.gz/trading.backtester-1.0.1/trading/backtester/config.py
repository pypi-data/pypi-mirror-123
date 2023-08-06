"""Module containing the configuration data class for the backtester."""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dtlib
import json as jsonlib

from dateutil import parser
import pytz


__all__ = [
    # Class exports
    "AssetConfig",
    "AttrDict",
    "BacktesterConfig",
]


class AttrDict(dict):
    """Attribute-only access dictionary class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self


@dataclass
class AssetConfig:
    """Asset-level configuration. Always an element of a list.

    Configurable Parameters:
        trading_symbol: String symbol of the crypto asset in the
            trading exchange.
        trading_timeframe: Execution timeframe of an asset.
        signal_source_exchange: String symbol of the crypto asset
            in the signal source exchange.
        signal_source_symbol: Name of the exchange where the backtester
            will fetch the OHLCV data from.
        signal_timeframe: The signal timeframe of an asset.
        percent_allocation: The percent allocation of an asset. The
            total of all the `percent_allocation` values must be equal
            to 100.
    """
    trading_symbol: str
    trading_timeframe: str
    signal_source_exchange: str
    signal_source_symbol: str
    signal_timeframe: str
    percent_allocation: float


@dataclass
class BacktesterConfig:
    """Class representation of a backtester configuration.

    Configurable Parameters:
        strategy_parameters: A dictionary containing the different
            strategy parameters that modify the behavior of a strategy:

            ```python
            # Example parameters of a EMA-based Golden Cross strategy
            "strategy_parameters": {
                "fast_ema_period": 50,
                "slow_ema_period": 200,
            }
            ```
        initial_balance: Sets the initial balance of the backtester.
        initial_balance_currency: Currency unit of the initial balance.
        trading_exchange: Name of the exchange where the backtester will
            simulate the trades of the strategy.
        starting_timestamp: The starting time of the backtester run.
        ending_timestamp: The ending time of the backtester run.
        assets: A list of dictionaries containing the different
            asset configurations:

            ```python
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
            ```

            See the documentation for `AssetConfig` for an explanation
            of what the different configuration keys are for.
    """
    strategy_parameters: AttrDict
    initial_balance: float
    initial_balance_currency: str
    trading_exchange: str
    starting_timestamp: str
    ending_timestamp: str
    assets: list[AssetConfig]

    @classmethod
    def load(
        cls,
        input_config: str | dict | BacktesterConfig,
    ) -> BacktesterConfig:

        """Auto-detection and dynamic loading of configuration.

        See the documentation for `BacktesterConfig` for an explanation
        of what the required configuration structure is.

        Raises:
            ValueError: Raised if the input is a string but evaluated
                as an invalid JSON.
            ValueError: Raised if the input configuration has missing
                dictionary keys, has an invalid value (for example the
                ending timestamp is older than the starting timestamp),
                or if extra unrecognized parameter keys is found in the
                input configuration.
            TypeError: Raised if any of configuration values has the
                incorrect data type.

        Return:
            The parsed configuration as a `BacktesterConfig` instance.
        """

        # Instance is already a BacktesterConfig instance, just return
        if isinstance(input_config, BacktesterConfig):
            return input_config

        # Try to parse configuration as JSON if its a string
        if isinstance(input_config, str):
            try:
                return cls.from_json(input_config)

            # Make the JSON exception message clearer
            except jsonlib.decoder.JSONDecodeError as error:
                raise ValueError(
                    f"invalid JSON configuration: {input_config}") from error

        return cls.from_dict(input_config)

    @classmethod
    def from_json(cls, input_config: str) -> BacktesterConfig:
        """Parse an JSON string into a backtester config instance.

        See the documentation for `BacktesterConfig` for an explanation
        of what the required configuration structure is.

        Raises:
            ValueError: Raised if the input configuration has missing
                dictionary keys, has an invalid value (for example the
                ending timestamp is older than the starting timestamp),
                or if extra unrecognized parameter keys is found in the
                input configuration.
            TypeError: Raised if any of configuration values has the
                incorrect data type.

        Return:
            The parsed configuration as a `BacktesterConfig` instance.
        """
        return cls.from_dict(jsonlib.loads(input_config))

    @classmethod
    def from_dict(cls, input_config: dict) -> BacktesterConfig:
        """Parse an object into a backtester config instance.

        This should be the main entry point of any configuration
        parsing. If we need to enable JSON or other configuration
        formats, we need to convert them first into Python's dictionary
        object and pass it to this function:

        ```python
        # Use a JSON string as an input configuration
        Backtester.from_dict(convert_json_to_dict(input_json_config))

        # Use a YAML string as an input configuration
        Backtester.from_dict(convert_yaml_to_dict(input_yaml_config))

        # Use an INI string as an input configuration
        Backtester.from_dict(convert_ini_to_dict(input_yaml_config))
        ```

        Raises:
            ValueError: Raised if the input configuration has missing
                dictionary keys, has an invalid value (for example the
                ending timestamp is older than the starting timestamp),
                or if extra unrecognized parameter keys is found in the
                input configuration.
            TypeError: Raised if any of configuration values has the
                incorrect data type.

        Return:
            The parsed configuration as a `BacktesterConfig` instance.
        """
        cls._validate_before_parsing(input_config)

        # Second-level configuration parsing
        parsed_assets = [AssetConfig(**a) for a in input_config["assets"]]
        parsed_strategy_parameters = AttrDict(
            input_config["strategy_parameters"])

        # Root-level configuration parsing
        semi_parsed_config = input_config.copy()
        semi_parsed_config.update({
            "strategy_parameters": parsed_strategy_parameters,
            "assets": parsed_assets,
        })

        # Store raw configuration as well
        parsed_config = cls(**semi_parsed_config)
        parsed_config.raw = input_config

        # Run validation against the parsed configuration. The first
        # part of the `from_dict` function already does the initial
        # validation of possibly missing dictionary keys. At this point
        # we're already sure that all the expected keys are present.
        parsed_config._validate_after_parsing()

        return parsed_config

    @staticmethod
    def _validate_before_parsing(input_config: dict):
        """Applies validation to the input configuration."""

        # Check if input config is a dictionary
        if not input_config:
            raise ValueError(f"invalid configuration {input_config}")

        # Check if input config is a dictionary
        if not isinstance(input_config, dict):
            raise TypeError(
                "input configuration must be a dictionary, got "
                f"{type(input_config)}")

        # Check if 2nd-level config keys can be found
        for config_key in ["assets", "strategy_parameters"]:
            if config_key not in input_config:
                raise ValueError(
                    f"{config_key} not found in the input configuration")

        # Check if assets configuration is a list
        if not isinstance(input_config["assets"], list):
            raise TypeError(
                "assets configuration must be a list, got "
                f"{type(input_config['assets'])}")

        # Check if strategy parameters configuration is dictionary
        if not isinstance(input_config["strategy_parameters"], dict):
            raise TypeError(
                "strategy parameters configuration must be a dictionary, "
                f"got {type(input_config['strategy_parameters'])}")

        # Check if assets elements are dictionary
        for asset in input_config["assets"]:
            if not isinstance(asset, dict):
                raise TypeError(
                    f"assets element must be a dictionary, got {type(asset)}")

    def _validate_after_parsing(self):
        """Applies validation to the parsed configuration."""

        # Validate strategy time span. End must be older than start.
        start = self._to_utc_datetime(self.starting_timestamp)
        end = self._to_utc_datetime(self.ending_timestamp)

        if start >= end:
            raise ValueError("ending timestamp must be older than the start.")

        # Validate the total allocation of assets. Must be equal to 100%
        total_allocation = sum([
            asset.percent_allocation for asset in self.assets
        ])

        if len(self.assets) != 0 and total_allocation != 100:
            raise ValueError(
                f"total allocation is not equal to 100%: {total_allocation}")

    @staticmethod
    def _to_utc_datetime(input_timestamp: str) -> dtlib.datetime:
        """Convert any timestamp into a UTC datetime."""
        first_day_current_yr = dtlib.datetime(dtlib.datetime.now().year, 1, 1)
        datetime = parser.parse(input_timestamp, default=first_day_current_yr)

        return datetime.replace(tzinfo=datetime.tzinfo or pytz.utc)
