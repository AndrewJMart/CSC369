import csv
from collections import defaultdict
import datetime
import time
import sys

def validate_dates(start_date, end_date):
    """Validate that end_date is after start_date."""
    if start_date >= end_date:
        raise ValueError("End date must be after start date.")

def color_pixel_counter(start_date: str, end_date: str):
    """Count the most placed color and pixel in the specified timeframe."""
    start_time = time.perf_counter_ns()
    pixel_dict = defaultdict(int)
    color_dict = defaultdict(int)
    
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H")
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d %H")
    
    with open(r"C:\Users\Andrew\Documents\CSC369\Week 1\2022_place_csv.csv", 'r') as raw_file:
        raw_csv = csv.reader(raw_file)
        next(raw_csv)  # Skip header
        
        for row in raw_csv:
            row_datetime = datetime.datetime.strptime(row[0].split(":")[0], "%Y-%m-%d %H")
            
            if start_datetime <= row_datetime <= end_datetime:
                color_dict[row[2]] += 1
                pixel_dict[row[3]] += 1

    # Find the most placed color and pixel
    common_color, color_placed = max(color_dict.items(), key=lambda item: item[1])
    common_pixel, pixel_placed = max(pixel_dict.items(), key=lambda item: item[1])
    
    end_time = time.perf_counter_ns()
    execution_time_ms = (end_time - start_time) // 1_000_000 
    
    # Print the execution report
    print(f"Execution Report:")
    print(f"- Timeframe: {start_date} to {end_date}")
    print(f"- Execution Time: {execution_time_ms} ms")
    print(f"- Most Placed Color: {common_color} (Placed {color_placed} times)")
    print(f"- Most Placed Pixel Location: {common_pixel} (Placed {pixel_placed} times)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        for element in sys.argv:
            print(element)
        print("Usage: python script.py <start_date> <end_date>")
        print("Example: python script.py '2022-04-01 12' '2022-04-01 18'")
        sys.exit(1)
    
    # Parse and validate input arguments
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    try:
        validate_dates(
            datetime.datetime.strptime(start_date, "%Y-%m-%d %H"),
            datetime.datetime.strptime(end_date, "%Y-%m-%d %H")
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Run the analysis for the specified timeframe
    color_pixel_counter(start_date, end_date)
