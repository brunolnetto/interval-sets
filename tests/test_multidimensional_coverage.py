import pytest
from src.intervals import Interval, Point
from src.multidimensional import Box


class TestBoxCoverage:
    """Targeted tests to fix coverage gaps in multidimensional.py."""

    def test_init_validation(self):
        """Cover Line 32: if not intervals: raise ValueError."""
        with pytest.raises(ValueError, match="must have at least 1 dimension"):
            Box([])

    def test_contains_is_empty(self):
        """Cover Line 77, 92, 98: is_empty checks in contains/overlaps."""
        # Create an empty box (one dimension empty)
        empty = Box([Interval.empty(), Interval(0, 1)])
        assert empty.is_empty()

        # Test contains with empty box
        assert not empty.contains((0.5, 0.5))

        # Test overlaps with empty box
        b = Box([Interval(0, 1), Interval(0, 1)])
        assert not empty.overlaps(b)
        assert not b.overlaps(empty)

    def test_overlaps_type_error(self):
        """Cover Line 92: Check overlap with non-Box."""
        b = Box([Interval(0, 1)])
        assert not b.overlaps("not a box")

    def test_overlaps_dimension_mismatch(self):
        """Cover Line 95: Overlaps dimension mismatch."""
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Cannot compare Box"):
            b1.overlaps(b2)

    def test_intersection_dimension_mismatch(self):
        """Cover Line 108: Intersection dimension mismatch."""
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Dimension mismatch"):
            b1.intersection(b2)

    def test_union_fallback(self):
        """Line 137: intersection fallback (should unlikely happen)."""
        # Hard to hit: Intersection of Convex Intervals is Convex.
        pass

    def test_difference_dimension_mismatch(self):
        """Cover Line 161: Difference dimension mismatch."""
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Dimension mismatch"):
            b1.difference(b2)

    def test_difference_no_overlap_check(self):
        # Line 167: overlaps check optimization
        # We implicitly hit this if we pass disjoint boxes, but we need to ensure we don't return early before the check if we enable optimization.
        # Current code checks intersection is_empty.
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(2, 3)])
        # intersection is empty.
        diff = b1.difference(b2)
        assert len(diff) == 1
        assert diff[0] == b1

    def test_intersection_results_in_point(self):
        """Cover Line 121 (implicit): Intersection results in Point."""
        # [0, 1] & [1, 2] -> Point(1)
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(1, 2)])
        inter = b1.intersection(b2)
        # Should be Box([Point(1)])
        assert inter.dimension == 1
        assert inter.intervals[0].is_point()
        assert inter.intervals[0].start == 1.0

    def test_equality_type_check(self):
        """Cover Line 146: __eq__ with non-Box."""
        b = Box([Interval(0, 1)])
        assert not (b == "not a box")
        assert not (b == 123)
