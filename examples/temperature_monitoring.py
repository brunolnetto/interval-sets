"""
Example: Temperature Range Monitoring

This example demonstrates using intervals for monitoring
temperature ranges, validating readings, and detecting anomalies.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intervals import Interval, IntervalSet


def main():
    print("=" * 60)
    print("Temperature Monitoring System")
    print("=" * 60)
    
    # Define temperature ranges (in Celsius)
    optimal_range = Interval(18, 25)        # Ideal: 18-25°C
    acceptable_range = Interval(15, 28)     # Acceptable: 15-28°C
    warning_cold = Interval(10, 15)         # Warning: 10-15°C
    warning_hot = Interval(28, 35)          # Warning: 28-35°C
    critical_range = IntervalSet([
        Interval(-10, 10),                  # Critical cold
        Interval(35, 50)                    # Critical hot
    ])
    
    print("\nTemperature Range Definitions:")
    print(f"  Optimal:    {optimal_range}°C")
    print(f"  Acceptable: {acceptable_range}°C")
    print(f"  Warning:    {warning_cold}°C or {warning_hot}°C")
    print(f"  Critical:   < 10°C or > 35°C")
    
    # Simulate temperature readings
    temperature_readings = [
        (8, "Server Room A"),
        (22, "Server Room B"),
        (16, "Storage Area"),
        (29, "Office Space"),
        (38, "Data Center"),
        (12, "Backup Room"),
        (24, "Control Room"),
    ]
    
    print("\n" + "=" * 60)
    print("Analyzing Temperature Readings")
    print("=" * 60)
    
    optimal_count = 0
    acceptable_count = 0
    warning_count = 0
    critical_count = 0
    
    for temp, location in temperature_readings:
        status = ""
        symbol = ""
        
        if temp in critical_range:
            status = "CRITICAL"
            symbol = "🚨"
            critical_count += 1
        elif temp in warning_cold or temp in warning_hot:
            status = "WARNING"
            symbol = "⚠️ "
            warning_count += 1
        elif temp in optimal_range:
            status = "OPTIMAL"
            symbol = "✓ "
            optimal_count += 1
        elif temp in acceptable_range:
            status = "ACCEPTABLE"
            symbol = "○ "
            acceptable_count += 1
        else:
            status = "UNKNOWN"
            symbol = "? "
        
        print(f"{symbol} {location:20s} {temp:5.1f}°C - {status}")
    
    # Summary statistics
    total = len(temperature_readings)
    print(f"\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Total readings: {total}")
    print(f"  Optimal:        {optimal_count} ({optimal_count/total*100:.0f}%)")
    print(f"  Acceptable:     {acceptable_count} ({acceptable_count/total*100:.0f}%)")
    print(f"  Warning:        {warning_count} ({warning_count/total*100:.0f}%)")
    print(f"  Critical:       {critical_count} ({critical_count/total*100:.0f}%)")
    
    if critical_count > 0:
        print(f"\n🚨 ALERT: {critical_count} critical temperature(s) detected!")
    elif warning_count > 0:
        print(f"\n⚠️  WARNING: {warning_count} temperature(s) need attention")
    else:
        print(f"\n✓ All temperatures within acceptable range")
    
    # Calculate safe operating range
    print(f"\n" + "=" * 60)
    print("Operating Range Analysis")
    print("=" * 60)
    
    # Intersection of acceptable ranges shows the safest zone
    safe_zone = optimal_range & acceptable_range
    print(f"\nSafest operating zone: {safe_zone}°C")
    
    # Find the range that needs the most attention
    # (temperatures outside optimal but inside acceptable)
    needs_adjustment = acceptable_range - optimal_range
    
    print(f"\nRanges needing adjustment to reach optimal:")
    if isinstance(needs_adjustment, IntervalSet):
        for i, range_adj in enumerate(needs_adjustment, 1):
            if range_adj.end <= optimal_range.start:
                print(f"  {i}. {range_adj}°C (too cold - increase heating)")
            else:
                print(f"  {i}. {range_adj}°C (too hot - increase cooling)")
    else:
        # Single interval result
        if needs_adjustment.end <= optimal_range.start:
            print(f"  1. {needs_adjustment}°C (too cold - increase heating)")
        else:
            print(f"  1. {needs_adjustment}°C (too hot - increase cooling)")
    
    # Find operating margin
    print(f"\n" + "=" * 60)
    print("Safety Margins")
    print("=" * 60)
    
    # Distance from optimal to warning zones
    cold_margin = optimal_range.start - warning_cold.end
    hot_margin = warning_hot.start - optimal_range.end
    
    print(f"\nMargin before warning:")
    print(f"  Cold side: {cold_margin:.1f}°C")
    print(f"  Hot side:  {hot_margin:.1f}°C")
    
    # Check specific temperature scenario
    print(f"\n" + "=" * 60)
    print("Scenario Analysis")
    print("=" * 60)
    
    test_temp = 17.5
    print(f"\nIf temperature drops to {test_temp}°C:")
    
    if test_temp in optimal_range:
        print("  ✓ Still in optimal range")
    elif test_temp in acceptable_range:
        distance_to_optimal = optimal_range.start - test_temp
        print(f"  ○ Acceptable, but {distance_to_optimal:.1f}°C below optimal")
        print(f"    Action: Increase temperature by {distance_to_optimal:.1f}°C")
    elif test_temp in warning_cold:
        distance_to_acceptable = acceptable_range.start - test_temp
        print(f"  ⚠️  Warning! {distance_to_acceptable:.1f}°C below acceptable")
        print(f"    Action: Immediately increase temperature")
    elif test_temp in critical_range:
        print(f"  🚨 CRITICAL! Temperature dangerously low")
        print(f"    Action: Emergency heating required")


if __name__ == "__main__":
    main()