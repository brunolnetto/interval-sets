"""
Generic R-tree implementation for spatial indexing.
"""

from typing import List, Optional, Tuple, Union, TypeVar, Generic, Callable

T = TypeVar("T")
# MBR Type: expected to have a .volume() method and a .overlaps(other) method
# and a .intervals property or similar. In this library, it's a Box.
MBR = TypeVar("MBR")


class RTreeNode(Generic[T, MBR]):
    """A node in the R-tree."""

    def __init__(self, max_entries: int, is_leaf: bool = False):
        self.max_entries = max_entries
        self.is_leaf = is_leaf
        self.children: List[Union["RTreeNode[T, MBR]", T]] = []
        self.mbr: Optional[MBR] = None
        self.parent: Optional["RTreeNode[T, MBR]"] = None

    def add_child(
        self,
        child: Union["RTreeNode[T, MBR]", T],
        child_mbr: MBR,
        expand_func: Callable[[Optional[MBR], MBR], MBR],
    ) -> None:
        """Add a child to this node and update MBR."""
        self.children.append(child)
        if isinstance(child, RTreeNode):
            child.parent = self

        self.mbr = expand_func(self.mbr, child_mbr)

    def recalculate_mbr(
        self,
        get_mbr_func: Callable[[Union["RTreeNode[T, MBR]", T]], MBR],
        expand_func: Callable[[Optional[MBR], MBR], MBR],
    ) -> None:
        """Recalculate MBR from scratch based on children."""
        self.mbr = None
        for child in self.children:
            self.mbr = expand_func(self.mbr, get_mbr_func(child))


class RTree(Generic[T, MBR]):
    """
    R-tree spatial index for fast intersection and containment queries.
    Implemented with Quadratic Split algorithm.
    """

    def __init__(
        self,
        get_mbr_func: Callable[[Union[RTreeNode[T, MBR], T]], MBR],
        expand_mbr_func: Callable[[Optional[MBR], MBR], MBR],
        get_volume_func: Callable[[MBR], float],
        overlaps_func: Callable[[MBR, MBR], bool],
        min_entries: int = 2,
        max_entries: int = 4,
    ):
        self.get_mbr = get_mbr_func
        self.expand_mbr = expand_mbr_func
        self.get_volume = get_volume_func
        self.overlaps = overlaps_func
        self.min_entries = min_entries
        self.max_entries = max_entries
        self.root: RTreeNode[T, MBR] = RTreeNode(max_entries, is_leaf=True)

    def insert(self, item: T) -> None:
        """Insert a new item into the R-tree."""
        item_mbr = self.get_mbr(item)
        leaf = self._choose_leaf(self.root, item_mbr)
        leaf.add_child(item, item_mbr, self.expand_mbr)

        if len(leaf.children) > self.max_entries:
            self._split_node(leaf)
        else:
            self._adjust_tree(leaf)

    def _choose_leaf(self, node: RTreeNode[T, MBR], item_mbr: MBR) -> RTreeNode[T, MBR]:
        """Choose the leaf node where a new item should be inserted."""
        if node.is_leaf:
            return node

        best_child: Optional[RTreeNode[T, MBR]] = None
        min_enlargement = float("inf")
        min_area = float("inf")

        for child in node.children:
            # Type guard for internal nodes
            if not isinstance(child, RTreeNode):
                continue

            area_before = self.get_volume(child.mbr) if child.mbr is not None else 0.0

            # Temporary enlargement
            new_mbr = self.expand_mbr(child.mbr, item_mbr)
            area_after = self.get_volume(new_mbr)

            enlargement = area_after - area_before

            if enlargement < min_enlargement:
                min_enlargement = enlargement
                min_area = area_after
                best_child = child
            elif enlargement == min_enlargement:
                if area_after < min_area:
                    min_area = area_after
                    best_child = child
                elif area_after == min_area:
                    if len(child.children) < len(best_child.children):  # type: ignore
                        best_child = child

        if best_child is None:  # Should not happen if tree is valid
            return node

        return self._choose_leaf(best_child, item_mbr)

    def _adjust_tree(self, node: RTreeNode[T, MBR]) -> None:
        """Propagate MBR changes up to the root."""
        node.recalculate_mbr(self.get_mbr, self.expand_mbr)
        if node.parent:
            self._adjust_tree(node.parent)

    def _split_node(self, node: RTreeNode[T, MBR]) -> None:
        """Split a node that exceeds max_entries using Quadratic Split."""
        # 1. Pick seeds
        c1, c2 = self._pick_seeds(node.children)

        # 2. Redistribute
        node.children.remove(c1)
        node.children.remove(c2)

        group1: RTreeNode[T, MBR] = RTreeNode(self.max_entries, is_leaf=node.is_leaf)
        group2: RTreeNode[T, MBR] = RTreeNode(self.max_entries, is_leaf=node.is_leaf)

        group1.add_child(c1, self.get_mbr(c1), self.expand_mbr)
        group2.add_child(c2, self.get_mbr(c2), self.expand_mbr)

        while node.children:
            if len(group1.children) + len(node.children) == self.min_entries:
                for c in list(node.children):
                    group1.add_child(c, self.get_mbr(c), self.expand_mbr)
                    node.children.remove(c)
                break
            if len(group2.children) + len(node.children) == self.min_entries:
                for c in list(node.children):
                    group2.add_child(c, self.get_mbr(c), self.expand_mbr)
                    node.children.remove(c)
                break

            # Pick next child to add
            child = self._pick_next(node.children, group1.mbr, group2.mbr)  # type: ignore
            node.children.remove(child)

            # Add to group with less enlargement
            area1 = self.get_volume(group1.mbr) if group1.mbr is not None else 0.0  # type: ignore
            area2 = self.get_volume(group2.mbr) if group2.mbr is not None else 0.0  # type: ignore

            mbr_c = self.get_mbr(child)

            new_mbr1 = self.expand_mbr(group1.mbr, mbr_c)
            enlarge1 = self.get_volume(new_mbr1) - area1

            new_mbr2 = self.expand_mbr(group2.mbr, mbr_c)
            enlarge2 = self.get_volume(new_mbr2) - area2

            if enlarge1 < enlarge2:
                group1.add_child(child, mbr_c, self.expand_mbr)
            elif enlarge2 < enlarge1:
                group2.add_child(child, mbr_c, self.expand_mbr)
            else:
                if area1 < area2:
                    group1.add_child(child, mbr_c, self.expand_mbr)
                elif area2 < area1:
                    group2.add_child(child, mbr_c, self.expand_mbr)
                else:
                    if len(group1.children) < len(group2.children):
                        group1.add_child(child, mbr_c, self.expand_mbr)
                    else:
                        group2.add_child(child, mbr_c, self.expand_mbr)

        # 3. Update hierarchy
        if node == self.root:
            new_root: RTreeNode[T, MBR] = RTreeNode(self.max_entries, is_leaf=False)
            new_root.add_child(group1, group1.mbr, self.expand_mbr)  # type: ignore
            new_root.add_child(group2, group2.mbr, self.expand_mbr)  # type: ignore
            self.root = new_root
        else:
            parent = node.parent
            if parent is not None:
                parent.children.remove(node)
                parent.add_child(group1, group1.mbr, self.expand_mbr)  # type: ignore
                parent.add_child(group2, group2.mbr, self.expand_mbr)  # type: ignore

                if len(parent.children) > self.max_entries:
                    self._split_node(parent)
                else:
                    self._adjust_tree(parent)

    def _pick_seeds(
        self, children: List[Union[RTreeNode[T, MBR], T]]
    ) -> Tuple[Union[RTreeNode[T, MBR], T], Union[RTreeNode[T, MBR], T]]:
        max_waste = -1.0
        seed1, seed2 = children[0], children[1]

        for i in range(len(children)):
            for j in range(i + 1, len(children)):
                m1 = self.get_mbr(children[i])
                m2 = self.get_mbr(children[j])

                combined = self.expand_mbr(m1, m2)
                waste = (
                    self.get_volume(combined)
                    - self.get_volume(m1)
                    - self.get_volume(m2)
                )

                if waste > max_waste:
                    max_waste = waste
                    seed1, seed2 = children[i], children[j]
        return seed1, seed2

    def _pick_next(
        self, children: List[Union[RTreeNode[T, MBR], T]], mbr1: MBR, mbr2: MBR
    ) -> Union[RTreeNode[T, MBR], T]:
        max_diff = -1.0
        best_child = children[0]

        for child in children:
            m = self.get_mbr(child)

            new_m1 = self.expand_mbr(mbr1, m)
            d1 = self.get_volume(new_m1) - self.get_volume(mbr1)

            new_m2 = self.expand_mbr(mbr2, m)
            d2 = self.get_volume(new_m2) - self.get_volume(mbr2)

            diff = abs(d1 - d2)
            if diff > max_diff:
                max_diff = diff
                best_child = child
        return best_child

    def search(self, query_mbr: MBR) -> List[T]:
        """Find all items whose MBR overlaps with the query MBR."""
        results: List[T] = []
        if self.root.mbr is None:
            return results
        self._search_recursive(self.root, query_mbr, results)
        return results

    def _search_recursive(
        self, node: RTreeNode[T, MBR], query_mbr: MBR, results: List[T]
    ) -> None:
        if node.mbr is None or not self.overlaps(node.mbr, query_mbr):
            return

        if node.is_leaf:
            for child in node.children:
                item_mbr = self.get_mbr(child)  # type: ignore
                if self.overlaps(item_mbr, query_mbr):
                    results.append(child)  # type: ignore
        else:
            for child in node.children:
                if isinstance(child, RTreeNode):
                    self._search_recursive(child, query_mbr, results)
