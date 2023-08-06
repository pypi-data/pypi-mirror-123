"""Module containing position constants and classes for the backtester."""

__all__ = [
    # Constants export
    "LONG",
    "SHORT",
    "VALID_POSITION_TYPES",
]


LONG = "long"
SHORT = "short"

# Consolidate into a list of string values that can be used
# for validation of newly created orders
VALID_POSITION_TYPES = (LONG, SHORT)
