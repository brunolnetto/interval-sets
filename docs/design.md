# Design & Implementation Details

This document covers the mathematical and algorithmic foundation of the `interval-sets` library.

## 1. Core Philosophy: Exact Set Theory
Unlike traditional "Interval Arithmetic" (which focused on error propagation in calculations), this library implements **exact set-theoretic operations** on the real line $\mathbb{R}$ and its Cartesian products $\mathbb{R}^n$.

### Topological Rigor
- **Boundary Handling**: We distinguish between open and closed boundaries.
- **Normalization**: Sets and Regions are always maintained in a disjoint, sorted form.
- **Degeneracy**: A point is simply a closed interval with zero length $[x, x]$. A point in ND is a Box with $N$ degenerate dimensions.

## 2. Multi-Dimensional Architecture

### The Box (Hyperrectangle)
A `Box` is defined as a strict Cartesian product of intervals: $B = I_1 \times I_2 \times ... \times I_n$.
- **Factorized Boundary behavior**: The boundary properties of a Box are derived from its component intervals.
- **Efficiency**: Most operations (intersection, containment, volume) are $O(N)$ where $N$ is the number of dimensions.

### The Set (ND Region)
A `Set` is a collection of **disjoint** `Box`es. 
- **Non-Convexity**: While a `Box` is always convex, a `Set` can represent arbitrary shapes (L-shapes, donuts, disjoint clusters) by composing boxes.
- **Disjoint Decomposition**: When two boxes overlap, the union is represented by decomposing one box into up to $2N$ disjoint fragments that do not overlap the other.

## 3. Key Algorithms

### Recursive Slicing (Difference)
The operation $A \setminus B$ for two boxes is the cornerstone of the library. It uses a recursive slicing strategy:
1. Compute intersection $O = A \cap B$. If empty, $A \setminus B = \{A\}$.
2. For each dimension $d$, slice $A$ along the boundaries of $O$ in that dimension.
3. Collect the "side" fragments and continue with the "center" part in the next dimension.

### Greedy Normalization
For $N$-dimensional sets, maintaining a **minimal** number of boxes is NP-Hard.
- **Our Strategy**: We guarantee **disjointness** but not **minimality**.
- **Insertion**: When adding a box $B$ to a set, we subtract all existing boxes from $B$ and add the resulting (disjoint) fragments.

## 4. Minkowski & Morphological Operations

The library implements morphological operations based on the Minkowski Sum ($A \oplus B$) and Minkowski Difference ($A \ominus B$).

- **Minkowski Sum (Dilation)**:
  - For Boxes: $(I_1 \times I_2) \oplus (J_1 \times J_2) = (I_1 + J_1) \times (I_2 + J_2)$.
  - For Sets: The union of all pairwise sums of component boxes.
- **Minkowski Difference (Erosion)**:
  - Defined as $A \ominus B = \{x : \{x\} \oplus B \subseteq A\}$.
  - For Sets: The intersection of $A$ eroded by each component box of $B$.

## 5. Advanced Analysis
- **Convex Hull**: The smallest `Box` (or `Interval`) containing all points in a set.
- **Diameter**: The maximum Euclidean distance between any two points. For a set, this is the length of the diagonal of its convex hull.
- **Hausdorff Distance**: A measure of how far two sets are from each other.
