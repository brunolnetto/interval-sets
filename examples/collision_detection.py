
"""
Practical Example: 2D Collision Detection and Navigation Space.

This script demonstrates how to use the 'Set' and 'Box' classes to define
complex 2D environments and calculate navigational constraints.
"""
from src.intervals import Interval
from src.multidimensional import Box, Set

def print_result(msg, result):
    print(f"\n>>> {msg}")
    print(result)

def run_demo():
    print("=== 2D COLLISION DETECTION DEMO ===")

    # 1. Define the Environment (The "World")
    # A 100x100 room
    room = Box([Interval(0, 100), Interval(0, 100)])
    world = Set([room])

    # 2. Add Obstacles (Static Geometry)
    # A central pillar [40, 60] x [40, 60]
    pillar = Box([Interval(40, 60), Interval(40, 60)])
    # A wall on the left
    wall = Box([Interval(0, 10), Interval(0, 80)])

    obstacles = Set([pillar, wall])
    print_result("Obstacles defined (Volume)", obstacles.volume()) # 400 + 800 = 1200

    # 3. Calculate "Walkable Space" (Universe minus Obstacles)
    walkable_space = world - obstacles
    print_result("Walkable Space Volume", walkable_space.volume()) # 10000 - 1200 = 8800
    print(f"Divided into {len(walkable_space.boxes)} disjoint boxes for exact calculation.")

    # 4. Player Positioning & Collision
    # Player represented as a 2x2 box
    player_pos_1 = (50, 50) # Center of the pillar
    player_box_1 = Box([Interval(49, 51), Interval(49, 51)])

    is_colliding = obstacles & player_box_1
    if not is_colliding.is_empty():
        print(f"\n[!] Collision detected at {player_pos_1}")
        print(f"    Overlap volume: {is_colliding.volume()}")

    # Safe position
    player_pos_2 = (20, 20)
    player_box_2 = Box([Interval(19, 21), Interval(19, 21)])
    
    # Check if completely within walkable space
    if player_pos_2 in walkable_space:
        print(f"\n[v] Player safe at {player_pos_2}")

    # 5. Range Queries
    # Find all obstacles in the "Top Right Quadrant" [50, 100] x [50, 100]
    view_frustum = Box([Interval(50, 100), Interval(50, 100)])
    visible_obstacles = obstacles & view_frustum
    print_result("Visible Obstacles in Top-Right Quadrant (Volume)", visible_obstacles.volume())

if __name__ == "__main__":
    run_demo()
