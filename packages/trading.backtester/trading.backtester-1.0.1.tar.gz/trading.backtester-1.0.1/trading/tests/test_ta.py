"""Tests for trading.backtester.ta."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import numpy as np

from trading.backtester import ta


class TestBacktesterTA:

    def test_crossover(self):
        assert ta.crossover((2, 1), [1, 3])
        assert ta.crossover([10, 6, 5, 5], [7, 8, 5, 2])
        assert ta.crossover(np.asarray([19, 7, 7, 8]), (9, 8, 7, 5))

    def test_crossunder(self):
        assert ta.crossunder([1, 2], [3, 1])
        assert ta.crossunder([7, 8, 5, 2], (10, 6, 5, 5))
        assert ta.crossunder(np.asarray([9, 11, 7, 5]), [19, 8, 7, 8])
