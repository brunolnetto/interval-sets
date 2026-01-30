import pytest
from src.intervals import Interval
from src.multidimensional import Box, BoxSet


class TestBoxCoverage:
    def test_init_validation(self):
        with pytest.raises(ValueError, match="Box must have at least 1 dimension"):
            Box([])
        with pytest.raises(TypeError, match="All elements must be Interval objects"):
            Box(["not an interval"])  # type: ignore

    def test_box_contains_is_empty(self):
        empty = Box.empty(2)
        assert not empty.contains((0.5, 0.5))
        assert not empty.overlaps(Box([Interval(0, 1), Interval(0, 1)]))

    def test_box_overlaps_type_error(self):
        b = Box([Interval(0, 1)])
        assert not b.overlaps("not a box")

    def test_box_overlaps_dimension_mismatch(self):
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Cannot compare Box"):
            b1.overlaps(b2)

    def test_box_intersection_dimension_mismatch(self):
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Dimension mismatch"):
            b1.intersection(b2)

    def test_box_intersection_weird_return(self):
        class MockResult:
            def is_empty(self):
                return False

        class BadInterval(Interval):
            def __init__(self):
                self._start = 0
                self._end = 1
                self._open_start = False
                self._open_end = False

            def is_empty(self):
                return False

            def intersection(self, other):
                return MockResult()

        b_bad = Box.empty(1)
        b_bad._intervals = (BadInterval(),)  # type: ignore
        b_normal = Box([Interval(0, 1)])
        res = b_bad.intersection(b_normal)
        assert res.is_empty()

    def test_box_difference_dimension_mismatch(self):
        b1 = Box([Interval(0, 1)])
        b2 = Box([Interval(0, 1), Interval(0, 1)])
        with pytest.raises(ValueError, match="Dimension mismatch"):
            b1.difference(b2)

    def test_boxset_convex_hull_no_dimension(self):
        # Line 632: dimension is None but list has boxes?
        # (Technically impossible with current add() but good for coverage)
        s = BoxSet()
        s._dimension = None
        s._boxes = [Box([Interval(0, 1)])]
        # Should return Box.empty(1)
        assert s.convex_hull().is_empty()

    def test_boxset_connected_components_no_dimension(self):
        # Line 870: dimension is None
        s = BoxSet()
        s._dimension = None
        s._boxes = [Box([Interval(0, 1)])]
        assert s.connected_components() == []

    def test_box_contains_boxset(self):
        # Line 185: isinstance(item, BoxSet)
        b = Box([Interval(0, 10), Interval(0, 10)])
        s = BoxSet([Box([Interval(2, 4), Interval(2, 4)])])
        assert b.contains(s)

        s2 = BoxSet([Box([Interval(2, 12), Interval(2, 4)])])
        assert not b.contains(s2)

    def test_boxset_lebesgue_measure(self):
        # Line 497
        s = BoxSet([Box([Interval(0, 1)])])
        assert s.lebesgue_measure() == 1.0
        assert s.is_measurable() is True
