# Copilot Instructions: Interval Sets Library

## Architecture Overview

This is a Python library for interval set operations on the real number line. The core design follows **immutable data structures** with **mathematical correctness** (Set Theory) as the primary goal.

### Core Components (src/intervals.py)

- **Interval**: Single continuous intervals with configurable open/closed boundaries `[a,b]`, `(a,b)`, `[a,b)`, `(a,b]`
- **Set**: Collections of disjoint intervals with automatic merging and normalization
- **Point**: Degenerate interval `[x,x]` inheriting from `Interval`

### Key Architectural Patterns

1.  **Immutability First**: All operations (Union, Intersection, etc.) return new objects; never mutate existing ones (except for internal init normalization).
2.  **Automatic Merging (Canonical Form)**: `Set` automatically sorts and merges overlapping/adjacent intervals on construction (`_normalize`).
    -   *Example:* `Set([ [0,5], [4,10] ])` -> `Set([ [0,10] ])`
    -   *Example:* `Set([ (0,10), [10,20) ])` -> `Set([ (0,20) ])`
3.  **Boundary Semantics**: Open vs closed boundaries are critical.
    -   `[0, 1]` intersects `(1, 2)` -> Empty (disjoint)
    -   `[0, 1]` intersects `[1, 2]` -> Point `1`
    -   `[0, 1]` unions `(1, 2)` -> `[0, 2)` (Adjacent merge)
4.  **Set Theory vs Interval Arithmetic**: This library implements **Set Operations** (Union, Intersection, Difference), NOT numerical error-bounding arithmetic.
    -   `+` operator acts as Union (if applicable/safe) or is discouraged in favor of `|`.
5.  **Type-Safe Operations**: Strong typing with descriptive error messages via `src/errors.py`.

## Development Workflow

### Essential Commands
```bash
pytest                 # Run test suite
pytest --cov=src       # Run with coverage (current standard: 100%)
```

### Testing Patterns
-   **Math Rigor Tests (tests/test_math_rigor.py)**: Use specific tests for mathematical edge cases (e.g., disconnected difference results, adjacent unions).
-   **Fixtures**: Use standard pytest fixtures.
-   **Coverage**: Maintain 100% branch coverage.

## Critical Implementation Details

### Boundary Handling
Open/closed boundaries affect all operations. When implementing:
-   **Union**: If boundaries touch/overlap, the result is *Closed* if *either* source is Closed (Logic: `open = open1 AND open2` if boundaries match).
-   **Intersection**: If boundaries touch/overlap, the result is *Open* if *either* source is Open (Logic: `open = open1 OR open2` if boundaries match).

### Set Normalization
The `_normalize()` method in `Set` is the source of truth for canonical representation:
1.  **Filter**: `_add_element` filters out empty intervals/sets immediately.
2.  **Sort**: Intervals sorted by start, then end.
3.  **Merge**: Greedy merge of overlapping or adjacent intervals.

### String Representation Standards
-   **Points**: `Point(5)` or sometimes formatted in sets.
-   **Intervals**: Mathematical notation `[0, 10]`, `(0, 10)`, `[0, 10)`, `(0, 10]`
-   **Set**: `{[0, 5], [10, 15]}` or `∅` for empty

## Code Style Conventions

### Imports
-   Use relative imports `from . import ...` within `src/`.
-   Use explicit imports `from src.intervals import ...` in tests.

### Type Hints
-   Use `TYPE_CHECKING` imports to avoid circular dependencies.
-   Forward reference classes as strings: `'Interval'`, `'Set'`.
-   Use `Union` or `|` (Python 3.10+) for return types: `Union[Interval, Set]`.

## Common Pitfalls

1.  **Set Operations Return Types**: Operations like `union` can return either an `Interval` (if connected) or a `Set` (if disjoint). Always check type or use polymorphic methods carefully.
2.  **Immutability**: `Set` has in-place operators (`|=`) which technically modify internal state *in standard Python sets*, but here they generally return new instances or reassignment. Be careful with internal state (`self._intervals`) which should only be modified during `__init__`.
3.  **Adjacent vs Overlap**: `[0,1)` and `[1,2]` are adjacent (mergeable). `[0,1)` and `(1,2)` are disjoint (gap at 1).

## Integration Points

-   **Errors**: `InvalidIntervalError` for bad construction `(5,0)`.
-   **Utils**: `intervals_are_adjacent` helper.

When implementing new features, prioritize **mathematical correctness** (Set Theory strictness) over performance. Ensure all edge cases (empty sets, infinite bounds if added, adjacent boundaries) are covered by tests.