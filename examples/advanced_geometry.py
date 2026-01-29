"""
Advanced Example: Architectural & Robotic Geometry.

This example showcases the library's premium features:
- Minkowski Operations (Dilation & Erosion)
- Convex Hull Calculation
- Set Diameter & Distance Analysis
- Topological Property Verification
"""

import sys
import os

# Add parent directory to path for imports to work when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from src.intervals import Interval
from src.multidimensional import Box, Set


def heading(text):
    print(f"\n{'='*60}\n{text}\n{'='*60}")


def run_demo():
    heading("1. Architectural Floor Plan")

    # Define a set of rooms (disjoint boxes)
    living_room = Box([Interval(0, 8), Interval(0, 6)])
    kitchen = Box([Interval(8, 12), Interval(0, 4)])
    bedroom = Box([Interval(0, 4), Interval(6, 10)])

    house = Set([living_room, kitchen, bedroom])
    print(f"House defined with {len(house.boxes)} rooms.")
    print(f"Total Floor Area: {house.volume()} m²")
    print(f"House Layout: {house}")

    heading("2. Configuration Space (Robotic Navigation)")
    # A robot is a 0.8m x 0.8m box
    robot_size = Box([Interval(-0.4, 0.4), Interval(-0.4, 0.4)])

    # Obstacles in the room (e.g., furniture)
    table = Box([Interval(2, 4), Interval(2, 3)])
    sofa = Box([Interval(5, 7), Interval(1, 2)])
    furniture = Set([table, sofa])

    # To find where the robot's CENTER can safely go,
    # we inflate obstacles by the robot's radius (Minkowski Sum)
    # This is called the "C-Space Obstacle"
    c_space_obstacles = furniture.dilate(robot_size)

    print(f"Original Furniture Area: {furniture.volume():.2f} m²")
    print(f"Inflated Obstacles Area: {c_space_obstacles.volume():.2f} m²")

    # Walkable area for the robot's center
    walkable_for_robot = house - c_space_obstacles
    print(f"Robot Walkable Area: {walkable_for_robot.volume():.2f} m²")

    heading("3. Equipment Fitting (Erosion)")
    # We want to place a large 3m x 3m carpet.
    # Where can the CENTER of the carpet be placed in the living room?
    carpet_size = Box([Interval(-1.5, 1.5), Interval(-1.5, 1.5)])
    carpet_valid_centers = living_room.erode(carpet_size)

    print(f"Living Room: {living_room}")
    print(f"Carpet center must be within: {carpet_valid_centers}")
    print(f"Valid area for carpet center: {carpet_valid_centers.volume()} m²")

    heading("4. Building Analysis (Convex Hull & Diameter)")
    # The footprint is the convex hull of all rooms
    footprint = house.convex_hull()
    print(f"Total Building Footprint (Convex Hull): {footprint}")
    print(
        f"Footprint Dimensions: {footprint.intervals[0].length()}m x {footprint.intervals[1].length()}m"
    )

    # The longest span of the house
    span = house.diameter()
    print(f"Maximum distance between any two points in the house: {span:.2f} m")

    # Distance between Bedroom and Kitchen
    dist = bedroom.distance(kitchen)
    print(f"Shortest distance (gap) between Bedroom and Kitchen: {dist:.2f} m")

    # 4.5 Distance between separate buildings
    detached_garage = Box([Interval(15, 20), Interval(0, 5)])
    dist_to_garage = house.distance(detached_garage)
    print(f"Detached Garage: {detached_garage}")
    print(f"Distance from house to detached garage: {dist_to_garage:.2f} m")

    heading("5. Topological Properties")
    # Is the house a compact set? (Closed and Bounded)
    # Our rooms are defined with closed intervals by default
    print(f"Is the house a bounded region? {house.is_bounded()}")
    print(f"Is the house a compact set? {house.is_compact()}")

    # Create an open "Garden" zone
    garden = Box([Interval.open(-5, 15), Interval.open(-5, 0)])
    print(f"Garden: {garden}")
    print(f"Is the garden an open set? {garden.is_open()}")
    print(f"Is the garden compact? {garden.is_compact()} (since it's open)")

    # Boundary check: The shell of the house
    house_boundary = house.boundary()
    print(
        f"Area of the house boundary: {house_boundary.volume()} (should be 0 for a 2D shell)"
    )
    print(
        f"The boundary consists of {len(house_boundary.boxes)} boundary line segments/points."
    )


if __name__ == "__main__":
    run_demo()
