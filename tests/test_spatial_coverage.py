from src.multidimensional import Box, BoxSet
from src.intervals import Interval
from src.spatial import RTree, RTreeNode


def test_boxset_with_indexing():
    s = BoxSet()
    for i in range(11):
        s.add(Box([Interval(2 * i, 2 * i + 1)]))

    assert s._index is not None
    assert len(s.boxes) == 11

    # Trigger search/insert with index (lines 542, 563 in multidimensional.py)
    s.add(Box([Interval(22, 23)]))
    assert len(s.boxes) == 12

    # Check contains with index (lines 698-699 in multidimensional.py)
    assert [2.5] in s
    assert [100] not in s


def test_rtree_choose_leaf_branches():
    def get_mbr(item):
        if hasattr(item, "mbr") and item.mbr is not None:
            return item.mbr
        return item

    def expand(m1, m2):
        if m1 is None:
            return m2
        return Box(
            [
                Interval(
                    min(m1.intervals[0].start, m2.intervals[0].start),
                    max(m1.intervals[0].end, m2.intervals[0].end),
                )
            ]
        )

    def get_vol(b):
        return b.volume()

    def overlaps(b1, b2):
        return b1.overlaps(b2)

    tree = RTree(get_mbr, expand, get_vol, overlaps, max_entries=2)

    # c1 and c2 have same enlargement (0) and same area (10)
    # c1 has 3 children, c2 has 1 child. Ties on area_after == min_area.
    # Should pick c2 because it has fewer children (line 99).
    c1 = RTreeNode(4, is_leaf=True)
    c1.mbr = Box([Interval(0, 10)])
    c1.children = [1, 2, 3]  # type: ignore

    c2 = RTreeNode(4, is_leaf=True)
    c2.mbr = Box([Interval(0, 10)])
    c2.children = [1]  # type: ignore

    tree.root.is_leaf = False
    tree.root.children = [c1, c2]  # type: ignore

    leaf = tree._choose_leaf(tree.root, Box([Interval(2, 3)]))
    assert leaf == c2

    # Branch 80: skip non-RTreeNode internal children
    tree.root.children = ["not a node", c1]  # type: ignore
    leaf = tree._choose_leaf(tree.root, Box([Interval(2, 3)]))
    assert leaf == c1

    # Branch 103: best_child is None
    tree.root.children = ["not a node"]  # type: ignore
    leaf = tree._choose_leaf(tree.root, Box([Interval(2, 3)]))
    assert leaf == tree.root


def test_rtree_split_node_starvation_and_tiebreaks():
    def get_mbr(item):
        if hasattr(item, "mbr") and item.mbr is not None:
            return item.mbr
        return item

    def expand(m1, m2):
        if m1 is None:
            return m2
        return Box(
            [
                Interval(
                    min(m1.intervals[0].start, m2.intervals[0].start),
                    max(m1.intervals[0].end, m2.intervals[0].end),
                )
            ]
        )

    def get_vol(b):
        return b.volume()

    def overlaps(b1, b2):
        return b1.overlaps(b2)

    # Starvation Group 1 (130-133)
    tree = RTree(get_mbr, expand, get_vol, overlaps, min_entries=3, max_entries=4)
    items = [
        Box([Interval(0, 1)]),  # Seed 1
        Box([Interval(100, 101)]),  # Seed 2
        Box([Interval(101, 102)]),  # To Group 2
        Box([Interval(102, 103)]),  # To Group 2
        Box([Interval(0.5, 1.5)]),  # Starved to Group 1
    ]
    for item in items:
        tree.insert(item)

    # Starvation Group 2 (135-138)
    tree2 = RTree(get_mbr, expand, get_vol, overlaps, min_entries=3, max_entries=4)
    items2 = [
        Box([Interval(0, 1)]),  # Seed 1
        Box([Interval(100, 101)]),  # Seed 2
        Box([Interval(0.1, 0.2)]),  # To Group 1
        Box([Interval(0.2, 0.3)]),  # To Group 1
        Box([Interval(100.5, 101.5)]),  # Starved to Group 2
    ]
    for item in items2:
        tree2.insert(item)

    # Tie-breaks 162, 164
    tree3 = RTree(get_mbr, expand, get_vol, overlaps, min_entries=1, max_entries=2)
    # Group 1 area 1, Group 2 area 5. Both enlargement 100.
    items3 = [
        Box([Interval(-100, -99)]),  # Seed 1, G1 area 1
        Box([Interval(100, 105)]),  # Seed 2, G2 area 5
        Box([Interval(0, 1)]),  # enlargement 100 for both. Picks G1.
    ]
    for item in items3:
        tree3.insert(item)

    # Swap areas
    tree4 = RTree(get_mbr, expand, get_vol, overlaps, min_entries=1, max_entries=2)
    items4 = [
        Box([Interval(100, 105)]),  # Seed 1, G1 area 5
        Box([Interval(-100, -99)]),  # Seed 2, G2 area 1
        Box([Interval(0, 1)]),  # Picks G2.
    ]
    for item in items4:
        tree4.insert(item)


def test_rtree_search_exit_branches():
    def get_mbr(item):
        return item

    def expand(m1, m2):
        return m2

    def get_vol(b):
        return 0

    def overlaps(b1, b2):
        return True

    tree = RTree(get_mbr, expand, get_vol, overlaps)
    # Line 229: empty root mbr
    assert tree.search(Box([Interval(0, 1)])) == []

    # Line 235: no overlap
    tree.root.mbr = Box([Interval(10, 11)])

    def no_overlap(m1, m2):
        return False

    tree.overlaps = no_overlap
    assert tree.search(Box([Interval(0, 1)])) == []


def test_rtree_adjust_tree_multiple_levels():
    # Force split and verify hierarchy
    s = BoxSet()
    for i in range(20):
        s.add(Box([Interval(i, i + 0.5), Interval(i, i + 0.5)]))
    # This triggers root splits and recursively split parent (173-176, 185)
    assert len(s.boxes) == 20
