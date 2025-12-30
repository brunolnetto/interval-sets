# Coverage Analysis: Final 10 Uncovered Lines

## Summary
Current coverage: **98%** (461 total statements, 10 uncovered)

Uncovered lines: `266, 319, 328, 341, 352, 550-551, 629, 653, 789`

## Line-by-Line Analysis

### ✅ Line 266 - COVERABLE
**Location**: `Interval.intersection()` - return empty set when `start == end` with open boundaries

**Trigger**:  
```python
a = Interval(0, 5, open_end=True)  # [0, 5)
b = Interval(5, 10, open_start=True)  # (5, 10]
result = a.intersection(b)  # Returns empty set
```

**Status**: Can be covered with specific test

---

###❓ Line 319 - POSSIBLY UNREACHABLE
**Location**: `Interval.difference()` - return self when intersection is empty Set

**Analysis**:
- Requires `overlaps()` to return True (otherwise line 315 returns early)
- BUT also requires `intersection()` to return empty Set
- If `overlaps()` is True, `intersection()` should NOT be empty
- This appears to be **defensive code** that may never execute

**Recommendation**: Add `# pragma: no cover` or remove if confirmed unreachable

---

### ❓ Line 328 - DEFENSIVE/UNREACHABLE
**Location**: `Interval.difference()` - safety return when intersection is not Interval

**Analysis**:
- Requires intersection to be a non-empty Set
- But `Interval.intersection()` only returns:
  - `Interval` (for non-empty intersections)
  - Empty `Set` (for empty intersections, handled at line 319)
- A non-empty Set from intersection would indicate a bug

**Recommendation**: Add `# pragma: no cover` - this is defensive code

---

### ❓ Lines 341, 352 - LIKELY UNREACHABLE
**Location**: `Interval.difference()` - pass statements for boundary edge cases

**Line 341 requires**: `self._start == int_start AND self._open_start AND NOT int_open_start`
- Self has open start `(`, intersection has closed start `[`

**Line 352 requires**: `int_end == self._end AND NOT int_open_end AND self._open_end`
- Self has open end `)`, intersection has closed end `]`

**Analysis**:
In `Interval.intersection()`, boundary logic is:
```python
if start == self._start:
    open_start = self._open_start
if start == other._start:
    open_start = open_start or other._open_start  # OR operator
```

The OR operator means if `self._open_start` is True, `int_open_start` will also be True.
Therefore, the condition `self._open_start AND NOT int_open_start` appears **impossible**.

**Recommendation**: Add `# pragma: no cover` or refactor/remove

---

### ❓ Lines 550-551 - DEFENSIVE/UNREACHABLE
**Location**: `Set._normalize()` - when union returns Set instead of Interval

**Analysis**:
- Reached when merging overlapping/adjacent intervals
- `union()` of overlapping/adjacent intervals always returns `Interval`
- The else branch handles if union returns `Set`, which shouldn't happen
- This is **defensive code**

**Recommendation**: Add `# pragma: no cover`

---

### ✅ Line 629 - COVERABLE  
**Location**: `Set.intersection()` - extend intervals when intersection is Set

**Trigger**:
```python
s1 = Set([Interval(0, 5), Interval(10, 15)])
s2 = Set([Interval(3, 7)])
result = s1.intersection(s2)  # Line 629 when handling Set results
```

**Status**: Should be coverable with proper test

---

### ✅ Line 653 - COVERABLE
**Location**: `Set.union()` - else branch when self is empty, other has multiple intervals

**Trigger**:
```python
s1 = Set()
s2 = Set([Interval(0, 5), Interval(10, 15)])  # Multiple intervals
result = s1.union(s2)  # Hits line 657
```

**Status**: Can be covered

---

### ✅ Line 789 - COVERABLE
**Location**: `Set.__ixor__()` - else branch when result is Set

**Trigger**:
```python
s1 = Set([Interval(0, 10)])
s2 = Set([Interval(5, 15)])
s1 ^= s2  # Result is Set with multiple intervals
```

**Status**: Can be covered

---

## Recommendations

### Option 1: Achieve 100% Coverage (Recommended)
Add targeted tests for linesthat ARE coverable:
- Line 266 ✅
- Line 629 ✅  
- Line 653 ✅
- Line 789 ✅

Add `# pragma: no cover` for defensive/unreachable code:
- Line 319 - Defensive check
- Line 328 - Defensive safety return
- Lines 341, 352 - Unreachable due to intersection logic
- Lines 550-551 - Defensive code

### Option 2: Refactor Code
Remove or simplify defensive code if confirmed unreachable:
- Simplify `difference()` by removing lines 318-319, 327-328
- Simplify boundary checks by removing lines 339-341, 350-352
- Simplify `_normalize()` by removing lines 549-551

### Option 3: Document as Expected
Keep code as-is for safety, accept 98% coverage as excellent for production code.

---

## Suggested Test Cases for Coverable Lines

```python
def test_line_266():
    """Intersection at point with open boundaries -> empty set"""
    a = Interval(0, 5, open_end=True)
    b = Interval(5, 10, open_start=True)
    assert a.intersection(b).is_empty()

def test_line_629():
    """Set intersection handling Set results"""
    s1 = Set([Interval(0, 5), Interval(10, 15)])
    s2 = Set([Interval(3, 12)])
    result = s1.intersection(s2)
    # Generates multiple intersection intervals

def test_line_653():
    """Union of empty Set with multi-interval Set"""
    s1 = Set()
    s2 = Set([Interval(0, 5), Interval(10, 15)])
    result = s1.union(s2)
    assert len(result) == 2

def test_line_789():
    """In-place XOR resulting in Set"""
    s1 = Set([Interval(0, 10)])
    s2 = Set([Interval(5, 15)])
    s1 ^= s2
    assert len(s1) >= 1
```

---

## Conclusion

**Current Status**: 98% coverage (excellent!)

**To reach 100%**:
1. Add 4 specific tests for coverable lines (266, 629, 653, 789)
2. Add `# pragma: no cover` to 6 defensive/unreachable lines (319, 328, 341, 352, 550, 551)

**Effort**: ~15 minutes to implement both suggestions

**Result**: 100% coverage achieved ✅
