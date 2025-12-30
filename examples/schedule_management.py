"""
Example: Schedule Management with Intervals

This example demonstrates how to use the interval library for 
managing schedules, finding free time slots, and checking conflicts.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.intervals import Interval, Set


def main():
    print("=" * 60)
    print("Schedule Management Example")
    print("=" * 60)
    
    # Define work day (9 AM to 5 PM, represented as hours)
    work_day = Interval(9, 17)
    print(f"\nWork day: {work_day}")
    
    # Define busy times (meetings)
    meetings = Set([
        Interval(9, 10),      # Team standup 9-10 AM
        Interval(11, 12.5),   # Client meeting 11 AM-12:30 PM
        Interval(14, 16)      # Project review 2-4 PM
    ])
    
    print("\nScheduled meetings:")
    for i, meeting in enumerate(meetings, 1):
        print(f"  {i}. {meeting}")
    
    # Find available time slots
    available = meetings.complement(Set([work_day]))
    
    print("\nAvailable time slots:")
    for i, slot in enumerate(available, 1):
        start_hour = int(slot.start)
        start_min = int((slot.start % 1) * 60)
        end_hour = int(slot.end)
        end_min = int((slot.end % 1) * 60)
        
        print(f"  {i}. {start_hour:02d}:{start_min:02d} - {end_hour:02d}:{end_min:02d}")
    
    # Calculate busy vs available time
    total_work_hours = work_day.length()
    busy_hours = meetings.measure()
    available_hours = total_work_hours - busy_hours
    
    print(f"\nTime summary:")
    print(f"  Total work hours: {total_work_hours:.1f} hours")
    print(f"  Busy time: {busy_hours:.1f} hours ({busy_hours/total_work_hours*100:.1f}%)")
    print(f"  Available time: {available_hours:.1f} hours ({available_hours/total_work_hours*100:.1f}%)")
    
    # Check if a specific time is available
    lunch_time = 13.0  # 1:00 PM  
    if lunch_time in meetings:
        # Find which meeting contains this time
        containing_meeting = None
        for meeting in meetings:
            if lunch_time in meeting:
                containing_meeting = meeting
                break
        print(f"\n⚠️  1:00 PM is busy (meeting: {containing_meeting})")
    else:
        print(f"\n✓ 1:00 PM is available for lunch!")
    
    # Try to schedule a new meeting (should not conflict)
    new_meeting = Interval.open(10, 11)  # (10, 11) AM - open intervals don't include endpoints
    
    print(f"\nTrying to schedule new meeting: {new_meeting}")
    
    # Check for conflicts
    conflicts = meetings & Set([new_meeting])
    
    if not conflicts.is_empty():
        print(f"  ✗ Conflict detected! Overlaps with existing meeting(s)")
    else:
        print(f"  ✓ No conflicts! Meeting can be scheduled")
        
        # Add the meeting
        updated_schedule = meetings | Set([new_meeting])
        print(f"\nUpdated schedule:")
        for i, meeting in enumerate(updated_schedule, 1):
            print(f"  {i}. {meeting}")
    
    # Try to schedule a conflicting meeting
    print(f"\nTrying to schedule conflicting meeting: [9.5, 10.5]")
    conflicting_meeting = Interval(9.5, 10.5)
    conflicts2 = meetings & Set([conflicting_meeting])
    
    if not conflicts2.is_empty():
        print(f"  ✗ Conflict detected! Overlaps with: {conflicts2}")
    else:
        print(f"  ✓ No conflicts!")


if __name__ == "__main__":
    main()