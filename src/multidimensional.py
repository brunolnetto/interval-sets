"""
Multi-dimensional interval arithmetic (Boxes and Regions).
"""

from typing import Sequence, List, Union, Tuple, Optional, Iterable
import math
from .intervals import Interval, IntervalSet


class Box:
    """
    Represents a contiguous region in N-dimensional space defined by the
    Cartesian product of N 1-dimensional Intervals.

    Definition: B = I_1 x I_2 x ... x I_n

    A Box can represent:
    - N-dimensional volume (all intervals non-degenerate)
    - Face/Hyperplane (1 degenerate interval)
    - Edge/Line (N-1 degenerate intervals)
    - Point (N degenerate intervals)
    """

    def __init__(self, intervals: Sequence[Interval]):
        """
        Create a new Box intersection of intervals.

        Args:
            intervals: A sequence of Interval objects, one for each dimension.
                       Can be empty for a 0-dimensional point? Or invalid?
                       We enforce at least 1 dimension?
        """
        if not intervals:
            raise ValueError("Box must have at least 1 dimension")

        self._intervals = tuple(intervals)
        self._dimension = len(intervals)

    @property
    def dimension(self) -> int:
        """The number of dimensions (N)."""
        return self._dimension

    @classmethod
    def empty(cls, dimension: int) -> "Box":
        """Create an empty box of the specified dimension."""
        return cls([Interval.empty()] * dimension)

    @property
    def intervals(self) -> Tuple[Interval, ...]:
        """The component intervals, one per dimension."""
        return self._intervals

    def is_empty(self) -> bool:
        """
        Check if the box is empty.
        A box is empty if ANY of its component intervals are empty.
        """
        return any(i.is_empty() for i in self._intervals)

    def volume(self) -> float:
        """
        Compute the N-dimensional volume (measure).
        """
        if self.is_empty():
            return 0.0

        vol = 1.0
        for i in self._intervals:
            vol *= i.length()
        return vol

    def is_bounded(self) -> bool:
        """Check if the box is bounded (all component intervals bounded)."""
        if self.is_empty():
            return True
        return all(i.is_bounded() for i in self._intervals)

    def is_open(self) -> bool:
        """Check if the box is open."""
        return not self.is_empty() and self == self.interior()

    def is_closed(self) -> bool:
        """Check if the box is closed."""
        return not self.is_empty() and self == self.closure()

    def is_compact(self) -> bool:
        """Check if the box is compact (closed and bounded)."""
        return self.is_closed() and self.is_bounded()

    def contains(self, item: Union[Sequence[float], "Box", "Set"]) -> bool:
        """
        Check if an N-dimensional point or Box/Set is contained in this box.
        """
        if isinstance(item, Box):
            if item.is_empty():
                return True
            if item.dimension != self.dimension:
                return False
            for i1, i2 in zip(self._intervals, item._intervals):
                if not i1.contains(i2):
                    return False
            return True

        if isinstance(item, Set):
            if item.is_empty():
                return True
            return all(self.contains(b) for b in item.boxes)

        # Point check
        point = item
        if len(point) != self._dimension:
            raise ValueError(
                f"Point dimension {len(point)} must match Box dimension {self._dimension}"
            )

        if self.is_empty():
            return False

        # Point is in box iff x_i in I_i for all i
        for val, interval in zip(point, self._intervals):
            if not interval.contains(val):
                return False
        return True

    def __contains__(self, item: Union[Sequence[float], "Box", "Set"]) -> bool:
        return self.contains(item)

    def overlaps(self, other: "Box") -> bool:
        """
        Check if this box overlaps with another box.

        Two boxes overlap if and only if they overlap in ALL dimensions.
        """
        if not isinstance(other, Box):
            return False  # Or raise TypeError

        if self._dimension != other._dimension:
            raise ValueError(
                f"Cannot compare Box(dim={self._dimension}) with Box(dim={other._dimension})"
            )

        if self.is_empty() or other.is_empty():
            return False

        return all(i1.overlaps(i2) for i1, i2 in zip(self._intervals, other.intervals))

    def intersection(self, other: "Box") -> "Box":
        """
        Compute the intersection of two boxes.
        Result is always a single Box (Cartesian product of dimension-wise intersections).
        """
        if self._dimension != other._dimension:
            raise ValueError(
                f"Dimension mismatch: {self._dimension} vs {other._dimension}"
            )

        # B_new = (I1 & J1) x (I2 & J2) ...
        # If any resulting interval I_k & J_k is convex (Interval), we assume Interval intersection returns Interval or simple Set.
        # But Interval.intersection returns Interval or Point or empty...
        # Wait, Interval.intersection currently returns Interval or Set (if empty).
        # We need component intersections to be Intervals.
        # Fortunately, the intersection of two Intervals is ALWAYS a single Interval (possibly empty).
        # It is Union that creates multiple intervals.

        new_intervals = []
        for i1, i2 in zip(self._intervals, other.intervals):
            inter = i1.intersection(i2)
            # inter creates a Point if single point, or Interval or empty Set?
            # Interval.intersection returns empty Set if empty...
            # We need to normalize this back to Interval to store in Box.

            # If inter is a Set (likely empty set from intersection), we check is_empty
            if hasattr(inter, "is_empty") and inter.is_empty():
                new_intervals.append(Interval.empty())
            else:
                # It must be an Interval or Point (subclass of Interval)
                if isinstance(inter, Interval):
                    new_intervals.append(inter)
                else:
                    new_intervals.append(Interval.empty())

        return Box(new_intervals)

    def interior(self) -> "Box":
        """
        Return the interior of the box.
        The interior is the Cartesian product of the interior of its intervals.
        """
        if self.is_empty():
            return self
        return Box([interval.interior() for interval in self._intervals])

    def closure(self) -> "Box":
        """
        Return the closure of the box.
        The closure is the Cartesian product of the closure of its intervals.
        """
        if self.is_empty():
            return self
        return Box([interval.closure() for interval in self._intervals])

    def boundary(self) -> "Set":
        """
        Return the topological boundary of the box.
        boundary(B) = closure(B) - interior(B)
        """
        if self.is_empty():
            return Set()
        return Set([self.closure()]) - self.interior()

    def convex_hull(self) -> "Box":
        """Return the smallest convex box containing this box."""
        return self

    def diameter(self) -> float:
        """Return the maximum distance between any two points in the box."""
        if self.is_empty():
            return 0.0
        return math.sqrt(sum(i.length() ** 2 for i in self._intervals))

    def distance_to_point(self, point: Sequence[float]) -> float:
        """Return the minimum Euclidean distance from a point to this box."""
        if self.is_empty():
            return float("inf")
        if len(point) != self.dimension:
            raise ValueError(f"Dimension mismatch: {len(point)} vs {self.dimension}")

        d2 = 0.0
        for i in range(self.dimension):
            iv = self._intervals[i]
            p = point[i]
            if p < iv.start:
                d2 += (iv.start - p) ** 2
            elif p > iv.end:
                d2 += (p - iv.end) ** 2
        return math.sqrt(d2)

    def minkowski_sum(self, other: Union["Box", Sequence[float], float]) -> "Box":
        """
        Compute the Minkowski sum of this box and another (dilation).
        A + B = {x + y : x in A, y in B}
        """
        if self.is_empty():
            return self

        if isinstance(other, (int, float)):
            return Box([interval.minkowski_sum(other) for interval in self._intervals])

        if isinstance(other, (list, tuple)):
            if len(other) != self.dimension:
                raise ValueError(
                    f"Vector dimension {len(other)} must match Box dimension {self.dimension}"
                )
            return Box(
                [
                    self._intervals[i].minkowski_sum(other[i])
                    for i in range(self.dimension)
                ]
            )

        if not isinstance(other, Box):
            raise TypeError(f"Minkowski sum requires Box, got {type(other)}")

        if other.is_empty():
            return other

        if other.dimension != self.dimension:
            raise ValueError(
                f"Box dimension {other.dimension} must match {self.dimension}"
            )

        return Box(
            [
                self._intervals[i].minkowski_sum(other._intervals[i])
                for i in range(self.dimension)
            ]
        )

    def distance(self, other: "Box") -> float:
        """Compute the minimum Euclidean distance between two boxes."""
        if self.is_empty() or other.is_empty():
            return float("inf")
        if self.dimension != other.dimension:
            raise ValueError(
                f"Dimension mismatch: {self.dimension} vs {other.dimension}"
            )

        d2 = 0.0
        for i in range(self.dimension):
            iv = self._intervals[i]
            jv = other.intervals[i]

            # 1D distance between intervals
            if iv.overlaps(jv) or iv.is_adjacent(jv):
                dist_i = 0.0
            elif iv.end < jv.start:
                dist_i = jv.start - iv.end
            else:  # jv.end < iv.start
                dist_i = iv.start - jv.end

            d2 += dist_i**2
        return math.sqrt(d2)

    def minkowski_difference(self, other: "Box") -> "Box":
        """
        Compute the Minkowski difference (erosion).
        A - B = {x : {x} + B is a subset of A}
        """
        if self.is_empty():
            return self

        if not isinstance(other, Box):
            raise TypeError(f"Minkowski difference requires Box, got {type(other)}")

        if other.is_empty():
            return Box.empty(self.dimension)

        if other.dimension != self.dimension:
            raise ValueError(
                f"Box dimension {other.dimension} must match {self.dimension}"
            )

        results = []
        for i in range(self.dimension):
            diff = self._intervals[i].minkowski_difference(other._intervals[i])
            if diff.is_empty():
                return Box([Interval.empty()] * self.dimension)
            results.append(diff)

        return Box(results)

    def dilate(self, other: Union["Box", Sequence[float], float]) -> "Box":
        """Alias for minkowski_sum"""
        return self.minkowski_sum(other)

    def erode(self, other: "Box") -> "Box":
        """Alias for minkowski_difference"""
        return self.minkowski_difference(other)

    def __add__(self, other: Union["Box", Sequence[float], float]) -> "Box":
        return self.minkowski_sum(other)

    def __radd__(self, other: Union[Sequence[float], float]) -> "Box":
        return self.minkowski_sum(other)

    def __repr__(self) -> str:
        return f"Box({list(self._intervals)})"

    def __eq__(self, other) -> bool:
        if hasattr(other, "boxes"):  # Set-like
            return other == self
        if not isinstance(other, Box):
            return False
        return self._intervals == other._intervals

    def __len__(self) -> int:
        """Return the dimension of the box."""
        return self._dimension

    def __iter__(self):
        """Iterate over component intervals."""
        return iter(self._intervals)

    def difference(self, other: "Box") -> List["Box"]:
        r"""
        Compute A \ B (set difference).
        Returns a list of disjoint boxes that represent the remaining region.

        Strategy: Recursive Slicing (Dimension reduction)
        1. Find intersection O = A & B.
        2. For each dimension, 'slice off' the parts of A that are strictly
           left/right of O.
        3. Shrink A to the bounds of O in that dimension and repeat.
        """
        if self._dimension != other._dimension:
            raise ValueError(
                f"Dimension mismatch: {self._dimension} vs {other._dimension}"
            )

        # if not self.overlaps(other): # Optimization
        #     return [self]

        inter = self.intersection(other)
        if inter.is_empty():
            return [self]

        result_boxes = []

        # We start with the full 'self' box and whittle it down
        # We define 'remainder' as the part of A that matches O in the dimensions processed so far
        current_intervals = list(self._intervals)

        overlap_intervals = inter.intervals

        for d in range(self._dimension):
            # Current dimension interval for the remainder of A
            r_int = current_intervals[d]
            # Overlap interval in this dimension
            o_int = overlap_intervals[d]

            # 1. Slice Left (Before Overlap)
            # Boundary: [r_start, o_start).
            left_open_end = not o_int.open_start

            # Create left interval.
            # Safety: r_int.start <= o_int.start (subset).
            # Code is unreachable if InvalidIntervalError is raised, but we expect validity.
            # We explicitly check for emptiness instead of rely on exception flow.
            # Using Interval constructor directly as it is robust.

            left_int = Interval(
                r_int.start,
                o_int.start,
                open_start=r_int.open_start,
                open_end=left_open_end,
            )

            if not left_int.is_empty():
                new_slice = list(current_intervals)
                new_slice[d] = left_int
                result_boxes.append(Box(new_slice))

            # 2. Slice Right (After Overlap)
            # Starts at o_int.end.
            right_open_start = not o_int.open_end

            right_int = Interval(
                o_int.end,
                r_int.end,
                open_start=right_open_start,
                open_end=r_int.open_end,
            )

            if not right_int.is_empty():
                new_slice = list(current_intervals)
                new_slice[d] = right_int
                result_boxes.append(Box(new_slice))

            # 3. Update 'current_intervals' for next dimension extraction
            current_intervals[d] = o_int

        return result_boxes


class Set:
    """
    Represents a set of disjoint N-dimensional boxes.
    This is the multi-dimensional equivalent of IntervalSet.

    Invariants:
    - All boxes in the set are pairwise disjoint.
    - All boxes have the same dimension.
    """

    def __init__(
        self, boxes: Optional[Iterable[Union[Box, "Set", Interval, IntervalSet]]] = None
    ):
        """
        Create a Set (collection of disjoint boxes).
        The inputs will be normalized to ensure disjointness.
        """
        self._dimension: Optional[int] = None
        self._boxes: List[Box] = []

        if boxes:
            for box in boxes:
                self.add(box)

    @property
    def dimension(self) -> Optional[int]:
        return self._dimension

    @property
    def boxes(self) -> List[Box]:
        """Return a copy of the list of disjoint boxes."""
        return list(self._boxes)

    def is_empty(self) -> bool:
        return not self._boxes

    def volume(self) -> float:
        """Total volume of the region."""
        return sum(box.volume() for box in self._boxes)

    def add(self, item: Union[Box, "Set", Interval, IntervalSet]) -> None:
        """
        Add an item (Box, Set, Interval, or IntervalSet) to the set, maintaining disjointness.

        Promotion:
            - Interval -> Box([Interval])
            - IntervalSet -> Multiple Box([Interval])
        """
        if isinstance(item, Set):
            for b in item.boxes:
                self.add(b)
            return

        if isinstance(item, Interval):
            item = Box([item])
        elif isinstance(item, IntervalSet):
            for i in item:
                self.add(Box([i]))
            return

        box = item
        if not isinstance(box, Box):
            raise TypeError(
                f"Cannot add {type(item)} to Set. Expected Box, Set, Interval or IntervalSet."
            )

        if box.is_empty():
            return

        if self._dimension is None:
            self._dimension = int(box.dimension)
        elif self._dimension != box.dimension:
            raise ValueError(
                f"Dimension mismatch: Set({self._dimension}) vs Box({box.dimension})"
            )

        # We want to add 'box' to our collection.
        # But we must subtract all EXISTING boxes from 'box' to find the
        # "fresh" parts of 'box' to add.
        # Existing self._boxes are already disjoint among themselves.

        fragments = [box]

        for existing in self._boxes:
            # We don't need to check all existing boxes, only those that overlap fragments.
            # But iterating all is O(N). Spatial index would be better for distinct N.
            if not fragments:
                break

            new_fragments = []
            for frag in fragments:
                if frag.overlaps(existing):
                    # Subtract existing from this fragment
                    # diff returns list of sub-fragments (disjoint from existing)
                    diffs = frag.difference(existing)
                    new_fragments.extend(diffs)
                else:
                    new_fragments.append(frag)
            fragments = new_fragments

        # Add the remaining disjoint fragments
        self._boxes.extend(fragments)

    def is_bounded(self) -> bool:
        """Check if the set is bounded."""
        if self.is_empty():
            return True
        return all(b.is_bounded() for b in self._boxes)

    def is_open(self) -> bool:
        """Check if the set is open."""
        return not self.is_empty() and self == self.interior()

    def is_closed(self) -> bool:
        """Check if the set is closed."""
        return not self.is_empty() and self == self.closure()

    def is_compact(self) -> bool:
        """Check if the set is compact (closed and bounded)."""
        return self.is_closed() and self.is_bounded()

    def distance(self, other: Union["Set", Box, Interval, IntervalSet]) -> float:
        """Compute the minimum Euclidean distance between two sets."""
        if self.is_empty() or other.is_empty():
            return float("inf")

        # Promote other to Set if needed
        if not isinstance(other, Set):
            other = Set([other])

        return min(b1.distance(b2) for b1 in self._boxes for b2 in other.boxes)

    def interior(self) -> "Set":
        """
        Return the interior of the set.
        The interior of a set is the union of the interiors of its component boxes.
        """
        if self.is_empty():
            return self
        # Create a new Set from the interiors of component boxes.
        # Since component boxes are disjoint, their interiors are also disjoint.
        return Set([box.interior() for box in self._boxes])

    def closure(self) -> "Set":
        """
        Return the closure of the set.
        The closure of a set is the union of the closures of its component boxes.
        """
        if self.is_empty():
            return self
        return Set([box.closure() for box in self._boxes])

    def boundary(self) -> "Set":
        """
        Return the topological boundary of the set.
        boundary(A) = closure(A) - interior(A)
        """
        if self.is_empty():
            return self
        return self.closure() - self.interior()

    def convex_hull(self) -> Box:
        """Return the smallest convex box containing this set."""
        if self.is_empty():
            return Box.empty(self._dimension or 1)

        if self._dimension is None:
            # Should be handled by is_empty check, but for typing:
            return Box.empty(1)

        intervals = []
        for d in range(self._dimension):
            inf_d = min(b.intervals[d].start for b in self._boxes)
            sup_d = max(b.intervals[d].end for b in self._boxes)

            has_closed_start = any(
                b.intervals[d].start == inf_d and not b.intervals[d].open_start
                for b in self._boxes
            )
            has_closed_end = any(
                b.intervals[d].end == sup_d and not b.intervals[d].open_end
                for b in self._boxes
            )

            intervals.append(
                Interval(
                    inf_d,
                    sup_d,
                    open_start=not has_closed_start,
                    open_end=not has_closed_end,
                )
            )
        return Box(intervals)

    def diameter(self) -> float:
        """Return the maximum distance between any two points in the set."""
        if self.is_empty():
            return 0.0
        return self.convex_hull().diameter()

    def distance_to_point(self, point: Sequence[float]) -> float:
        """Return the minimum Euclidean distance from a point to this set."""
        if self.is_empty():
            return float("inf")
        return min(b.distance_to_point(point) for b in self._boxes)

    def contains(self, item: Union[Sequence[float], Box, "Set"]) -> bool:
        """Check if point, Box, or Set is contained in this Set."""
        if isinstance(item, Box):  # Box-like
            if item.is_empty():
                return True
            # Box is in Set if it's contained in the UNION of component boxes.
            if self.is_empty():
                return item.is_empty()
            return (Set([item]) - self).is_empty()

        if isinstance(item, Set):  # Set-like
            if item.is_empty():
                return True
            return all(self.contains(b) for b in item.boxes)

        # Point check
        point = item
        if self._dimension is None:
            return False

        if len(point) != self._dimension:
            raise ValueError(
                f"Point dimension {len(point)} must match Set dimension {self._dimension}"
            )

        for box in self._boxes:
            if box.contains(point):
                return True
        return False

    def __contains__(self, item: Union[Sequence[float], Box, "Set"]) -> bool:
        return self.contains(item)

    def intersection(
        self, other: Union[Box, "Set", "Interval", "IntervalSet"]
    ) -> "Set":
        """
        Compute intersection with another Set, Box, Interval, or IntervalSet.
        Returns a new Set.
        """
        if not isinstance(other, Set):
            other = Set([other])

        if self._dimension and other.dimension and self._dimension != other.dimension:
            raise ValueError("Dimension mismatch")

        # Result is Union(A_i & B_j) for all i, j.
        # Since A_i disjoint and B_j disjoint, the results (A_i & B_j) are automatically disjoint?
        # Proof:
        # (A1 & B1) vs (A1 & B2). A1 is same. B1 disjoint B2 => (A1&B1) disjoint (A1&B2).
        # (A1 & B1) vs (A2 & B1). A1 disjoint A2 => ...
        # (A1 & B1) vs (A2 & B2). Disjoint.
        # So yes! We just collect all pairwise intersections.

        result_boxes = []
        for b1 in self._boxes:
            for b2 in other.boxes:
                if b1.overlaps(b2):
                    inter = b1.intersection(b2)
                    # overlaps() guarantees non-empty intersection
                    result_boxes.append(inter)

        # Manually create region to bypass normalization checks?
        # Or just use constructor (which attempts normalization but here inputs are already disjoint).
        # But Set() constructor calls add() which runs difference logic.
        # If we pass disjoint boxes to constructor, add() loop will just verify validity (overlap check fails).
        # So it is safe but maybe O(N^2) instead of O(N)?
        # For now, safe constructor.
        return Set(result_boxes)

    def difference(self, other: Union[Box, "Set", "Interval", "IntervalSet"]) -> "Set":
        """
        Compute A - B.
        A set is a collection of boxes A_i.
        A - B = Union(A_i) - Union(B_j) = Union( (A_i - Union(B_j)) )
        For each A_i, we subtract ALL B_j.
        """
        if not isinstance(other, Set):
            other = Set([other])

        if self._dimension and other.dimension and self._dimension != other.dimension:
            raise ValueError("Dimension mismatch")

        final_boxes = []

        for a_box in self._boxes:
            # We start with A_i and chop parts off it
            current_fragments = [a_box]

            for b_box in other.boxes:
                next_fragments = []
                for frag in current_fragments:
                    if frag.overlaps(b_box):
                        next_fragments.extend(frag.difference(b_box))
                    else:
                        next_fragments.append(frag)
                current_fragments = next_fragments
                if not current_fragments:
                    break

            final_boxes.extend(current_fragments)

        return Set(final_boxes)

    def union(self, other: Union[Box, "Set", Interval, IntervalSet]) -> "Set":
        """
        Compute A | B.
        Just create new Set with all boxes.
        """
        # Promotion handled by add()
        new_set = Set(self._boxes)
        new_set.add(other)
        return new_set

    def symmetric_difference(
        self, other: Union[Box, "Set", Interval, IntervalSet]
    ) -> "Set":
        """
        Compute A ^ B = (A - B) | (B - A).
        """
        if not isinstance(other, Set):
            other = Set([other])

        diff1 = self.difference(other)
        diff2 = other.difference(self)
        return diff1.union(diff2)

    def __or__(self, other: Union[Box, "Set", Interval, IntervalSet]) -> "Set":
        return self.union(other)

    def __and__(self, other: Union[Box, "Set", Interval, IntervalSet]) -> "Set":
        return self.intersection(other)

    def __sub__(self, other: Union[Box, "Set", Interval, IntervalSet]) -> "Set":
        return self.difference(other)

    def __xor__(self, other: Union[Box, "Set", Interval, IntervalSet]) -> "Set":
        return self.symmetric_difference(other)

    def is_connected(self) -> bool:
        """
        Check if the set is connected.
        A set of disjoint boxes is connected if its adjacency graph is connected.
        """
        if self.is_empty() or len(self._boxes) <= 1:
            return True

        return len(self.connected_components()) == 1

    def connected_components(self) -> List["Set"]:
        """
        Decompose the set into its connected components.
        Boxes are considered 'connected' if their closures have a non-empty intersection.
        """
        if self.is_empty():
            return []

        n = len(self._boxes)
        n = len(self._boxes)
        adj: List[List[int]] = [[] for _ in range(n)]

        # Build adjacency list
        for i in range(n):
            for j in range(i + 1, n):
                # Check if closures overlap in all dimensions
                is_adj = True
                assert self._dimension is not None
                for k in range(self._dimension):
                    # We use Interval.closure() followed by overlaps()
                    if (
                        not self._boxes[i]
                        .intervals[k]
                        .closure()
                        .overlaps(self._boxes[j].intervals[k].closure())
                    ):
                        is_adj = False
                        break

                if is_adj:
                    adj[i].append(j)
                    adj[j].append(i)

        components = []
        visited = [False] * n

        for root in range(n):
            if not visited[root]:
                comp_indices = []
                stack = [root]
                visited[root] = True

                while stack:
                    curr = stack.pop()
                    comp_indices.append(curr)
                    for neighbor in adj[curr]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            stack.append(neighbor)

                components.append(Set([self._boxes[idx] for idx in comp_indices]))

        return components

    def minkowski_sum(
        self, other: Union["Set", Box, Interval, IntervalSet, Sequence[float], float]
    ) -> "Set":
        """
        Compute the Minkowski sum of this set and another (dilation).
        """
        if self.is_empty():
            return self

        if isinstance(other, (int, float, list, tuple)):
            # Shift all boxes
            return Set([box.minkowski_sum(other) for box in self._boxes])

        if not isinstance(other, Set):
            other = Set([other])  # type: ignore

        if other.is_empty():
            return other

        # Pairwise sums of boxes
        results = []
        for b_a in self._boxes:
            for b_b in other.boxes:
                results.append(b_a.minkowski_sum(b_b))
        return Set(results)

    def minkowski_difference(
        self, other: Union["Set", Box, Interval, IntervalSet]
    ) -> "Set":
        """
        Compute the Minkowski difference (erosion).
        A - B = {x : {x} + B is a subset of A}
        """
        if self.is_empty():
            return self

        # If other is connected (Box/Interval), we erode component-wise
        if isinstance(other, (Box, Interval)):
            if other.is_empty():
                return Set()
            # Box promotion if needed
            if isinstance(other, Interval):
                other = Box([other])

            results = []
            for b_a in self._boxes:
                res = b_a.minkowski_difference(other)
                if not res.is_empty():
                    results.append(res)
            return Set(results)

        if isinstance(other, IntervalSet):
            other = Set([other])

        if not isinstance(other, Set):
            raise TypeError(
                f"Minkowski difference requires Set, Box, or Interval, got {type(other)}"
            )

        if other.is_empty():
            return Set()

        # Intersection of erosions by each component box
        current_res: "Set" = self
        for b_b in other.boxes:
            res_b = self.minkowski_difference(b_b)
            current_res = current_res & res_b  # type: ignore
            if current_res.is_empty():
                break
        return current_res

    def dilate(
        self, other: Union["Set", Box, Interval, IntervalSet, Sequence[float], float]
    ) -> "Set":
        """Alias for minkowski_sum"""
        return self.minkowski_sum(other)

    def erode(self, other: Union["Set", Box, Interval, IntervalSet]) -> "Set":
        """Alias for minkowski_difference"""
        return self.minkowski_difference(other)

    def dilate_epsilon(self, epsilon: float) -> "Set":
        """
        Shortcut for dilation by a centered box [-epsilon, epsilon]^N.
        This expands the set in all directions.
        """
        if epsilon == 0:
            return self
        dim = self._dimension or 1
        ebit = Interval.closed(-epsilon, epsilon)
        ebox = Box([ebit] * dim)
        return self.dilate(ebox)

    def __add__(
        self, other: Union["Set", Box, Interval, IntervalSet, Sequence[float], float]
    ) -> "Set":
        return self.minkowski_sum(other)

    def __radd__(self, other: Union[Sequence[float], float]) -> "Set":
        return self.minkowski_sum(other)

    def opening(self, other: Union["Set", Box, Interval, IntervalSet]) -> "Set":
        """
        Compute the morphological opening of this set by another.
        Opening(A, B) = dilation(erosion(A, B), B)
        """
        return self.erode(other).dilate(other)

    def closing(self, other: Union["Set", Box, Interval, IntervalSet]) -> "Set":
        """
        Compute the morphological closing of this set by another.
        Closing(A, B) = erosion(dilation(A, B), B)
        """
        return self.dilate(other).erode(other)

    def __eq__(self, other) -> bool:
        """Check equality with another set or box/interval."""
        if isinstance(other, (Box, Interval, IntervalSet)):
            other = Set([other])
        if not isinstance(other, Set):
            return False
        if self.is_empty() and other.is_empty():
            return True
        if self._dimension != other._dimension:
            return False
        # Disjoint boxes equality is tricky if they are not canonical.
        # But our add() ensures disjointness.
        # However, same region can be tiled differently.
        # For strict equality, we'd need canonical form.
        # For now, let's at least handle the easy case and volume check.
        # Better: A == B iff (A - B) is empty and (B - A) is empty.
        return (self - other).is_empty() and (other - self).is_empty()

    def __repr__(self) -> str:
        return f"Set(dim={self._dimension}, boxes={len(self._boxes)})"

    def __iter__(self):
        return iter(self._boxes)
