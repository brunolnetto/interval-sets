
"""
Advanced Example: 3D Constructive Solid Geometry (CSG).

This script demonstrates how to create complex 3D shapes using 
Boolean operations on Boxes.
"""
from src.intervals import Interval
from src.multidimensional import Box, Set

def run_csg_demo():
    print("=== 3D CSG: BUILDING A HOLLOW FRAME ===")

    # 1. Create a large Outer Cube [0, 10]^3
    outer_cube = Box([Interval(0, 10), Interval(0, 10), Interval(0, 10)])
    frame = Set([outer_cube])
    print(f"Initial Cube Volume: {frame.volume()}") # 1000

    # 2. Punch a hole through the X-axis (creating a 'tube')
    # Hole is 6x6 in YZ, but extends fully in X
    x_hole = Box([Interval(-1, 11), Interval(2, 8), Interval(2, 8)])
    frame = frame - x_hole
    print(f"Volume after X-hole: {frame.volume()}") # 1000 - (10 * 6 * 6) = 640

    # 3. Punch a hole through the Y-axis
    y_hole = Box([Interval(2, 8), Interval(-1, 11), Interval(2, 8)])
    frame = frame - y_hole
    print(f"Volume after Y-hole: {frame.volume()}") # 640 - (Y-hole parts not already removed)
    
    # 4. Punch a hole through the Z-axis
    z_hole = Box([Interval(2, 8), Interval(2, 8), Interval(-1, 11)])
    frame = frame - z_hole
    print(f"Volume after Z-hole: {frame.volume()}")
    
    # Final shape property
    print(f"\nFinal Hollow Frame contains {len(frame.boxes)} disjoint boxes.")
    print("This represents an exact 'Cage' structure defined by set-theoretic difference.")

    # 5. Point Probe
    # Center Point (5, 5, 5) should be empty
    center = (5, 5, 5)
    if center not in frame:
        print(f"Verification: Center point {center} is correctly hollow.")

if __name__ == "__main__":
    run_csg_demo()
