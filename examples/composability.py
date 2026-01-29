"""
Composability Demo: Intervals, Points, Boxes, and Regions.

This script demonstrates how the different geometric primitives compose
to represent complex N-dimensional concepts.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.intervals import Interval, Point, IntervalSet
from src.multidimensional import Box, Set


def section(title):
    print(f"\n{'='*10} {title} {'='*10}")


def demo_points_as_intervals():
    section("1. Points are 1st-Class Intervals")

    # A Box is defined by Intervals. Since Point is an Interval,
    # we can create an N-dimensional Point using strict composition.
    p_x = Point(5)
    p_y = Point(10)

    # 2D Point at (5, 10)
    point_2d = Box([p_x, p_y])

    print(f"2D Point Box: {point_2d}")
    print(f"Volume: {point_2d.volume()}")
    print(f"Contains (5, 10)? {point_2d.contains((5, 10))}")


def demo_mixed_geometry():
    section("2. Mixed Dimensionality in a Set")

    # A Set can hold 'Boxes' of different effective dimensionality
    # (e.g., a volume and a floating flat plane), provided they exist
    # in the same embedding space (dimension N).

    # 3D Space
    # Object 1: A Unit Cube (Volume)
    cube = Box([Interval(0, 1), Interval(0, 1), Interval(0, 1)])

    # Object 2: A 'Sheet' floating above it (Plane) at z=2
    # x=[0,2], y=[0,2], z=[2,2] (Point interval in Z)
    sheet = Box([Interval(0, 2), Interval(0, 2), Point(2)])

    # Object 3: A 'Line' piercing through (Line) at x=0.5, y=0.5
    # x=[0.5, 0.5], y=[0.5, 0.5], z=[-1, 3]
    line = Box([Point(0.5), Point(0.5), Interval(-1, 3)])

    universe = Set()
    universe.add(cube)
    universe.add(sheet)
    universe.add(line)

    print(f"Set contains {len(universe.boxes)} disjoint boxes.")
    print(f"Total Volume: {universe.volume()}")
    # Note: Volume of sheet and line are 0.0 mathematically in 3D (Lebesgue measure).


def demo_1d_isomorphism():
    section("3. 1D Set vs 1D IntervalSet")

    # Conceptually, Set(dim=1) is the same as IntervalSet.
    # IntervalSet is optimized (O(N log N) merge), Set is generic (recursive slicing).

    # Create disjoint pieces: [0, 2] and [4, 6]
    i1 = Interval(0, 2)
    i2 = Interval(4, 6)

    s = IntervalSet([i1, i2])
    r = Set([Box([i1]), Box([i2])])  # 1D boxes

    print(f"IntervalSet: {s}")
    print(f"Set (1D): {r}")

    # Subtraction test
    # Subtract [1, 5]
    sub = Interval(1, 5)

    s_diff = s - IntervalSet([sub])
    r_diff = r.difference(Set([Box([sub])]))

    print(f"IntervalSet Diff: {s_diff}")  # Should be {[0, 1), (5, 6]}
    print(f"Set Diff: {r_diff}")

    # They should represent the sameremaining space
    # Set might strictly output closed boxes if slicing logic defaults to closed?
    # No, our slicing algorithm preserves open/closed boundaries accurately.


if __name__ == "__main__":
    demo_points_as_intervals()
    demo_mixed_geometry()
    demo_1d_isomorphism()
