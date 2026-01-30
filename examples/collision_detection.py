"""
Practical Example: 2D Collision Detection and Navigation Space.

This script demonstrates how to use the 'BoxSet' and 'Box' classes to define
complex 2D environments and calculate navigational constraints.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intervals import Interval
from src.multidimensional import Box, BoxSet


def print_result(msg, result):
    print(f"\n>>> {msg}")
    print(result)


def run_demo():
    print("=== 2D COLLISION DETECTION DEMO ===")

    # 1. Define the Environment (The "World")
    # A 100x100 room
    room = Box([Interval(0, 100), Interval(0, 100)])
    world = BoxSet([room])

    # 2. Add Obstacles (Static Geometry)
    # A central pillar [40, 60] x [40, 60]
    pillar = Box([Interval(40, 60), Interval(40, 60)])
    # A wall on the left
    wall = Box([Interval(0, 10), Interval(0, 80)])

    obstacles = BoxSet([pillar, wall])
    print_result("Obstacles defined (Volume)", obstacles.volume())  # 400 + 800 = 1200

    # 3. Calculate "Walkable Space" (Universe minus Obstacles)
    walkable_space = world - obstacles
    print_result(
        "Walkable Space Volume", walkable_space.volume()
    )  # 10000 - 1200 = 8800
    print(
        f"Divided into {len(walkable_space.boxes)} disjoint boxes for exact calculation."
    )

    # 4. Player Positioning & Collision
    # Player represented as a 2x2 box
    player_size = Box([Interval(-1, 1), Interval(-1, 1)])
    player_pos_1 = (50, 50)  # Center of the pillar

    # Check collision by inflating obstacles by player size (Minkowski Sum)
    # This creates the "C-Space" (Configuration Space) obstacles
    c_obstacles = obstacles.dilate(player_size)

    if player_pos_1 in c_obstacles:
        print(f"\n[!] Collision detected at {player_pos_1}")
        print(f"    (The center of a 2x2 player is inside an inflated obstacle)")

    # Safe position
    player_pos_2 = (20, 20)
    if player_pos_2 in world - c_obstacles:
        print(f"\n[v] Player safe at {player_pos_2}")

    # 5. Analysis
    # Get the bounding box of all obstacles
    bounding_box = obstacles.convex_hull()
    print_result("Obstacles Bounding Box", bounding_box)
    print(f"Maximum obstacle span (diameter): {obstacles.diameter():.2f}")


if __name__ == "__main__":
    run_demo()
