# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-11-12

### Changed
- **BREAKING**: Complete architecture migration from Point/ContinuousInterval/DisjointInterval/EmptySet to clean Interval/Set design
- `Interval` class replaces both Point and ContinuousInterval with unified API
- `Set` class replaces DisjointInterval and EmptySet with automatic normalization
- Mathematical correctness with Union return types allowing operations to return appropriate types
- Enhanced boundary semantics with `open_start`/`open_end` parameters
- Rich factory methods: `Interval.point()`, `Interval.open()`, `Set.points()`, etc.

### Removed
- Legacy classes: `Point`, `ContinuousInterval`, `DisjointInterval`, `EmptySet` (no longer exported)
- Legacy test files and fixtures

### Added
- Dynamic return types for mathematical correctness
- Comprehensive operator overloading (`|`, `&`, `-`, `^`, `<=`, `>=`, `in`)
- Rich utility methods: `measure()`, `boundary_points()`, `infimum()/supremum()`
- Clean integration test suite with real-world scenarios

## [0.1.0] - 2024-11-11

### Added
- Initial release of interval-arithmetic library
- `Point` class for representing points on the real number line
  - Arithmetic operations: `+`, `-`
  - Comparison operations: `==`, `!=`, `<`, `<=`, `>`, `>=`
  - Hashable for use in sets and dictionaries
- `ContinuousInterval` class for representing intervals with open/closed boundaries
  - Support for `[a, b]`, `(a, b)`, `[a, b)`, `(a, b]` notation
  - Set operations: `union()`, `intersection()`, `difference()`
  - Containment checking: `contains()`, `contains_value()`, `contains_point()`
  - Membership testing with `in` operator
  - Interval arithmetic: `+` for merging, `-` for difference
  - Comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`
  - Hashable for use in sets and dictionaries
- `DisjointInterval` class for managing collections of non-overlapping intervals
  - Automatic merging of overlapping intervals
  - Set operations: `union()`, `intersection()`, `difference()`, `complement()`
  - Collection interface: iteration, indexing, length
  - Membership testing with `in` operator
  - Methods: `add_interval()`, `get_interval_containing_point()`, `total_length()`
- `EmptySet` class for representing empty sets
- Custom exception classes:
  - `IntervalError` - Base exception for interval operations
  - `InvalidIntervalError` - For invalid interval construction
  - `OverlappingIntervalError` - For overlapping interval violations
- Input validation:
  - Prevents NaN values in Points and ContinuousIntervals
  - Prevents infinite values in Points and ContinuousIntervals
  - Clear error messages with actual values shown
- Comprehensive documentation:
  - Full API documentation with examples
  - README with quick start guide
  - Example scripts for common use cases
- Test suite with 95%+ coverage:
  - 70+ test cases
  - Tests for all core functionality
  - Edge case testing
  - Input validation testing

### Documentation
- README.md with full API reference and examples
- CHANGELOG.md for tracking changes
- Example scripts:
  - `examples/schedule_management.py` - Calendar and meeting scheduling
  - `examples/data_range_analysis.py` - Data coverage and gap analysis
  - `examples/temperature_monitoring.py` - Temperature range validation

### Development
- Complete project setup with `pyproject.toml`
- Configured tools:
  - pytest for testing
  - pytest-cov for coverage reporting
  - black for code formatting
  - ruff for linting
  - mypy for type checking
- Type hints throughout the codebase
- Comprehensive docstrings for all public APIs

## [Unreleased]

### Planned
- Support for infinite intervals (unbounded intervals)
- Interval arithmetic with uncertainty propagation
- Visualization tools for intervals
- Performance optimizations for large interval collections
- Additional set operations (symmetric difference, etc.)
- Serialization/deserialization support (JSON, pickle)
- Integration with numpy arrays
- Command-line interface for interval operations

---

[0.1.0]: https://github.com/yourusername/interval-arithmetic/releases/tag/v0.1.0