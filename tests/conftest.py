"""Pytest configuration and shared fixtures for interval arithmetic tests."""

import pytest
from src.intervals import Interval, IntervalSet


@pytest.fixture
def work_day():
    """A work day interval (9 AM to 5 PM)."""
    return Interval(9, 17)


@pytest.fixture
def meetings():
    """A collection of meeting times."""
    return IntervalSet(
        [
            Interval(9, 10),  # 9-10 AM
            Interval(11, 12.5),  # 11 AM-12:30 PM
            Interval(14, 16),  # 2-4 PM
        ]
    )


@pytest.fixture
def data_ranges():
    """Data coverage ranges with gaps."""
    return IntervalSet([Interval(0, 1000), Interval(1500, 2500), Interval(2800, 4000)])


@pytest.fixture(scope="module")
def small_interval():
    """A small interval [0, 5]."""
    return Interval(0, 5)
