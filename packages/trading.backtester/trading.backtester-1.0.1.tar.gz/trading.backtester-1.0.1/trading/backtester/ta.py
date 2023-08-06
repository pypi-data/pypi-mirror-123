"""Module containing technical analysis functions for the backtester."""

from typing import Sequence

import talib


__all__ = [
    # Function exports
    "crossover",
    "crossunder",
]


def crossover(x: Sequence[float], y: Sequence[float]) -> bool:
    return x[0] > y[0] and x[1] < y[1]


def crossunder(x: Sequence[float], y: Sequence[float]) -> bool:
    return x[0] < y[0] and x[1] > y[1]


# Dynamic export of TA-lib functions
for function_name in dir(talib):
    if function_name.isupper() and "_" not in function_name:
        globals()[function_name.lower()] = getattr(talib, function_name)
        __all__.append(function_name.lower())
