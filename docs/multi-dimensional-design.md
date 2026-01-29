# Multi-Dimensional Interval Implementation Plan

## Overview

This document outlines the design and implementation plan for extending the `interval-sets` library to support N-dimensional intervals (Hyperrectangles/Boxes) and sets of such intervals (Regions).

## Core Concepts

### 1. The `Box` Class (Hyperrectangle)
A `Box` represents a contiguous region in N-dimensional space defined by the Cartesian product of N 1-dimensional `Interval`s.

- **Definition**: $B = I_1 \times I_2 \times ... \times I_n$
- **Properties**:
  - `dimension`: The number of dimensions (N).
  - `intervals`: A tuple/list of `Interval` objects, one per dimension.
  - `volume`: Product of the lengths of component intervals.
  - `is_empty`: True if any component interval is empty.

**API Draft**:
```python
class Box:
    def __init__(self, intervals: Sequence[Interval]): ...
    
    @property
    def dimension(self) -> int: ...
    
    def volume(self) -> float: ...
    
    def contains(self, point: Sequence[float]) -> bool: ...
```

### 2. The `Region` Class (Multi-Dimensional Set)
A `Region` represents a collection of disjoint `Box`es. This is the N-dimensional equivalent of the `Set` class.

- **Normalization**: Overlapping boxes must be decomposed into disjoint boxes. This is significantly more complex than 1D merging. The "union" of two overlapping boxes may produce a non-convex shape (e.g., L-shape) which must be represented as a set of smaller disjoint boxes.
- **Operations**:
  - `Union (|)`
  - `Intersection (&)`
  - `Difference (-)`
  - `Symmetric Difference (^)`

## Key Challenges & Decisions

1.  **Disjoint Decomposition**:
    - Unlike 1D where "merging" is just extending start/end, in ND, adding two overlapping boxes $A$ and $B$ results in $A \cup (B \setminus A)$.
    - $B \setminus A$ typically fragments $B$ into multiple smaller boxes.
    - *Strategy*: Use a standard algorithm (e.g., from KD-tree or R-tree literature, or simple recursive decomposition) to maintain the invariant that `Region` contains only disjoint boxes.

2.  **Dimension Safety**:
    - All operations must enforce matching dimensions.
    - Error: `ValueError("Cannot operate on Box(dim=2) and Box(dim=3)")`.

3.  **Visualization (Optional)**:
    - `__repr__` should clearly show dimensions.
    - Possible 2D ASCII plotting for debugging?

## Implementation Roadmap

### Phase 1: The `Box` Class
- [ ] Implement `Box` initialization and validation.
- [ ] Implement `volume`, `contains` (point), `overlaps` (box).
- [ ] Implement `intersection` (component-wise intersection).
  - $A \cap B = (I_{A1} \cap I_{B1}) \times ... \times (I_{An} \cap I_{Bn})$

### Phase 2: `Box` Arithmetic & Decomposition
- [ ] Implement `Box` difference (returns set of Boxes).
  - $A \setminus B$
- [ ] Implement `Box` union (sets of Boxes).

### Phase 3: The `Region` Class
- [ ] Implement `Region` to hold list of disjoint `Box`es.
- [ ] Implement insertion/normalization logic (the hard part).
- [ ] Implement full set operations (`|`, `&`, `-`, `^`).

### Phase 4: Integration
- [ ] Update `README.md`.
- [ ] Add extensive tests, especially for 2D and 3D cases.

## Example Usage

```python
# 2D Unit Square
x_axis = Interval(0, 1)
y_axis = Interval(0, 1)
square = Box([x_axis, y_axis])

# 3D Box
cube = Box([Interval(0, 2), Interval(0, 2), Interval(0, 2)])
print(cube.volume()) # 8.0

# Region (L-shape)
b1 = Box([Interval(0, 2), Interval(0, 1)]) # Bottom bar
b2 = Box([Interval(0, 1), Interval(0, 2)]) # Left bar
l_shape = Region([b1, b2]) # Automatically handles overlap at [0,1]x[0,1]
```
