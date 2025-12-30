# Copilot Instructions: Interval Arithmetic Library

## Architecture Overview

This is a Python library for interval arithmetic and set operations on the real number line. The core design follows **immutable data structures** with **mathematical correctness** as the primary goal.

### Core Components (src/intervals.py)

- **Interval**: Single continuous intervals with configurable open/closed boundaries `[a,b]`, `(a,b)`, `[a,b)`, `(a,b]`
- **Set**: Collections of disjoint intervals with automatic merging and normalization

### Key Architectural Patterns

1. **Immutability First**: All operations return new objects; never mutate existing ones
2. **Automatic Merging**: Set automatically merges overlapping/adjacent intervals on construction
3. **Boundary Semantics**: Open vs closed boundaries are critical - `(0,1)` and `[0,1]` behave differently
4. **Type-Safe Operations**: Strong typing with descriptive error messages via `src/errors.py`
5. **Python Protocol Compliance**: Full support for `in`, `hash()`, comparison operators, iteration

## Development Workflow

### Essential Commands (via Makefile)
```bash
make test              # Run pytest suite
make test-coverage     # Generate HTML coverage report
make lint             # Check with ruff + black
make format           # Auto-format with black + ruff + isort
make type-check       # Run mypy
make pre-commit       # Run all pre-commit hooks
```

### Testing Patterns
- **Fixtures in conftest.py**: Reusable test objects (points, intervals, disjoint intervals)
- **Parameterized tests**: Use `@pytest.mark.parametrize` for boundary condition testing
- **Error testing**: Verify specific exception types and messages
- **Property-based testing**: Test mathematical properties (associativity, commutativity)

Example test pattern:
```python
def test_interval_contains_point(self, small_interval, point_five):
    assert point_five in small_interval
    assert 5 in small_interval  # Also test numeric values
```

## Critical Implementation Details

### Boundary Handling
Open/closed boundaries affect all operations. When implementing:
- Check `open_start`/`open_end` flags
- Use `intervals_are_adjacent()` from utils.py for merge logic
- Remember: `(0,1)` and `[1,2]` are NOT adjacent, but `(0,1]` and `[1,2]` ARE

### Error Handling Conventions
Use helper functions from `src/errors.py`:
```python
# For legacy compatibility (still used in errors.py)
raise point_error('+', other)  # Auto-generates type error message
raise continuous_interval_error('<=', other)

# For validation
raise InvalidIntervalError(f"Invalid interval: start ({start}) must be <= end ({end})")
```

### Set Merge Algorithm
The `_add_interval_internal()` method is critical - it maintains the non-overlapping invariant:
1. Sort intervals by start point
2. Check each interval against existing ones for overlap/adjacency
3. Merge when `is_overlapping()` or `intervals_are_adjacent()` returns True
4. Union operation must handle all boundary combinations

### String Representation Standards
- Points: `Interval.point(5)` 
- Intervals: Mathematical notation `[0, 10]`, `(0, 10)`, `[0, 10)`, `(0, 10]`
- Set: `{[0, 5], [10, 15]}` or `∅` for empty

## Code Style Conventions

### Imports
Use relative imports within package: `from .errors import point_error`

### Documentation
- All public methods need comprehensive docstrings with Args/Returns/Raises/Examples
- Include mathematical notation in docstrings where relevant
- Examples should be runnable in doctest format

### Type Hints
- Use `TYPE_CHECKING` imports to avoid circular dependencies
- Forward reference classes as strings: `'ContinuousInterval'`
- Use Union types for operations that can return different types

### Testing Requirements
- Test mathematical properties (reflexivity, transitivity, etc.)
- Test boundary conditions extensively (open vs closed boundaries)
- Test error cases with specific exception types
- Use fixtures from conftest.py to avoid duplication
- Aim for 95%+ coverage (current standard)

## Common Pitfalls

1. **Boundary Logic**: Always consider how open/closed boundaries interact in operations
2. **Immutability**: Never modify objects in place - always return new instances
3. **Empty Intervals**: Handle empty intervals correctly in all operations
4. **Type Checking**: Use isinstance() checks before accessing attributes
5. **Merge Logic**: DisjointInterval merge algorithm must preserve mathematical correctness

## Integration Points

- Uses `utils.py` for interval comparison and adjacency logic
- All errors inherit from `IntervalError` base class
- Package exports controlled via `src/__init__.py` - update when adding public classes
- Test fixtures in `tests/conftest.py` - add new fixtures for common test objects

When implementing new features, prioritize mathematical correctness over performance, maintain immutability, and ensure comprehensive test coverage with both success and error cases.