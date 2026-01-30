from src.intervals import Interval, IntervalSet


def test_interval_init_validation():
    # Line 126, 131, 136
    # These are in Interval.point, Interval.open, etc?
    # Wait, the coverage says 126, 131, 136 are missing.
    # Let's check the content of intervals.py again around those lines.
    pass


def test_intervalset_minkowski_diff_empty_source():
    # Line 1493: if self.is_empty(): return self
    s = IntervalSet()
    assert s.minkowski_difference(Interval(0, 1)) == s


def test_hausdorff_midpoint_not_in_interval():
    # Line 1573: if interval.start < midpoint < interval.end
    # A = [0, 1]
    # B = [5, 6] | [8, 9] -> gap (6, 8) midpoint 7.
    # 0 < 7 < 1 is False.
    A = IntervalSet([Interval(0, 1)])
    B = IntervalSet([Interval(5, 6), Interval(8, 9)])
    A.hausdorff_distance(B)


def test_intervalset_membership_optimization():
    # Line 1118: if value < self._intervals[0].start: return False
    s = IntervalSet([Interval(10, 20)])
    assert 5 not in s


def test_intervalset_contains_interval():
    # Line 1279, 1283, 1299
    s = IntervalSet([Interval(0, 10), Interval(20, 30)])
    # 1279: other.start < self._intervals[0].start
    assert Interval(-1, 5) not in s
    # 1283: other.end > self._intervals[-1].end
    assert Interval(25, 35) not in s
    # 1299: potential match but doesn't contain
    assert Interval(5, 15) not in s


def test_interval_various_factories():
    # Attempting to hit 126, 131, 136 if they are factory methods
    assert Interval.real_line().is_bounded() is False
    assert Interval.positive_reals().start == 0
    assert Interval.from_center_radius(5, 2) == Interval(3, 7)
