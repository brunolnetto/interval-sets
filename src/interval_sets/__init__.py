"""
Interval Arithmetic Library

A Python library for working with intervals and points on the real number line.
Supports continuous intervals with open/closed boundaries and disjoint interval collections.
"""

from .intervals import Interval, IntervalSet
from .multidimensional import Box, BoxSet
from .errors import (
    IntervalError,
    InvalidIntervalError,
    OverlappingIntervalError,
    point_error,
    continuous_interval_error,
)
from .utils import Config, config

__all__ = [
    # Core classes
    "Interval",
    "IntervalSet",
    "Box",
    "BoxSet",
    # Exceptions
    "IntervalError",
    "InvalidIntervalError",
    "OverlappingIntervalError",
    # Error functions
    "point_error",
    "continuous_interval_error",
    # Configuration
    "Config",
    "config",
]
