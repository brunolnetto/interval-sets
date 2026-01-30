from src.multidimensional import Box, BoxSet
from src.intervals import Interval, IntervalSet
from src.spatial import RTree, RTreeNode
from typing import Optional, Union


# Helpers for internal R-tree testing
def get_mbr_internal(item: Union[Box, RTreeNode]) -> Box:
    if hasattr(item, "mbr") and item.mbr is not None:
        return item.mbr  # type: ignore
    return item  # type: ignore


def expand_mbr_internal(m1: Optional[Box], m2: Box) -> Box:
    if m1 is None:
        return m2
    return Box(
        [
            Interval(
                min(m1.intervals[i].start, m2.intervals[i].start),
                max(m1.intervals[i].end, m2.intervals[i].end),
            )
            for i in range(m1.dimension)
        ]
    )


def test_rtree_choose_leaf_comprehensive():
    def get_vol(b):
        return b.volume()

    def overlaps(b1, b2):
        return b1.overlaps(b2)

    tree = RTree(get_mbr_internal, expand_mbr_internal, get_vol, overlaps)

    node = RTreeNode(4, is_leaf=False)

    # c1: [0, 10], Area 10, 3 children
    c1 = RTreeNode(4, is_leaf=True)
    c1.mbr = Box([Interval(0, 10)])
    c1.children = [1, 2, 3]  # type: ignore

    # c2: [0, 10], Area 10, 1 child
    c2 = RTreeNode(4, is_leaf=True)
    c2.mbr = Box([Interval(0, 10)])
    c2.children = [1]  # type: ignore

    # c3: [0, 20], Area 20, 1 child
    c3 = RTreeNode(4, is_leaf=True)
    c3.mbr = Box([Interval(0, 20)])
    c3.children = [1]  # type: ignore

    node.add_child(c1, c1.mbr, expand_mbr_internal)
    node.add_child(c2, c2.mbr, expand_mbr_internal)
    node.add_child(c3, c3.mbr, expand_mbr_internal)

    # Target Box [0, 5]. Enlargement 0 for all.
    # Areas: c1=10, c2=10, c3=20.
    # Between c1 and c2, c2 has fewer children.
    # This hits lines: 91, 94, 98, 99.
    leaf = tree._choose_leaf(node, Box([Interval(0, 5)]))
    assert leaf == c2

    # Line 95: Area_after < min_area
    # c2 vs c3. 10 < 20. Hits update.
    # To hit it cleanly, we need inf -> c3 -> c1?
    # Logic: loop through children. first one sets min_enlargement/min_area.
    node.children = [c3, c1]
    # first child sets min_area=20. second child has area 10. updates.
    leaf = tree._choose_leaf(node, Box([Interval(0, 10)]))
    assert leaf == c1


def test_rtree_split_node_complex():
    def get_vol(b):
        return b.volume()

    def overlaps(b1, b2):
        return b1.overlaps(b2)

    tree = RTree(
        get_mbr_internal,
        expand_mbr_internal,
        get_vol,
        overlaps,
        min_entries=2,
        max_entries=4,
    )

    # seed starvation: Lines 130-137
    # s1, s2, b1, b2, b3.
    # s1 seed G1. s2 seed G2.
    # b1, b2 -> G2. (G1:1, G2:3). Left: 1.
    # G1 + 1 == 2 (min_entries). Group 1 gets the rest.
    node = RTreeNode(4, is_leaf=True)
    seeds = [Box([Interval(0, 1)]), Box([Interval(100, 101)])]
    others = [
        Box([Interval(101, 102)]),
        Box([Interval(102, 103)]),
        Box([Interval(0.1, 0.2)]),
    ]
    node.children = seeds + others
    node.mbr = Box([Interval(0, 103)])

    # To hit _split_node, we need a parent or root context
    tree.root = RTreeNode(4, is_leaf=False)
    tree.root.children = [node]
    node.parent = tree.root

    tree._split_node(node)
    assert len(tree.root.children) == 2


def test_rtree_split_area_tiebreak_nesting():
    def get_vol(b):
        return b.volume()

    def overlaps(b1, b2):
        return b1.overlaps(b2)

    tree = RTree(get_mbr_internal, expand_mbr_internal, get_vol, overlaps)

    # Logic in lines 161-169.
    # Tie in enlargement.
    # seed1 area 10. seed2 area 5.
    # item enlargement 0. Picks Area 5 (group 2). Hit 163-164.

    # seed1 area 5. seed2 area 10.
    # enlargement 0. Picks Area 5 (group 1). Hit 161-162.

    # seed1 area 10. seed2 area 10.
    # enlargement 0. Area tie. Picks group with fewer children (Group 2 initially).
    # Then picks Group 1.

    node = RTreeNode(4, is_leaf=True)
    node.children = [
        Box([Interval(0, 10)]),
        Box([Interval(0, 10)]),
        Box([Interval(0, 1)]),
        Box([Interval(0, 1)]),
        Box([Interval(0, 1)]),
    ]
    tree.root = RTreeNode(4, is_leaf=False)
    tree.root.children = [node]
    node.parent = tree.root
    tree._split_node(node)
    assert len(tree.root.children) == 2


def test_rtree_search_exit_branches():
    def get_vol(b):
        return 0

    def overlaps(b1, b2):
        return True

    tree = RTree(get_mbr_internal, expand_mbr_internal, get_vol, overlaps)

    # Line 229 coverage (empty root MBR)
    assert tree.search(Box([Interval(0, 1)])) == []

    # Line 244->243 (descend only into nodes)
    tree.insert(Box([Interval(0, 1)]))
    tree.root.is_leaf = False
    tree.root.children.append("not-a-node")
    tree.search(Box([Interval(0, 1)]))


def test_multidimensional_set_build_index_empty():
    s = BoxSet()
    s._build_index()  # Line 709 cover
    assert s._index is None


def test_multidimensional_set_add_dimension_logic():
    # Cover BoxSet.add logic branches
    s = BoxSet()
    s.add(Box([Interval(0, 1)]))  # First add sets dimension
    # s._dimension = 1

    # Coverage for 542 (if not fragments)?
    # add box [0.1, 0.9]. existing [0, 1] contains it. fragments becomes empty.
    s.add(Box([Interval(0.1, 0.9)]))

    # Coverage for 563 (is_bounded)
    assert s.is_bounded() is True

    # Coverage for 565 (is_open)
    s_open = BoxSet([Box([Interval.open(0, 1)])])
    assert s_open.is_open() is True


def test_intervals_hausdorff_midpoint_not_in_interval():
    # Hit missing branch 1573->1568 (if midpoint inside)
    # A = [0, 1]
    # B = [5, 6] | [8, 9] -> gap (6, 8) midpoint 7.
    # 0 < 7 < 1 is False.
    A = IntervalSet([Interval(0, 1)])
    B = IntervalSet([Interval(5, 6), Interval(8, 9)])
    A.hausdorff_distance(B)
