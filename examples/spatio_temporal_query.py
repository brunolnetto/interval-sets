"""
Advanced Example: Spatio-Temporal Queries.

This example demonstrates using a 3D 'Set' to represent spatial regions
traversed over time. It shows how to query if a point-event (x, y, t)
falls within a managed spatio-temporal 'Set'.
"""

from src.intervals import Interval, Point, IntervalSet
from src.multidimensional import Box, Set


def run_demo():
    print("=== SPATIO-TEMPORAL QUERY DEMO ===")

    # 1. Define a "Moving Zone"
    # Dimension 0: X, Dimension 1: Y, Dimension 2: Time (T)

    # Zone A: At T=[0, 10], Zone is [0, 5]x[0, 5]
    zone_a_early = Box([Interval(0, 5), Interval(0, 5), Interval(0, 10)])

    # Zone A: At T=[10, 20], Zone moves to [5, 10]x[5, 10]
    zone_a_late = Box([Interval(5, 10), Interval(5, 10), Interval(10, 20)])

    # Create the Spatio-Temporal Set
    restricted_area = Set([zone_a_early, zone_a_late])

    print(f"Restricted Area defined as a 3D Set.")
    print(
        f"Total Spatio-Temporal Volume: {restricted_area.volume()}"
    )  # 25*10 + 25*10 = 500

    # 2. Querying Events
    # Event 1: At T=5, Point (2, 2) -> Should be inside
    event_1 = (2, 2, 5)
    print(f"\nQuery: Is Event {event_1} in restricted area?")
    print(f"Result: {event_1 in restricted_area}")  # True

    # Event 2: At T=15, Point (2, 2) -> Should be outside (Zone moved)
    event_2 = (2, 2, 15)
    print(f"Query: Is Event {event_2} in restricted area?")
    print(f"Result: {event_2 in restricted_area}")  # False

    # Event 3: At T=15, Point (7, 7) -> Should be inside
    event_3 = (7, 7, 15)
    print(f"Query: Is Event {event_3} in restricted area?")
    print(f"Result: {event_3 in restricted_area}")  # True

    # 3. Intersection Query (Time Slice)
    # What was the spatial footprint at T=[5, 15]?
    time_slice = Box(
        [
            Interval(-float("inf"), float("inf")),
            Interval(-float("inf"), float("inf")),
            Interval(5, 15),
        ]
    )

    footprint_in_slice = restricted_area & time_slice
    print(
        f"\nSpatio-temporal volume between T=5 and T=15: {footprint_in_slice.volume()}"
    )
    # Should be (5*5 * 5) [T=5,10] + (5*5 * 5) [T=10,15] = 125 + 125 = 250

    # 4. Universal Promotion Demo
    print("\n=== PROMOTION DEMO ===")

    # Create a 1D Time-Only Set
    maintenance_windows = IntervalSet([Interval(25, 30), Interval(40, 45)])

    # Promote it to a 1D Box Set automatically
    # Note: We need to be careful with dimensions. A 3D set cannot add a 1D set.
    # But we can create a new 1D Set container.
    timeline = Set()
    timeline.add(maintenance_windows)

    print(f"1D Set created from IntervalSet. Dimension: {timeline.dimension}")
    print(f"Total time covered: {timeline.volume()}")

    # 5. Advanced Query: Proximity
    # Is any event "close" to the restricted area?
    risky_point = (12, 12, 15)  # Outside but near Zone A Late [5,10]x[5,10] at T=15
    dist = restricted_area.distance_to_point(risky_point)
    print(f"\nQuery: Distance from {risky_point} to restricted area?")
    print(f"Result: {dist:.2f} units")

    if dist < 5.0:
        print("Warning: Point is within 5 units of a restricted Spatio-Temporal zone!")


if __name__ == "__main__":
    run_demo()
