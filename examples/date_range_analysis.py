"""
Example: Data Range Analysis

This example demonstrates analyzing data ranges, finding gaps,
and computing coverage statistics.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intervals import Set, Interval


def main():
    print("=" * 60)
    print("Data Range Analysis Example")
    print("=" * 60)
    
    # Simulate sensor data ranges (timestamps in seconds)
    # Some data is missing due to sensor failures
    data_ranges = Set([
        Interval(0, 1000),       # First chunk
        Interval(1500, 2500),    # Second chunk (gap: 1000-1500)
        Interval(2800, 4000),    # Third chunk (gap: 2500-2800)
        Interval(4500, 6000),    # Fourth chunk (gap: 4000-4500)
    ])
    
    print("\nAvailable data ranges:")
    for i, range_interval in enumerate(data_ranges, 1):
        print(f"  {i}. {range_interval} ({range_interval.length():.0f} seconds)")
    
    # Expected data range
    expected_range = Interval(0, 6000)
    print(f"\nExpected range: {expected_range} ({expected_range.length():.0f} seconds)")
    
    # Find missing data (gaps)
    gaps = data_ranges.complement(Set([expected_range]))
    
    print(f"\nMissing data (gaps):")
    if len(gaps) == 0:
        print("  None - complete coverage!")
    else:
        for i, gap in enumerate(gaps, 1):
            print(f"  {i}. {gap} ({gap.length():.0f} seconds)")
    
    # Calculate coverage statistics
    total_time = expected_range.length()
    covered_time = data_ranges.measure()
    missing_time = sum(gap.length() for gap in gaps)
    
    print(f"\nCoverage Statistics:")
    print(f"  Total time: {total_time:.0f} seconds")
    print(f"  Data available: {covered_time:.0f} seconds ({covered_time/total_time*100:.1f}%)")
    print(f"  Data missing: {missing_time:.0f} seconds ({missing_time/total_time*100:.1f}%)")
    
    # Check if specific timestamps are available
    timestamps_to_check = [500, 1200, 3500, 4200, 5500]
    
    print(f"\nChecking specific timestamps:")
    for ts in timestamps_to_check:
        if ts in data_ranges:
            # Find which interval contains this timestamp
            containing_interval = None
            for interval in data_ranges:
                if ts in interval:
                    containing_interval = interval
                    break
            print(f"  t={ts:4d}s: ✓ Available (in range {containing_interval})")
        else:
            print(f"  t={ts:4d}s: ✗ Missing")
    
    # Merge with new data
    print(f"\n" + "=" * 60)
    print("Adding new recovered data...")
    print("=" * 60)
    
    recovered_data = Set([
        Interval(1200, 1600),  # Fills part of first gap
        Interval(2600, 2900),  # Fills second gap
    ])
    
    print(f"\nRecovered data:")
    for i, range_interval in enumerate(recovered_data, 1):
        print(f"  {i}. {range_interval}")
    
    # Merge with existing data
    merged_data = data_ranges | recovered_data
    
    print(f"\nMerged data ranges:")
    for i, range_interval in enumerate(merged_data, 1):
        print(f"  {i}. {range_interval} ({range_interval.length():.0f} seconds)")
    
    # Recalculate coverage
    new_covered = merged_data.measure()
    new_gaps = merged_data.complement(Set([expected_range]))
    new_missing = sum(gap.length() for gap in new_gaps)
    
    print(f"\nUpdated Coverage:")
    print(f"  Data available: {new_covered:.0f} seconds ({new_covered/total_time*100:.1f}%)")
    print(f"  Data missing: {new_missing:.0f} seconds ({new_missing/total_time*100:.1f}%)")
    print(f"  Improvement: +{(new_covered - covered_time):.0f} seconds " +
          f"(+{(new_covered - covered_time)/total_time*100:.1f}%)")
    
    # Find largest gap
    if len(new_gaps) > 0:
        largest_gap = max(new_gaps, key=lambda g: g.length())
        print(f"\nLargest remaining gap: {largest_gap} ({largest_gap.length():.0f} seconds)")


if __name__ == "__main__":
    main()